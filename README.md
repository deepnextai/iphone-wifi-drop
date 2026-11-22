# ⚡ AirTransfer

> **High-speed, local Wi-Fi file sharing between iPhone and Windows PC — No third-party apps, cables, or cloud storage required.**

---

## 🌟 Key Highlights

- 📱 **Zero App on iPhone**: Connects directly through Apple Safari via a single QR code scan.
- 🔒 **100% Offline & Private**: Works completely on your local network. Your data never leaves your devices or goes to external servers.
- 🚀 **Full Local Network Speed**: Uses your home Wi-Fi router bandwidth (25–50+ MB/s) without consuming internet data.
- 🎥 **Original Resolution**: Preserves 100% full-resolution photos (`.HEIC` / `.JPG`) and high-bitrate 4K HDR videos (`.MOV`).
- 🔄 **Bi-directional Sharing**: Send media from iPhone to PC, or browse and download PC files directly to your iPhone.
- 📈 **Real-Time Transfer Metrics**: Live upload progress bar with transfer rate (MB/s) and byte counters.
- 🖵 **One-Click Windows Launcher**: Pre-configured desktop launcher with automatic LAN IP detection and terminal QR code.

---

## 🔒 Security & Complete Privacy

- **Strictly Local Network (Offline)**: All data travels directly between your iPhone and PC across your local Wi-Fi router. Internet access is not even required.
- **Zero Third-Party Cloud**: No external servers, no cloud storage, and no middleman. Your personal photos, videos, and files never leave your physical devices.
- **Zero Analytics & Telemetry**: No tracking scripts, external CDN calls, or user logging. Everything runs standalone on your machine.
- **Direct Local Storage**: Files are saved directly to your local PC storage (`Downloads/iPhone_Transfers`) without temporary cloud caching.

---

## 📂 Project Architecture

```
ios_drop/
├── server.py              # FastAPI streaming server with auto-LAN discovery
├── index.html             # Glassmorphism mobile-first web app (iOS design)
├── Start-AirTransfer.bat  # One-click Windows launcher
├── requirements.txt       # Minimal dependencies
├── verify_app.py          # End-to-end automated test suite
└── README.md              # Project documentation
```

---

## 🛠️ Prerequisites

- **Operating System**: Windows 10 or 11
- **Python**: Version 3.10 or higher
- **Local Network**: Both iPhone and PC must be connected to the **same Wi-Fi network**

---

## 🚀 How to Install and Run

### Option 1: Quick Start (Recommended for Windows)

1. Clone or download this repository:
   ```bash
   git clone https://github.com/<your-username>/airtransfer.git
   cd airtransfer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Double-click **`Start-AirTransfer.bat`** to launch the server and open the web portal.

---

### Option 2: Manual Terminal Startup

```bash
# Navigate to the project directory
cd airtransfer

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

Upon startup, the console displays:
- Active LAN IP and port (e.g. `http://<your-local-ip>:5321`)
- An ASCII QR code in the terminal
- Automatically launches your browser to the local connection page

---

## 📱 How to Use

1. **Start the Server**: Run `server.py` or double-click `Start-AirTransfer.bat`.
2. **Scan the QR Code**: Open the default **Camera** app on your iPhone and point it at the QR code on your PC screen.
3. **Open the Portal**: Tap the yellow Safari prompt that appears.
4. **Send Files**:
   - Tap **"Photos & Videos"** to transfer media from your Photo Library.
   - Tap **"Browse Files"** to transfer documents or uncompressed raw camera clips.
5. **Access Your Files**: Received files are automatically saved to your PC at:
   ```
   C:\Users\<Your-Username>\Downloads\iPhone_Transfers
   ```
   *(You can also click "Open Folder on Laptop" right from the web page).*

---

## 💡 Tips for iPhone Media Playback on Windows

- **High-Bitrate 4K / HDR Videos**: Modern iPhones record high-resolution media in 10-bit HEVC / HDR formats. For optimal playback on Windows, use **VLC Media Player** or any media player with HEVC support.
- **100% Uncompressed Video**: For massive 4K/60fps video clips, save the clip to the iPhone **Files** app first (`Share ➔ Save to Files`), then choose **"Browse Files"** in the web portal to bypass iOS Safari's default web-compression.

---

## 🧪 Automated Verification Suite

Run the built-in end-to-end tests to verify server endpoints, file uploading, and downloads:

```bash
python verify_app.py
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
