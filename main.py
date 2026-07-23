from fastapi import FastAPI, UploadFile
import pandas as pd

app = FastAPI(title="LedgerMind AI Bookkeeper")

@app.get("/")
def home():
    return {"message": "LedgerMind is running! Upload CSV to /scan"}

@app.post("/scan")
async def scan_books(file: UploadFile):
    df = pd.read_csv(file.file)
    
    duplicates = df[df.duplicated()]
    big_expenses = df[df['amount'] > 500] # tax deductions
    fraud = df[df['amount'] < 0] # suspicious
    
    return {
        "duplicates_found": len(duplicates),
        "potential_deductions": len(big_expenses),
        "suspicious_transactions": len(fraud),
        "status": "Scan complete"
    }
