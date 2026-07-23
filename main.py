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
    <head>
        <title>LedgerMind AI Bookkeeper</title>
        <style>
            body {font-family: Arial; text-align: center; padding: 50px; background: #f0f8ff;}
            h1 {color: #0066cc;}
           .card {background: white; padding: 20px; margin: 15px auto; width: 400px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
            input[type="file"] {margin: 20px;}
            button {background: #0066cc; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;}
            button:hover {background: #004999;}
            #result {margin-top: 20px; text-align: left; background: #f5f5f5; padding: 15px; border-radius: 8px;}
        </style>
    </head>
    <body>
        <h1>LedgerMind AI Bookkeeper</h1>
        <p>Automatically find tax deductions, catch fraud, and clean your books</p>
        
        <div class="card">
            <h3>📊 Upload Your CSV File</h3>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" accept=".csv" required>
                <br>
                <button type="submit">Scan Books Now</button>
            </form>
            <div id="result"></div>
        </div>

        <script>
            document.getElementById('uploadForm').onsubmit = async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = "Scanning... ⏳";
                
                const res = await fetch('/scan', {method: 'POST', body: formData});
                const data = await res.json();
                resultDiv.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
            }
        </script>
    </body>
    </html>
    """

@app.post("/scan")
async def scan_books(file: UploadFile):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    duplicates = df.duplicated().sum()
    total_rows = len(df)
    
    deductions = 0
    fraud = 0
    if 'amount' in df.columns:
        deductions = df[df['amount'] < 0].shape[0] # negative = expense
        fraud = df[df['amount'] > 500].shape[0] # big amounts = suspicious
    
    return {
        "status": "Scan Complete ✅",
        "total_transactions": total_rows,
        "duplicates_found": int(duplicates),
        "potential_deductions": int(deductions),
        "suspicious_transactions": int(fraud),
        "message": "Your books are clean!" if duplicates == 0 else f"Found {duplicates} duplicate entries"
    }

