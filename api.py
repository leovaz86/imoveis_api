
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class Input(BaseModel):
    endereco: str
    url: str

@app.post("/coletar")
def coletar(data: Input):
    cmd = ["python","main.py","--endereco",data.endereco,"--url",data.url,"--saida","saida.csv"]
    subprocess.run(cmd)
    return {"csv": open("saida.csv").read()}
