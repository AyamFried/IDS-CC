from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import urllib.request
import urllib.error
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dashboard Keamanan")

@app.get("/", response_class=HTMLResponse)
def tampilkan_dashboard():
    try:
        # Memanggil API menggunakan nama service internal Kubernetes
        url = "http://ids-service:8000/data-alert"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=5).read()
        data_alerts = json.loads(response.decode('utf-8'))
        
        # Validasi data
        if not isinstance(data_alerts, list):
            logger.warning("API response is not a list")
            return "<h1>Sistem Aman / Belum ada serangan.</h1>"
        
        html_content = "<h1>🚨 Dashboard IDS & Firewall 🚨</h1><ul>"
        for alert in data_alerts:
            if 'ip_penyerang' in alert and 'pesan' in alert:
                html_content += f"<li><b>{alert['ip_penyerang']}</b>: {alert['pesan']}</li>"
        html_content += "</ul>"
        return html_content
    except urllib.error.URLError as e:
        logger.error(f"Network error connecting to ids-service: {e}")
        return f"<h1>Sistem Aman / Belum ada serangan.</h1><p>Service error: {type(e).__name__}</p>"
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return "<h1>Sistem Aman / Belum ada serangan.</h1><p>Invalid API response</p>"
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return f"<h1>Sistem Aman / Belum ada serangan.</h1><p>Error occurred</p>"