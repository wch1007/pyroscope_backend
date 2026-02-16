from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import json
import logging
from app.database import get_db
from app.models.scan import ScanRecord
from app.models.image import ScanImage
from app.schemas.image import ImageUploadResponse, FuelEstimationData
from app.services.image_service import ImageService
from app.services.fuel_estimation_service import FuelEstimationService
from app.utils.validators import validate_image_type
from app.utils.file_handler import validate_image_file
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/upload", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    scan_id: int = Form(...),
    image_type: str = Form(...),
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    captured_at: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    estimate_fuel: Optional[bool] = Form(True),  # Enable fuel estimation by default
    db: Session = Depends(get_db)
):
    """
    Upload an image for a scan
    
    If estimate_fuel is True and image_type is 'visible', automatically estimates fuel load
    """
    # Validate file
    validate_image_file(file)
    
    # Validate image type
    image_type = validate_image_type(image_type)
    
    # Verify scan exists
    scan = db.query(ScanRecord).filter(ScanRecord.id == scan_id).first()
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    # Save image file
    image_service = ImageService()
    file_info = await image_service.save_image(file, scan_id, image_type)
    
    # Parse metadata if provided
    metadata_dict = None
    if metadata:
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            pass
    
    # Parse captured_at
    captured_datetime = None
    if captured_at:
        try:
            captured_datetime = datetime.fromisoformat(captured_at.replace('Z', '+00:00'))
        except ValueError:
            pass
    
    # Create database record
    scan_image = ScanImage(
        scan_id=scan_id,
        image_type=image_type,
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"],
        width=file_info["width"],
        height=file_info["height"],
        latitude=latitude,
        longitude=longitude,
        captured_at=captured_datetime,
        metadata=metadata_dict
    )
    
    db.add(scan_image)
    db.commit()
    db.refresh(scan_image)
    
    # Perform fuel estimation if requested and image is visible type
    fuel_estimation_data = None
    if estimate_fuel and image_type == "visible":
        try:
            logger.info(f"Starting fuel estimation for image {scan_image.id}")
            fuel_service = FuelEstimationService()
            estimation_result = fuel_service.estimate_fuel_load(file_info["file_path"])
            
            if estimation_result.get("success"):
                logger.info(f"Fuel estimation successful: {estimation_result}")
                
                # Update scan record with fuel estimation data
                scan.fuel_load = estimation_result.get("total_fuel_load")
                scan.one_hour_fuel = estimation_result.get("one_hour_fuel")
                scan.ten_hour_fuel = estimation_result.get("ten_hour_fuel")
                scan.hundred_hour_fuel = estimation_result.get("hundred_hour_fuel")
                scan.pine_cone_count = estimation_result.get("pine_cone_count")
                
                db.commit()
                db.refresh(scan)
                
                # Prepare fuel estimation data for response
                fuel_estimation_data = FuelEstimationData(
                    total_fuel_load=estimation_result.get("total_fuel_load"),
                    one_hour_fuel=estimation_result.get("one_hour_fuel"),
                    ten_hour_fuel=estimation_result.get("ten_hour_fuel"),
                    hundred_hour_fuel=estimation_result.get("hundred_hour_fuel"),
                    pine_cone_count=estimation_result.get("pine_cone_count")
                )
            else:
                logger.warning(f"Fuel estimation failed: {estimation_result.get('error')}")
        
        except Exception as e:
            # Log the error but don't fail the image upload
            logger.error(f"Error during fuel estimation: {str(e)}", exc_info=True)
    
    return ImageUploadResponse(
        image_id=scan_image.id,
        file_path=file_info["file_path"],
        url=f"/api/images/{scan_image.id}",
        fuel_estimation=fuel_estimation_data
    )


@router.get("/{image_id}")
async def get_image(image_id: int, db: Session = Depends(get_db)):
    """Get image file by ID"""
    image = db.query(ScanImage).filter(ScanImage.id == image_id).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    if not os.path.exists(image.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image file not found on disk"
        )
    
    return FileResponse(
        image.file_path,
        media_type=image.mime_type or "image/jpeg"
    )
