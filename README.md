# YfileTransfer - Simple Computer to Android File Transfer

A lightweight, local network file transfer solution that allows you to quickly transfer files from your computer (Mac, Windows, or Linux) to your Android phone without using cloud services.

## Features

- 🚀 **Fast & Direct**: Transfer files over your local Wi-Fi network
- 📱 **Mobile-Friendly**: Beautiful web interface optimized for Android phones
- 📷 **QR Code**: Easy connection via QR code scanning
- 🎨 **Modern UI**: Clean, responsive design
- 🔒 **Local Only**: Files never leave your network
- ⚡ **No Setup**: Just run and go!

## Requirements

- Python 3.6 or higher
- Computer (Mac, Windows, or Linux) and Android device on the same Wi-Fi network

## Installation on Another Computer

### Step 1: Copy Files to the Other Computer

You can transfer the application files to another computer using:
- USB drive
- Network share
- Cloud storage (Google Drive, Dropbox, etc.)
- Email (zip the folder)

**Files needed:**
- `server.py`
- `requirements.txt`
- `start.sh` (for Mac/Linux) or `start.bat` (for Windows)
- `README.md` (optional, for reference)

### Step 2: Install Python (if not already installed)

- **Windows**: Download from [python.org](https://www.python.org/downloads/) - make sure to check "Add Python to PATH" during installation
- **Linux**: Usually pre-installed, or install via package manager:
  ```bash
  sudo apt-get install python3 python3-pip  # Debian/Ubuntu
  sudo yum install python3 python3-pip      # RedHat/CentOS
  ```
- **Mac**: Usually pre-installed, or install via Homebrew: `brew install python3`

### Step 3: Install Dependencies

**On Mac/Linux:**
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**On Windows:**
```cmd
REM Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
```

> **Note**: On macOS and some Linux systems, you may need to use `pip3` instead of `pip`, or create a virtual environment to avoid system package conflicts.

## Usage

### Basic Usage

**On Mac/Linux:**

1. **Activate the virtual environment** (if you created one):
```bash
source venv/bin/activate
```

2. **Start the server**:
```bash
python3 server.py
```

Or use the convenience script:
```bash
./start.sh
```

**On Windows:**

1. **Activate the virtual environment** (if you created one):
```cmd
venv\Scripts\activate
```

2. **Start the server**:
```cmd
python server.py
```

Or use the convenience script:
```cmd
start.bat
```

### Transfer Files

1. **Add files to transfer**:
   - Add files you want to transfer to the `YfileTransfer` directory
   - Or specify a custom directory (see below)
   - The server will automatically detect and list them

2. **Access from Android**:
   - Make sure your computer and Android phone are on the **same Wi-Fi network**
   - Open your Android phone's browser
   - Enter the URL shown in the terminal (e.g., `http://192.168.1.100:8000`)
   - Or scan the QR code that was generated (`qr_code.png`)
   - Select files and click "Download" or "Download selected"

### Custom Directory

To serve files from a different directory:

**Mac/Linux:**
```bash
python3 server.py /path/to/your/files
```

**Windows:**
```cmd
python server.py C:\path\to\your\files
```

## How It Works

1. The server starts a local HTTP server on your computer (port 8000 by default)
2. It detects your computer's local IP address on your Wi-Fi network
3. You access the server from your Android phone's browser using that IP address
4. Files are transferred directly over your local network - no internet required!

## Troubleshooting

### Can't connect from Android phone?

- ✅ Make sure both devices are on the **same Wi-Fi network**
- ✅ Check that your computer's firewall isn't blocking port 8000
  - **Windows**: Check Windows Firewall settings
  - **Mac**: System Settings → Network → Firewall
  - **Linux**: Check `iptables` or `ufw` settings
- ✅ Try accessing the URL directly in your Android browser
- ✅ Verify the IP address shown in the terminal matches your computer's network IP
- ✅ Make sure the server is actually running (check the terminal output)

### Port already in use?

If port 8000 is already in use, you can modify the `port` variable in `server.py` to use a different port.

### QR code not generating?

Make sure `qrcode[pil]` is installed. You can still access the server manually by typing the URL in your browser.

## Security Note

This server is designed for local network use only. It's not secure for use over the internet. Only use it on trusted local networks.

## License

Free to use and modify for personal use.

