from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

# Initialize Flask app
app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# Improved HTML with CSS for better visuals
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: #f4f4f4;
            margin: 0;
            padding: 50px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: auto;
        }
        h2 {
            color: #333;
        }
        input[type="text"] {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎥 YouTube Video Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter Video URL" required>
            <br>
            <button type="submit">Download</button>
        </form>
    </div>
</body>
</html>
"""

# Main page with a form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("url")
        if video_url:
            try:
                # Download options
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    filename = ydl.prepare_filename(info)  # Get file name

                return send_file(filename, as_attachment=True)  # Send file to user
            except Exception as e:
                return f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE)  # Show form using inline HTML

# Run Flask in production
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
