# Fuel Load Estimation API Guide

Complete guide for automatically processing images and obtaining fuel load estimates using the integrated web scraping API.

---

## Quick Start - Test in Terminal

### Method 1: Using Python Script (Recommended for Windows)

```bash
# Step 1: Start the backend server (in terminal 1)
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

# Step 2: Use Python test script (in terminal 2)
cd test
..\backend\venv\Scripts\python.exe upload_test.py

# The script will automatically upload the image and display results
```

### Method 2: Using cURL (Linux/Mac or Git Bash on Windows)

```bash
# Step 1: Start the backend server (in terminal 1)
cd backend
python -m uvicorn app.main:app --reload

# Step 2: Upload a test image (in terminal 2)
cd backend
curl -X POST http://localhost:8000/api/images/upload \
  -F "file=@test/02.jpg" \
  -F "scan_id=1" \
  -F "image_type=visible"

# Response will show: {"image_id": 1}

# Step 3: Estimate fuel load
curl -X POST http://localhost:8000/api/images/1/estimate-fuel

# Response will show fuel estimation results after ~30-60 seconds
```

**Note for Windows PowerShell Users**: PowerShell's `curl` is an alias for `Invoke-WebRequest` and doesn't support standard curl syntax. Use the Python script method instead (see `test/upload_test.py`).

### Method 2: Using Python Script (Batch Processing)

```bash
# Step 1: Create test directory and add images
cd backend
mkdir test_images
# Place your test images (.jpg, .png) in backend/test_images/

# Step 2: Create and run test script
# Copy the test_fuel_estimation.py script from this guide (see section below)
# Then run:
python test_fuel_estimation.py

# The script will automatically:
# - Upload all images in test_images/
# - Call fuel estimation API for each
# - Display results and summary
```

### Expected Timeline

- **Image Upload**: 1-2 seconds
- **Fuel Estimation**: 30-60 seconds per image
- **Total**: ~35-65 seconds per image

### Immediate Test

If you have test images in `E:\launch project\pyroscope_dashboard\test\`, run:

```bash
# Navigate to backend
cd "E:\launch project\pyroscope_dashboard\backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Make sure backend is running in another terminal, then:
curl -X POST http://localhost:8000/api/images/upload \
  -F "file=@../test/image1.jpg" \
  -F "scan_id=1" \
  -F "image_type=visible"

# Note the returned image_id, then:
curl -X POST http://localhost:8000/api/images/1/estimate-fuel
```

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Testing with Images](#testing-with-images)
- [Response Format](#response-format)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

---

## 🔍 Overview

The Fuel Load Estimation API automatically processes images through an external web service to estimate fuel loads. The system uses Selenium WebDriver to interact with the [WFAS (Wildland Fire Assessment System)](https://www.wfas.net/nfdr-fuel-moisture/) website.

### What it Does

1. **Uploads images** to the WFAS fuel moisture calculator
2. **Extracts results** including:
   - Total fuel load (tons/acre)
   - 1-hour fuel load
   - 10-hour fuel load
   - 100-hour fuel load
   - Pine cone count
3. **Updates database** with estimation results
4. **Returns structured data** for frontend display

### Technology Stack

- **Selenium WebDriver**: Browser automation
- **webdriver-manager**: Automatic driver management
- **httpx**: HTTP client for file operations
- **FastAPI**: API endpoint handling

---

## ✅ Prerequisites

### 1. Install Required Dependencies

The fuel estimation dependencies are already in `requirements.txt`:

```txt
selenium>=4.15.0
webdriver-manager>=4.0.1
httpx>=0.25.0
```

Install them:

```bash
cd backend
pip install selenium webdriver-manager httpx
```

### 2. Chrome Browser

**Required**: Google Chrome must be installed on your system.

- **Windows**: Download from https://www.google.com/chrome/
- **Linux**: `sudo apt-get install google-chrome-stable`
- **Mac**: Download from https://www.google.com/chrome/

### 3. Internet Connection

The API requires internet access to communicate with the WFAS website.

---

## ⚙️ Configuration

### Environment Variables

Configure the fuel estimation API in your `.env` file:

```env
# Fuel Estimation Configuration
FUEL_ESTIMATION_API_URL=https://www.wfas.net/nfdr-fuel-moisture/
FUEL_ESTIMATION_TIMEOUT=60
FUEL_ESTIMATION_HEADLESS=True
```

**Parameters:**

- `FUEL_ESTIMATION_API_URL`: The WFAS website URL
- `FUEL_ESTIMATION_TIMEOUT`: Maximum wait time (seconds) for results
- `FUEL_ESTIMATION_HEADLESS`: Run browser in headless mode (True/False)

### Headless vs GUI Mode

**Headless Mode (Recommended):**
```env
FUEL_ESTIMATION_HEADLESS=True
```
- Faster execution
- No visible browser window
- Suitable for production

**GUI Mode (Debugging):**
```env
FUEL_ESTIMATION_HEADLESS=False
```
- Shows browser window
- Useful for troubleshooting
- See what's happening in real-time

### Valid Image Types

When uploading images, you must specify one of these **four valid image types**:

- **`thermal`** - Thermal/infrared images
- **`visible`** - Visible light/RGB images (most common)
- **`panorama`** - Panoramic view images
- **`detail`** - Close-up detail images

❌ **Invalid types** (will return 400 error): `topdown`, `overhead`, `aerial`, etc.

Example:
```bash
# ✅ Correct
-F "image_type=visible"

