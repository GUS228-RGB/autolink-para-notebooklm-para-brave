from flask import Flask, jsonify, render_template, request
import re
import subprocess
import sys
from pathlib import Path
import requests

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
LINKS_FILE = BASE_DIR / "notebooklm_links.txt"
AUTOMATION_SCRIPT = BASE_DIR / "notebooklm_automacao.py"

def extract_video_ids(html):
    ids = []
    for pattern in [
        r'"videoId":"([A-Za-z0-9_-]{11})"',
        r'watch\\?v=([A-Za-z0-9_-]{11})',
    ]:
        for vid in re.findall(pattern, html):
            if vid not in ids:
                ids.append(vid)
    return ids

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/extract")
def extract():
    data = request.get_json(silent=True) or {}
    url = (data.get("playlist_url") or "").strip()
    if not url:
        return jsonify(ok=False, error="Cole uma URL de playlist do YouTube."), 400
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        return jsonify(ok=False, error=f"Erro ao acessar a playlist: {e}"), 502
    links = [f"https://www.youtube.com/watch?v={v}" for v in extract_video_ids(r.text)]
    return jsonify(ok=True, count=len(links), links=links)

@app.post("/api/automate")
def automate():
    data = request.get_json(silent=True) or {}
    links = list(dict.fromkeys(str(x).strip() for x in (data.get("links") or []) if str(x).strip()))
    if not links:
        return jsonify(ok=False, error="Extraia os links primeiro."), 400
    LINKS_FILE.write_text("\n".join(links) + "\n", encoding="utf-8")
    try:
        subprocess.Popen([sys.executable, str(AUTOMATION_SCRIPT)], cwd=str(BASE_DIR))
    except Exception as e:
        return jsonify(ok=False, error=f"Não foi possível iniciar a automação: {e}"), 500
    return jsonify(ok=True, count=len(links), message="Automação iniciada no Brave.")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
