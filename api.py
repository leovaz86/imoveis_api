
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, json, os

app = FastAPI(title="Vertex Laudos API", version="1.0.0")

class Input(BaseModel):
    endereco: str
    vivareal_url: str
    radius_km: float = 1.0

@app.get("/")
def root():
    return {"ok": True, "service": "vertex-laudos", "endpoints": ["/coletar", "/health", "/docs"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/coletar")
def coletar(data: Input):
    output_csv = "saida.csv"
    cmd = [
        "python", "main.py",
        "--endereco", data.endereco,
        "--vivareal_url", data.vivareal_url,
        "--radius_km", str(data.radius_km),
        "--saida", output_csv
    ]
    subprocess.run(cmd, check=True)
    with open(output_csv, "r", encoding="utf-8") as f:
        csv_text = f.read()
    return {"csv": csv_text}
