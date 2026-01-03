#!/usr/bin/env python3
"""
Simple file transfer server for Computer to Android transfer
Run this script on your computer (Mac, Windows, or Linux), then access it from your Android phone's browser

Uses Python's built-in HTTP server - no external dependencies except qrcode for QR code generation
"""

import os
import sys
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import qrcode
from io import BytesIO

class FileTransferHandler(SimpleHTTPRequestHandler):
    """Custom handler for file transfer with better UI"""
    
    def __init__(self, *args, directory=None, **kwargs):
        self.directory = directory or os.getcwd()
        super().__init__(*args, directory=self.directory, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        if parsed.path == '/' or parsed.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.generate_index().encode())
        else:
            # Serve files normally
            super().do_GET()
    
    def generate_index(self):
        """Generate HTML index page with file list"""
        files = []
        for item in sorted(os.listdir(self.directory)):
            item_path = os.path.join(self.directory, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                size_str = self.format_size(size)
                files.append({
                    'name': item,
                    'size': size_str,
                    'url': f'/{item}'
                })
        
        files_html = ''
        if files:
            files_html += '''
            <div class="bulk-actions">
                <button class="bulk-btn" onclick="selectAll(true)">Select all</button>
                <button class="bulk-btn secondary" onclick="selectAll(false)">Select none</button>
                <button class="bulk-btn primary" onclick="downloadSelected()">Download selected</button>
            </div>
            '''
            for file_info in files:
                files_html += f'''
                <div class="file-item">
                    <label class="check-wrap">
                        <input type="checkbox" class="file-check" value="{file_info['name']}">
                    </label>
                    <div class="file-info">
                        <span class="file-name">{file_info['name']}</span>
                        <span class="file-size">{file_info['size']}</span>
                    </div>
                    <a href="{file_info['url']}" class="download-btn" download>Download</a>
                </div>
                '''
        else:
            files_html = '<p class="no-files">No files found. Add files to this directory to transfer them.</p>'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Transfer</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .content {{
            padding: 30px;
        }}
        .file-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            margin-bottom: 10px;
            transition: all 0.3s;
            gap: 12px;
        }}
        .file-item:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        .file-info {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .file-name {{
            font-weight: 600;
            color: #333;
            word-break: break-all;
        }}
        .file-size {{
            font-size: 12px;
            color: #666;
        }}
        .download-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            white-space: nowrap;
        }}
        .download-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        .no-files {{
            text-align: center;
            color: #666;
            padding: 40px;
            font-size: 16px;
        }}
        .info-box {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #666;
        }}

        .bulk-actions {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 0 0 15px 0;
        }}
        .bulk-btn {{
            border: 1px solid #ddd;
            background: #fff;
            color: #333;
            padding: 10px 14px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
        }}
        .bulk-btn.secondary {{
            opacity: 0.85;
        }}
        .bulk-btn.primary {{
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }}
        .check-wrap {{
            display: flex;
            align-items: center;
            padding: 6px 6px;
        }}
        .file-check {{
            width: 18px;
            height: 18px;
            accent-color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 File Transfer</h1>
            <p>Select one file, or pick multiple and download one-by-one</p>
        </div>
        <div class="content">
            <div class="info-box">
                💡 <strong>Tip:</strong> Make sure your Mac and Android phone are on the same Wi-Fi network
            </div>
            {files_html}
        </div>
    </div>
    <script>
        function selectAll(on) {{
            document.querySelectorAll('.file-check').forEach(cb => cb.checked = on);
        }}

        function downloadSelected() {{
            const selected = Array.from(document.querySelectorAll('.file-check:checked')).map(cb => cb.value);
            if (!selected.length) {{
                alert('Select at least one file first.');
                return;
            }}
            // Trigger downloads sequentially (Android browsers may ignore rapid programmatic clicks)
            let i = 0;
            const btn = document.querySelector('.bulk-btn.primary');
            const original = btn ? btn.textContent : '';
            if (btn) btn.textContent = 'Downloading...';

            function next() {{
                if (i >= selected.length) {{
                    if (btn) btn.textContent = original || 'Download selected';
                    return;
                }}
                const name = selected[i++];
                const a = document.createElement('a');
                a.href = '/' + encodeURIComponent(name);
                a.download = name;
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                setTimeout(next, 700);
            }}
            next();
        }}
    </script>
</body>
</html>'''
    
    def format_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def log_message(self, format, *args):
        """Override to show cleaner logs"""
        print(f"[{self.address_string()}] {format % args}")


def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url):
    """Generate QR code for the URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Save QR code to file
    qr_path = os.path.join(os.path.dirname(__file__), 'qr_code.png')
    with open(qr_path, 'wb') as f:
        f.write(buffer.getvalue())
    return qr_path


def main():
    """Main function to start the server"""
    port = 8000
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Allow custom directory via command line argument
    if len(sys.argv) > 1:
        custom_dir = os.path.abspath(sys.argv[1])
        if os.path.isdir(custom_dir):
            directory = custom_dir
        else:
            print(f"Error: {custom_dir} is not a valid directory")
            sys.exit(1)
    
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}"
    
    # Create handler with directory
    handler = lambda *args, **kwargs: FileTransferHandler(*args, directory=directory, **kwargs)
    
    try:
        server = HTTPServer(('0.0.0.0', port), handler)
        
        print("\n" + "="*60)
        print("🚀 File Transfer Server Started!")
        print("="*60)
        print(f"📁 Serving directory: {directory}")
        print(f"🌐 Server URL: {url}")
        print(f"📱 Open this URL on your Android phone's browser")
        print("="*60)
        
        # Generate QR code
        try:
            qr_path = generate_qr_code(url)
            print(f"📷 QR Code saved to: {qr_path}")
            print(f"   Scan this QR code with your Android phone to open the URL")
        except Exception as e:
            print(f"⚠️  Could not generate QR code: {e}")
        
        print("\n💡 Tips:")
        print("   - Make sure your Mac and Android phone are on the same Wi-Fi")
        print("   - Add files to the directory to make them available for transfer")
        print("   - Press Ctrl+C to stop the server")
        print("="*60 + "\n")
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"\n❌ Error: Port {port} is already in use")
            print(f"   Try using a different port or stop the process using port {port}")
        else:
            print(f"\n❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

