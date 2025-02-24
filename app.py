import os
import logging
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
from urllib.parse import urlparse
import tempfile
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
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
                'progress_hooks': [],
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
    app.run(host='0.0.0.0', port=5000, debug=True)
