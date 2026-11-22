import os
import sys
import io
import time
import socket
import urllib.parse
from pathlib import Path
import threading
import webbrowser

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aiofiles
import qrcode

PORT = 5321
UPLOAD_DIR = Path.home() / "Downloads" / "iPhone_Transfers"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = '127.0.0.1'
    finally:
        s.close()
    return ip

LAN_IP = get_lan_ip()
SERVER_URL = f"http://{LAN_IP}:{PORT}"

app = FastAPI(title="AirTransfer - iPhone to Laptop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_unique_filename(filename: str) -> Path:
    safe_name = Path(filename).name
    if not safe_name or safe_name in ('.', '..'):
        safe_name = f"transfer_{int(time.time())}"
    dest = UPLOAD_DIR / safe_name
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while True:
        candidate = UPLOAD_DIR / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1

@app.get("/api/info")
def get_info():
    return {
        "ip": LAN_IP,
        "port": PORT,
        "url": SERVER_URL,
        "upload_dir": str(UPLOAD_DIR)
    }

@app.get("/api/qr")
def get_qr_image():
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2,
    )
    qr.add_data(SERVER_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved = []
    chunk_size = 1024 * 1024  # 1MB buffer for fast streaming
    for file in files:
        if not file.filename:
            continue
        dest = get_unique_filename(file.filename)
        total_bytes = 0
        async with aiofiles.open(dest, "wb") as out_f:
            while chunk := await file.read(chunk_size):
                await out_f.write(chunk)
                total_bytes += len(chunk)
        saved.append({
            "name": dest.name,
            "size": total_bytes
        })
    return {"success": True, "saved": saved, "count": len(saved)}

@app.get("/api/files")
def list_files():
    items = []
    if UPLOAD_DIR.exists():
        for p in UPLOAD_DIR.iterdir():
            if p.is_file():
                st = p.stat()
                items.append({
                    "name": p.name,
                    "size": st.st_size,
                    "modified": st.st_mtime,
                    "url": f"/api/download/{urllib.parse.quote(p.name)}"
                })
    items.sort(key=lambda x: x["modified"], reverse=True)
    return {"files": items, "count": len(items)}

@app.get("/api/download/{filename}")
def download_file(filename: str):
    safe_name = Path(filename).name
    file_path = UPLOAD_DIR / safe_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=str(file_path),
        filename=safe_name,
        media_type="application/octet-stream"
    )

@app.post("/api/open-folder")
def open_folder():
    try:
        os.startfile(str(UPLOAD_DIR))
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/", response_class=HTMLResponse)
def index():
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>AirTransfer Server Running</h1>"

def print_banner():
    qr = qrcode.QRCode(border=1)
    qr.add_data(SERVER_URL)
    qr.make(fit=True)
    
    print("\n" + "=" * 60)
    print("   🚀 AIRTRANSFER - iPHONE TO LAPTOP WI-FI DROP")
    print("=" * 60)
    print(f"  * Status       : RUNNING & READY")
    print(f"  * Laptop IP    : {LAN_IP}")
    print(f"  * iPhone Link  : {SERVER_URL}")
    print(f"  * Saving to    : {UPLOAD_DIR}")
    print("-" * 60)
    print("  📱 SCAN THIS QR CODE WITH YOUR iPHONE CAMERA:")
    print("-" * 60)
    try:
        qr.print_ascii(invert=True)
    except Exception:
        pass
    print("-" * 60)
    print(f"  Or simply open Safari on iPhone and type: {SERVER_URL}")
    print("  (Make sure iPhone and Laptop are on the SAME Wi-Fi)")
    print("=" * 60 + "\n")

def open_laptop_browser():
    time.sleep(1.2)
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

if __name__ == "__main__":
    if is_port_in_use(PORT):
        print("\n" + "=" * 60)
        print("   AIRTRANSFER SERVER ALREADY RUNNING")
        print("=" * 60)
        print(f"  * Local Link   : http://localhost:{PORT}")
        print(f"  * Remote Link  : {SERVER_URL}")
        print("  Opening browser window...")
        print("=" * 60 + "\n")
        webbrowser.open(f"http://localhost:{PORT}")
        time.sleep(1)
        sys.exit(0)

    print_banner()
    threading.Thread(target=open_laptop_browser, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")

