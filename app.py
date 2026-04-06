from flask import Flask, request, send_file, render_template_string, jsonify
import yt_dlp
import os
import tempfile

app = Flask(__name__)

historial = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TikTok Downloader 🎀</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #ff9a9e, #fecfef);
            min-height: 100vh;
            padding: 30px;
            color: #333;
        }

        .container {
            max-width: 500px;
            margin: auto;
        }

        h1 {
            text-align: center;
            color: #ff4d88;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 25px;
            font-size: 14px;
        }

        .card {
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        input, select {
            width: 100%;
            padding: 12px;
            border-radius: 12px;
            border: none;
            outline: none;
            margin-bottom: 12px;
            background: #fff;
            box-shadow: 0 0 0 2px #ffd1dc;
        }

        input:focus, select:focus {
            box-shadow: 0 0 0 2px #ff4d88;
        }

        .btn-row {
            display: flex;
            gap: 10px;
        }

        button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        .btn-info {
            background: #ffe0eb;
            color: #ff4d88;
        }

        .btn-info:hover {
            background: #ffd1dc;
        }

        .btn-download {
            background: #ff4d88;
            color: white;
        }

        .btn-download:hover {
            background: #e0437a;
        }

        .loading {
            text-align: center;
            margin-top: 10px;
            color: #ff4d88;
            display: none;
        }

        .loading.show {
            display: block;
        }

        .error {
            background: #ffe6e6;
            color: #d8000c;
            padding: 10px;
            border-radius: 10px;
            margin-top: 10px;
        }

        .info-box {
            margin-top: 15px;
            background: white;
            border-radius: 12px;
            padding: 12px;
            display: none;
        }

        .info-box.show {
            display: block;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 13px;
        }

        .info-label {
            color: #888;
        }

        .info-value {
            font-weight: bold;
            color: #333;
        }

        h3 {
            color: #ff4d88;
            margin-bottom: 10px;
        }

        .historial-item {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            padding: 6px 0;
        }

        .empty {
            text-align: center;
            color: #aaa;
            font-size: 13px;
        }

    </style>
</head>

<body>
    <div class="container">
        <h1>🎀 TikTok Downloader</h1>
        <p class="subtitle">Descarga videos sin marca de agua</p>

        <div class="card">
            <input type="text" id="url" placeholder="Pega tu link aquí..." />

            <select id="quality">
                <option value="best">✨ Alta calidad</option>
                <option value="worst">⚡ Rápido</option>
            </select>

            <div class="btn-row">
                <button class="btn-info" onclick="getInfo()">🔍 Info</button>
                <button class="btn-download" onclick="downloadVideo()">⬇ Descargar</button>
            </div>

            <div class="loading" id="loading">⏳ Procesando...</div>
            <div id="error-msg" class="error" style="display:none"></div>

            <div class="info-box" id="info-box">
                <div class="info-row"><span class="info-label">Título</span><span id="i-title"></span></div>
                <div class="info-row"><span class="info-label">Autor</span><span id="i-autor"></span></div>
                <div class="info-row"><span class="info-label">Duración</span><span id="i-dur"></span></div>
                <div class="info-row"><span class="info-label">Vistas</span><span id="i-views"></span></div>
            </div>
        </div>

        <div class="card">
            <h3>📋 Historial</h3>
            <div id="historial">
                {% if historial %}
                    {% for h in historial %}
                    <div class="historial-item">
                        <span>{{ h.titulo }}</span>
                        <span>{{ h.hora }}</span>
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="empty">Sin descargas aún</p>
                {% endif %}
            </div>
        </div>
    </div>

<script>
function showError(msg) {
    const el = document.getElementById('error-msg');
    el.textContent = msg;
    el.style.display = 'block';
}

function hideError() {
    document.getElementById('error-msg').style.display = 'none';
}

function setLoading(val) {
    document.getElementById('loading').className = val ? 'loading show' : 'loading';
}

async function getInfo() {
    const url = document.getElementById('url').value.trim();
    if (!url) return showError('Pon un link primero 💔');

    hideError();
    setLoading(true);

    const res = await fetch('/info', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url})
    });

    const data = await res.json();
    setLoading(false);

    if (data.error) return showError(data.error);

    document.getElementById('i-title').textContent = data.titulo;
    document.getElementById('i-autor').textContent = data.autor;
    document.getElementById('i-dur').textContent = data.duracion;
    document.getElementById('i-views').textContent = data.vistas;

    document.getElementById('info-box').classList.add('show');
}

async function downloadVideo() {
    const url = document.getElementById('url').value.trim();
    const quality = document.getElementById('quality').value;

    if (!url) return showError('Pon un link primero 💔');

    hideError();
    setLoading(true);

    const res = await fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url, quality})
    });

    setLoading(false);

    if (!res.ok) {
        const data = await res.json();
        return showError(data.error || 'Error');
    }

    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'video.mp4';
    a.click();
}
</script>

</body>
</html>
"""
@app.route('/')
def index():
    return render_template_string(HTML, historial=historial[-10:][::-1])

@app.route('/info', methods=['POST'])
def info():
    data = request.get_json()
    url = data.get('url', '').strip()

    if 'tiktok.com' not in url:
        return jsonify({'error': 'Solo se aceptan links de TikTok.'})

    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        duracion = f"{int(info.get('duration', 0) // 60)}:{int(info.get('duration', 0) % 60):02d}"
        vistas = f"{info.get('view_count', 0):,}" if info.get('view_count') else 'N/A'

        return jsonify({
            'titulo': info.get('title', 'Sin título')[:60],
            'autor': info.get('uploader', 'Desconocido'),
            'duracion': duracion,
            'vistas': vistas,
            'preview_url': info.get('url', '')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '').strip()
    quality = data.get('quality', 'best')

    if 'tiktok.com' not in url:
        return jsonify({'error': 'Solo se aceptan links de TikTok.'}), 400

    try:
        tmp_dir = tempfile.mkdtemp()
        output_path = os.path.join(tmp_dir, '%(title)s.%(ext)s')

        ydl_opts = {
            'outtmpl': output_path,
            'format': quality,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            historial.append({
                'titulo': info_dict.get('title', 'Sin título')[:50],
                'hora': __import__('datetime').datetime.now().strftime('%H:%M')
            })

        return send_file(filename, as_attachment=True, download_name='tiktok-video.mp4')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)





