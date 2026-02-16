"""
Test script for Fuel Estimation Service
Tests the integration with Wildlands AI fuel estimation API
"""
import os
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.fuel_estimation_service import FuelEstimationService
from app.config import settings


def test_fuel_estimation():
    """Test fuel estimation with a sample image"""
    print("=" * 60)
    print("Fuel Estimation Service Test")
    print("=" * 60)
    
    # Check configuration
    print("\n📋 Configuration:")
    print(f"  API URL: {settings.FUEL_ESTIMATION_API_URL}")
    print(f"  Timeout: {settings.FUEL_ESTIMATION_TIMEOUT}s")
    print(f"  Headless Mode: {settings.FUEL_ESTIMATION_HEADLESS}")
    
    # Check if test image exists (using user's provided image)
    test_image_paths = [
        r"C:\Users\lenovo\.cursor\projects\d-Launch-Project-backend\assets\c__Users_lenovo_AppData_Roaming_Cursor_User_workspaceStorage_f8d6fe62b2204b08bde05d08ceb2f6a4_images_image-17eb065c-1059-4520-b407-8df50a0d5300.png",
        r"C:\Users\lenovo\.cursor\projects\d-Launch-Project-backend\assets\c__Users_lenovo_AppData_Roaming_Cursor_User_workspaceStorage_f8d6fe62b2204b08bde05d08ceb2f6a4_images_image-8717c079-3fa2-455c-bf2b-34a24920330a.png"
    ]
    
    test_image = None
    for path in test_image_paths:
        if os.path.exists(path):
            test_image = path
            break
    
    if not test_image:
        print("\n❌ Error: No test image found!")
        print("Please provide a test image path.")
        return False
    
    print(f"\n📷 Test Image: {test_image}")
    print(f"  File exists: ✓")
    print(f"  File size: {os.path.getsize(test_image) / 1024:.2f} KB")
    
    # Initialize service
    print("\n🔧 Initializing Fuel Estimation Service...")
    service = FuelEstimationService()
    
    # Perform estimation
    print("\n🚀 Starting fuel estimation...")
    print("  (This may take 30-60 seconds...)")
    print("  ⏳ Please wait...")
    
    try:
        result = service.estimate_fuel_load(test_image)
        
        print("\n" + "=" * 60)
        print("📊 Estimation Results:")
        print("=" * 60)
        
        if result.get("success"):
            print("\n✅ Estimation Successful!\n")
            
            # Display results
            if result.get("total_fuel_load") is not None:
                print(f"  🔥 Total Fuel Load:     {result['total_fuel_load']:.3f} tons/acre")
            
            if result.get("one_hour_fuel") is not None:
                print(f"  ⏱️  1-Hour Fuel:         {result['one_hour_fuel']:.3f} tons/acre")
            
            if result.get("ten_hour_fuel") is not None:
                print(f"  ⏱️  10-Hour Fuel:        {result['ten_hour_fuel']:.3f} tons/acre")
            
            if result.get("hundred_hour_fuel") is not None:
                print(f"  ⏱️  100-Hour Fuel:       {result['hundred_hour_fuel']:.3f} tons/acre")
            
            if result.get("pine_cone_count") is not None:
                print(f"  🌲 Pine Cone Count:     {result['pine_cone_count']}")
            
            print("\n" + "=" * 60)
            return True
        else:
            print("\n❌ Estimation Failed!")
            print(f"  Error: {result.get('error', 'Unknown error')}")
            print("\n" + "=" * 60)
            return False
    
    except Exception as e:
        print("\n❌ Exception occurred!")
        print(f"  Error: {str(e)}")
        print("\n" + "=" * 60)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("\n🧪 Testing Fuel Estimation Integration\n")
    
    # Run test
    success = test_fuel_estimation()
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✅ Test Completed Successfully!")
    else:
        print("❌ Test Failed!")
    print("=" * 60 + "\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
