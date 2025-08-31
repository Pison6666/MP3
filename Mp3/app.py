from flask import Flask, request, render_template_string, send_from_directory
from downloader import start_download, DOWNLOAD_FOLDER
import os

app = Flask(__name__)

# HTML template สำหรับหน้าเว็บ
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Downloader</title>
    <style>
        body { font-family: sans-serif; background: #282c34; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #3c4049; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center; }
        h1 { margin-top: 0; }
        input[type="text"] { width: 90%; padding: 10px; margin-bottom: 1rem; border-radius: 5px; border: 1px solid #666; background: #282c34; color: white; }
        button { padding: 10px 20px; border: none; border-radius: 5px; background-color: #1DB954; color: white; font-size: 16px; cursor: pointer; }
        .message { margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Music Downloader 🎧</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Paste YouTube or Spotify URL" required>
            <br>
            <button type="submit">Download</button>
        </form>
        <div class="message">
            {% if message %}
                <p>{{ message }}</p>
            {% endif %}
            {% if file_path %}
                <p>Download complete! <a href="/downloads/{{ file_name }}" download>Click here to download</a></p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    file_path = None
    file_name = None
    if request.method == 'POST':
        url = request.form['url']
        message = f"Processing link: {url}"
        downloaded_file_path = start_download(url)
        if downloaded_file_path:
            file_name = os.path.basename(downloaded_file_path)
            file_path = downloaded_file_path
            message = "Success!"
        else:
            message = "Failed to download. Please check the URL or console for errors."

    return render_template_string(HTML_TEMPLATE, message=message, file_path=file_path, file_name=file_name)

@app.route('/downloads/<filename>')
def downloaded_file(filename):
    """ทำให้ไฟล์ที่ดาวน์โหลดแล้วสามารถกดลิงก์โหลดได้"""
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    # ทำให้เข้าจากมือถือในวง LAN เดียวกันได้
    app.run(host='0.0.0.0', port=5000, debug=True)