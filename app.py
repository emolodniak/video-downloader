import os
import logging
from flask import Flask, render_template_string, request, send_file, jsonify
import yt_dlp
from urllib.parse import urlparse
import tempfile
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Get PORT from environment (required for Render)
PORT = int(os.environ.get("PORT", 5000))

def is_valid_url(url):
    """Check if the provided URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_filename(filename):
    """Sanitize the filename to prevent issues."""
    return re.sub(r'[^\w\-_\. ]', '_', filename)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 50px;
            display: flex;
            justify-content: center;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
        }
        h2 {
            color: #333;
            text-align: center;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            margin: 15px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #4CAF50;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Video Downloader</h2>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Enter YouTube Video URL" required>
            <button type="submit">Download</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    """Handles video download."""
    video_url = request.form.get('url')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    if not is_valid_url(video_url):
        return jsonify({'error': 'Invalid URL format'}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)

                if not os.path.exists(filename):
                    return jsonify({'error': 'Download failed'}), 500
                
                safe_filename = sanitize_filename(os.path.basename(filename))

                return send_file(
                    filename,
                    as_attachment=True,
                    download_name=safe_filename
                )

    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Download failed: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
