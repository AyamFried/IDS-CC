from fastapi import FastAPI
from pydantic import BaseModel
import socket

app = FastAPI(title="IDS Log Analyzer")
alerts = [] # Database di memori

class NetworkLog(BaseModel):
    source_ip: str
    protocol: str
    action: str

@app.post("/kirim-log")
def analyze_log(log: NetworkLog):
    if log.protocol == "SSH" and log.action == "FAILED":
        peringatan = {"ip_penyerang": log.source_ip, "pesan": f"Anomali: Indikasi Brute Force SSH! (Dideteksi oleh Pod: {socket.gethostname()})"}
        alerts.append(peringatan)
        return {"status": "Bahaya", "detail": peringatan}
    return {"status": "Aman", "pesan": f"Log dicatat oleh Pod: {socket.gethostname()}"}

@app.get("/data-alert")
def get_alerts():
    return alerts