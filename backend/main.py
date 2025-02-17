from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from summary_logic import analyze_sales_data
from category_analysis import get_category_data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (change this for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers
)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../frontend/static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # Construct the path to the index.html file
        index_path = os.path.join(os.path.dirname(__file__), '../frontend/index.html')
        with open(index_path) as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summary")
async def summary():
    try:
        analysis = analyze_sales_data()
        return jsonable_encoder(analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/category/{category_name}")
async def category_analysis(category_name: str):
    return get_category_data(category_name)