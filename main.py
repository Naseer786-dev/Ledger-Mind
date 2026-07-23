from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import io

app = FastAPI(title="LedgerMind AI Bookkeeper")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>LedgerMind AI Bookkeeper</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f8ff;">
        <h1 style="color: #0066cc;">LedgerMind AI Bookkeeper</h1>
        <p>Automatically find tax deductions, catch fraud, and clean your books</p>
        <h3>🔍 Smart Scanning</h3>
        <h3>💰 Tax Deductions</h3>
        <h3>🛡️ Fraud Detection</h3>
        <p><b>API is Live at /scan</b></p>
    </body>
    </html>
    """

@app.post("/scan")
async def scan_books(file: UploadFile):
    return {"status": "API working! Upload a CSV with 'amount' column"}
