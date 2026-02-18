import requests

print("Testing connection...")
try:
    r = requests.get("http://localhost:8000/api/scans")
    print(f"API is working! Status: {r.status_code}")
    print("Now testing upload...")
    
    with open("02.jpg", "rb") as f:
        files = {"file": ("02.jpg", f, "image/jpeg")}
        data = {"scan_id": "1", "image_type": "visible"}
        r2 = requests.post("http://localhost:8000/api/images/upload", files=files, data=data)
        print(f"Upload status: {r2.status_code}")
        print(f"Response: {r2.json()}")
except Exception as e:
    print(f"Error: {e}")
