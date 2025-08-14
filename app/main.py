from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from .routers import predictions, data
from .core.config import settings

app = FastAPI(
    title="Football Score Prediction API",
    description="ML-powered football score prediction service",
    version="1.0.0"
)

app.include_router(predictions.router, prefix="/api/v1")
app.include_router(data.router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)