# ❌ Wrong
-F "image_type=topdown"
```

---

## 🔌 API Endpoints

### Upload Image and Estimate Fuel Load

```http
POST /images/{image_id}/estimate-fuel
```

**Description**: Process an uploaded image and return fuel load estimates.

**Path Parameters:**
- `image_id` (integer): ID of the uploaded image in database

**Response**: `FuelEstimationResult`

```json
{
  "success": true,
  "total_fuel_load": 0.325,
  "one_hour_fuel": 0.025,
  "ten_hour_fuel": 0.100,
  "hundred_hour_fuel": 0.200,
  "pine_cone_count": 15,
  "error": null
}
```

---

## 💻 Usage Examples

### Example 1: Basic Usage with cURL

```bash
# Upload an image first
curl -X POST http://localhost:8000/api/images/upload \
  -F "file=@path/to/image.jpg" \
  -F "scan_id=1" \
  -F "image_type=visible"

# Response will include image_id, e.g., {"image_id": 1}

# Estimate fuel load
curl -X POST http://localhost:8000/api/images/1/estimate-fuel
```

### Example 2: Python Script

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api"
IMAGE_PATH = "test/image.jpg"
SCAN_ID = 1

# Step 1: Upload image
with open(IMAGE_PATH, 'rb') as f:
    files = {'file': f}
    data = {'scan_id': SCAN_ID, 'image_type': 'visible'}
    response = requests.post(f"{BASE_URL}/images/upload", files=files, data=data)
    image_id = response.json()['image_id']
    print(f"Image uploaded: ID = {image_id}")

# Step 2: Estimate fuel load
response = requests.post(f"{BASE_URL}/images/{image_id}/estimate-fuel")
result = response.json()

print(f"Success: {result['success']}")
print(f"Total Fuel Load: {result['total_fuel_load']} tons/acre")
print(f"1-Hour Fuel: {result['one_hour_fuel']} tons/acre")
print(f"10-Hour Fuel: {result['ten_hour_fuel']} tons/acre")
print(f"100-Hour Fuel: {result['hundred_hour_fuel']} tons/acre")
print(f"Pine Cones: {result['pine_cone_count']}")
```

### Example 3: JavaScript/Node.js

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const BASE_URL = 'http://localhost:8000/api';
const IMAGE_PATH = 'test/image.jpg';

