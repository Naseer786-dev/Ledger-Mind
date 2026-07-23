from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import io

app = FastAPI(title="LedgerMind AI Bookkeeper")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/scan")
async def scan_books(file: UploadFile):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    duplicates = df[df.duplicated()]
    big_expenses = df[df["amount"] > 500] # tax deductions
    fraud = df[df["amount"] < 0] # suspicious
    
    return {
        "duplicates_found": len(duplicates),
        "potential_deductions": len(big_expenses),
        "suspicious_transactions": len(fraud),
        "status": "scan complete"
    }
