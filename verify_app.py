import sys
import io
from pathlib import Path
from starlette.testclient import TestClient

# Add directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from server import app, UPLOAD_DIR, PORT, LAN_IP

client = TestClient(app)

def test_all():
    print(f"[*] Testing with LAN_IP: {LAN_IP}, PORT: {PORT}")
    
    # 1. Test GET /
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "AirTransfer" in res.text, "AirTransfer not in response"
    print("  [+] GET / passed (HTML served correctly)")

    # 2. Test GET /api/info
    res = client.get("/api/info")
    assert res.status_code == 200
    data = res.json()
    assert data["ip"] == LAN_IP
    assert data["port"] == PORT
    assert "url" in data
    print(f"  [+] GET /api/info passed: {data['url']}")

    # 3. Test GET /api/qr
    res = client.get("/api/qr")
    assert res.status_code == 200
    assert res.headers["content-type"] == "image/png"
    assert len(res.content) > 100
    print("  [+] GET /api/qr passed (PNG generated successfully)")

    # 4. Test POST /api/upload with mock files (image + text)
    dummy_img = io.BytesIO(b"\xFF\xD8\xFF\xE0MockImageDataHere")
    dummy_text = io.BytesIO(b"Hello from iPhone transfer test!")
    files = [
        ("files", ("test_photo.jpg", dummy_img, "image/jpeg")),
        ("files", ("notes.txt", dummy_text, "text/plain")),
    ]
    res = client.post("/api/upload", files=files)
    assert res.status_code == 200, f"Upload failed: {res.text}"
    upload_data = res.json()
    assert upload_data["success"] is True
    assert upload_data["count"] == 2
    print(f"  [+] POST /api/upload passed: {upload_data['saved']}")

    # Verify files exist in UPLOAD_DIR
    file1 = UPLOAD_DIR / "test_photo.jpg"
    file2 = UPLOAD_DIR / "notes.txt"
    assert file1.exists(), "test_photo.jpg does not exist in UPLOAD_DIR"
    assert file2.exists(), "notes.txt does not exist in UPLOAD_DIR"
    print("  [+] Verified physical files created in UPLOAD_DIR")

    # 5. Test GET /api/files
    res = client.get("/api/files")
    assert res.status_code == 200
    files_list = res.json()
    assert files_list["count"] >= 2
    filenames = [f["name"] for f in files_list["files"]]
    assert "test_photo.jpg" in filenames
    assert "notes.txt" in filenames
    print(f"  [+] GET /api/files passed ({files_list['count']} files listed)")

    # 6. Test GET /api/download/{filename}
    res = client.get("/api/download/notes.txt")
    assert res.status_code == 200
    assert res.content == b"Hello from iPhone transfer test!"
    print("  [+] GET /api/download/notes.txt passed (file downloaded accurately)")

    print("\n[SUCCESS] ALL AIRTRANSFER TESTS PASSED 100%!")

if __name__ == "__main__":
    test_all()
