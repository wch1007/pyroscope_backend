from pydantic import BaseModel
from typing import Optional


class FuelEstimationData(BaseModel):
    """Fuel estimation data returned with image upload"""
    total_fuel_load: Optional[float] = None
    one_hour_fuel: Optional[float] = None
    ten_hour_fuel: Optional[float] = None
    hundred_hour_fuel: Optional[float] = None
    pine_cone_count: Optional[int] = None


class ImageUploadResponse(BaseModel):
    image_id: int
    file_path: str
    url: str
    message: str = "Image uploaded successfully"
    fuel_estimation: Optional[FuelEstimationData] = None