async function estimateFuelLoad() {
  // Step 1: Upload image
  const formData = new FormData();
  formData.append('file', fs.createReadStream(IMAGE_PATH));
  formData.append('scan_id', '1');
  formData.append('image_type', 'visible');
  
  const uploadResponse = await axios.post(
    `${BASE_URL}/images/upload`,
    formData,
    { headers: formData.getHeaders() }
  );
  
  const imageId = uploadResponse.data.image_id;
  console.log(`Image uploaded: ID = ${imageId}`);
  
  // Step 2: Estimate fuel load
  const estimateResponse = await axios.post(
    `${BASE_URL}/images/${imageId}/estimate-fuel`
  );
  
  const result = estimateResponse.data;
  console.log('Estimation Results:');
  console.log(`Total Fuel Load: ${result.total_fuel_load} tons/acre`);
  console.log(`1-Hour Fuel: ${result.one_hour_fuel} tons/acre`);
  console.log(`10-Hour Fuel: ${result.ten_hour_fuel} tons/acre`);
  console.log(`100-Hour Fuel: ${result.hundred_hour_fuel} tons/acre`);
  console.log(`Pine Cones: ${result.pine_cone_count}`);
}

estimateFuelLoad();
```

---

## 🧪 Testing with Images

### Prepare Test Images

1. **Create test directory:**
```bash
mkdir -p backend/test_images
```

2. **Place test images:**
```
backend/test_images/
├── sample1.jpg
├── sample2.jpg
└── sample3.jpg
```

### Batch Processing Script

Create `backend/test_fuel_estimation.py`:

```python
"""
Test script for batch fuel estimation
"""
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api"
TEST_DIR = Path("test_images")
SCAN_ID = 1

