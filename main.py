from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Check if this is inventory format
    if 'PRODUCT CODE' in df.columns:
        total_items = len(df)
        total_boxes = pd.to_numeric(df.get('BOX', 0), errors='coerce').sum()
        result = {
            "status": "success",
            "file_type": "Inventory Report",
            "total_products": int(total_items),
            "total_boxes": int(total_boxes),
            "message": f"Scanned {total_items} products with {total_boxes} total boxes"
        }
    else:
        result = {"status": "success", "rows": len(df), "columns": list(df.columns)}
    
    return result