def process_image(image_path):
    """Process a single image and return results"""
    print(f"\n{'='*60}")
    print(f"Processing: {image_path.name}")
    print('='*60)
    
    # Upload image
    with open(image_path, 'rb') as f:
        files = {'file': (image_path.name, f, 'image/jpeg')}
        data = {'scan_id': SCAN_ID, 'image_type': 'visible'}
        
        try:
            response = requests.post(
                f"{BASE_URL}/images/upload",
                files=files,
                data=data
            )
            response.raise_for_status()
            image_id = response.json()['image_id']
            print(f"✓ Uploaded successfully (ID: {image_id})")
        except Exception as e:
            print(f"✗ Upload failed: {e}")
            return None
    
    # Estimate fuel load
    try:
        response = requests.post(
            f"{BASE_URL}/images/{image_id}/estimate-fuel",
            timeout=90
        )
        response.raise_for_status()
        result = response.json()
        
        if result['success']:
            print(f"✓ Estimation successful")
            print(f"  Total Fuel Load: {result['total_fuel_load']:.4f} tons/acre")
            print(f"  1-Hour Fuel: {result['one_hour_fuel']:.4f} tons/acre")
            print(f"  10-Hour Fuel: {result['ten_hour_fuel']:.4f} tons/acre")
            print(f"  100-Hour Fuel: {result['hundred_hour_fuel']:.4f} tons/acre")
            print(f"  Pine Cone Count: {result['pine_cone_count']}")
            return result
        else:
            print(f"✗ Estimation failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"✗ Estimation request failed: {e}")
        return None

def main():
    """Process all images in test directory"""
    if not TEST_DIR.exists():
        print(f"Error: Directory '{TEST_DIR}' not found")
        return
    
    # Find all image files
    image_files = list(TEST_DIR.glob("*.jpg")) + \
                  list(TEST_DIR.glob("*.jpeg")) + \
                  list(TEST_DIR.glob("*.png"))
    
    if not image_files:
        print(f"No image files found in '{TEST_DIR}'")
        return
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    results = []
    for image_path in image_files:
        result = process_image(image_path)
        if result:
            results.append({
                'filename': image_path.name,
                'result': result
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Total images: {len(image_files)}")
    print(f"Successful: {len(results)}")
    print(f"Failed: {len(image_files) - len(results)}")
    
    if results:
        print("\nResults:")
        for item in results:
            print(f"  {item['filename']}: {item['result']['total_fuel_load']:.4f} tons/acre")

if __name__ == "__main__":
    main()
```

### Run Batch Processing

```bash
cd backend

# Make sure backend is running in another terminal
# Then run the test script
python test_fuel_estimation.py
```

**Expected Output:**

```
Found 3 images to process

============================================================
Processing: sample1.jpg
============================================================
✓ Uploaded successfully (ID: 1)
✓ Estimation successful
  Total Fuel Load: 0.3250 tons/acre
  1-Hour Fuel: 0.0250 tons/acre
  10-Hour Fuel: 0.1000 tons/acre
  100-Hour Fuel: 0.2000 tons/acre
  Pine Cone Count: 15

============================================================
Processing: sample2.jpg
============================================================
✓ Uploaded successfully (ID: 2)
✓ Estimation successful
  Total Fuel Load: 0.2800 tons/acre
  ...

============================================================
SUMMARY
============================================================
Total images: 3
Successful: 3
Failed: 0

Results:
  sample1.jpg: 0.3250 tons/acre
  sample2.jpg: 0.2800 tons/acre
  sample3.jpg: 0.3100 tons/acre
```

---

## 📊 Response Format

### Success Response

```json
{
  "success": true,
  "total_fuel_load": 0.325,
  "one_hour_fuel": 0.025,
  "ten_hour_fuel": 0.100,
  "hundred_hour_fuel": 0.200,
  "pine_cone_count": 15,
  "error": null
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether estimation succeeded |
| `total_fuel_load` | float | Total fuel load (tons/acre) |
| `one_hour_fuel` | float | Fine fuels (1-hour timelag) |
| `ten_hour_fuel` | float | Small fuels (10-hour timelag) |
| `hundred_hour_fuel` | float | Medium fuels (100-hour timelag) |
| `pine_cone_count` | integer | Number of pine cones detected |
| `error` | string/null | Error message if failed |

### Error Response

```json
{
  "success": false,
  "total_fuel_load": null,
  "one_hour_fuel": null,
  "ten_hour_fuel": null,
  "hundred_hour_fuel": null,
  "pine_cone_count": null,
  "error": "Failed to extract results from website"
}
```

**Common Error Messages:**

- `"Image file not found"` - Image doesn't exist in database
- `"Failed to upload image to website"` - Network/upload issue
- `"Timeout waiting for results"` - Processing took too long
- `"Failed to extract results from website"` - Parsing error
- `"WebDriver initialization failed"` - Browser/driver issue

---

## 🔧 Troubleshooting

### Issue 1: WebDriver Not Found

**Error:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Solution:**
```bash
# The webdriver-manager should handle this automatically
# If it doesn't work, manually install:
pip install --upgrade webdriver-manager
```

### Issue 2: Chrome Not Installed

**Error:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX
```

**Solution:**
1. Install/Update Google Chrome
2. Restart your computer
3. Try again

### Issue 3: Timeout Errors

**Error:**
```
"error": "Timeout waiting for results"
```

**Solutions:**

1. **Increase timeout:**
```env
FUEL_ESTIMATION_TIMEOUT=120  # Increase to 120 seconds
```

2. **Check internet connection:**
```bash
ping www.wfas.net
```

3. **Test in GUI mode:**
```env
FUEL_ESTIMATION_HEADLESS=False
```

### Issue 4: Image Upload Fails

**Error:**
```
"error": "Failed to upload image to website"
```

**Solutions:**

1. **Check image format:**
   - Supported: JPEG, PNG
   - Max size: Usually 10MB
   
2. **Verify image is valid:**
```python
from PIL import Image
img = Image.open("test.jpg")
print(img.format, img.size)  # Should show: JPEG (width, height)
```

3. **Check file permissions:**
```bash
ls -la backend/uploads/
```

### Issue 5: Missing email-validator Module

**Error:**
```
ImportError: email-validator is not installed, run `pip install 'pydantic[email]'`
```

**Solution:**
```bash
# Activate virtual environment first
cd backend
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Install missing dependency
pip install email-validator

# Restart backend
python -m uvicorn app.main:app --reload
```

### Issue 6: PowerShell cURL Command Not Working

**Error:**
```
Invoke-WebRequest : A parameter cannot be found that matches parameter name 'X'
```

**Cause**: PowerShell's `curl` is an alias for `Invoke-WebRequest` and doesn't support standard curl syntax.

**Solution - Use Python Script:**
```bash
# Create test script if not exists
cd test
..\backend\venv\Scripts\python.exe upload_test.py
```

**Alternative - Use Invoke-WebRequest:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/images/upload" `
  -Method Post `
  -Form @{
    file = Get-Item -Path "..\test\02.jpg"
    scan_id = "1"
    image_type = "visible"
  }
```

### Issue 7: Results Not Parsing

**Error:**
```
"error": "Failed to extract results from website"
```

**Possible Causes:**
1. Website structure changed
2. Unexpected response format
3. Website is down

**Debug Steps:**

1. **Run in GUI mode** to see what's happening:
```env
FUEL_ESTIMATION_HEADLESS=False
```

2. **Check service code:**
```python
# backend/app/services/fuel_estimation_service.py
# Add debugging logs
print(f"Page source: {driver.page_source[:500]}")
```

3. **Verify website is accessible:**
```bash
curl -I https://www.wfas.net/nfdr-fuel-moisture/
```

---

## 🚀 Advanced Usage

### Automatic Fuel Estimation on Upload

Modify the upload endpoint to automatically trigger estimation:

```python
# backend/app/routers/images.py

@router.post("/upload-and-estimate")
async def upload_and_estimate(
    file: UploadFile = File(...),
    scan_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Upload image and automatically estimate fuel load"""
    
    # Upload image
    image = await ImageService.upload_image(db, file, scan_id, "topdown")
    
    # Estimate fuel load
    result = FuelEstimationService.estimate_fuel_load(image.id, db)
    
    return {
        "image_id": image.id,
        "estimation": result
    }
```

### Batch Processing with Queue

For production, use a task queue (e.g., Celery):

```python
# backend/tasks.py
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def estimate_fuel_load_async(image_id: int):
    """Background task for fuel estimation"""
    db = SessionLocal()
    try:
        result = FuelEstimationService.estimate_fuel_load(image_id, db)
        return result
    finally:
        db.close()
```

### Custom Result Processing

```python
def process_estimation_result(result):
    """Process and classify fuel load estimation"""
    if not result['success']:
        return {"risk_level": "unknown", "message": result['error']}
    
    total = result['total_fuel_load']
    
    # Classify risk based on total fuel load
    if total < 0.2:
        risk = "low"
    elif total < 0.35:
        risk = "medium"
    else:
        risk = "high"
    
    return {
        "risk_level": risk,
        "total_fuel": total,
        "breakdown": {
            "fine": result['one_hour_fuel'],
            "small": result['ten_hour_fuel'],
            "medium": result['hundred_hour_fuel']
        }
    }
```

---

## 📈 Performance Considerations

### Timing Expectations

- **Image Upload**: ~1-2 seconds
- **Fuel Estimation**: ~30-60 seconds
- **Total Process**: ~35-65 seconds per image

### Optimization Tips

1. **Use Headless Mode** in production:
```env
FUEL_ESTIMATION_HEADLESS=True
```

2. **Process Multiple Images in Parallel**:
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_image, img) for img in images]
    results = [f.result() for f in futures]
```

3. **Cache Results** to avoid re-processing:
```python
# Check if estimation already exists
existing = db.query(ScanRecord).filter(
    ScanRecord.id == scan_id,
    ScanRecord.fuel_load.isnot(None)
).first()

if existing:
    return existing.fuel_load  # Use cached result
```

---

## 📝 Best Practices

1. **Always validate images before upload**
2. **Set reasonable timeouts** (60-120 seconds)
3. **Log all estimation attempts** for debugging
4. **Handle errors gracefully** and retry if appropriate
5. **Use headless mode** in production
6. **Monitor API usage** to avoid rate limiting
7. **Store raw images** for manual verification if needed

---

## 🔗 Related Documentation

- [Main README](./README.md)
- [API Documentation](./docs/API.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)

---

**Last Updated**: February 17, 2026

**Version**: 1.0.0

**Status**: Production Ready ✅
