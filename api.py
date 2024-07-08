from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mimetypes import guess_type
from utils import fetch_content, analyze_content
import requests


router = APIRouter()

class URLRequest(BaseModel):
    url: str

@router.post("/analyze")
async def analyze_file(file: UploadFile = File(None), url: str = Form(None)):
    if file:
        FILENAME = file.filename
        file_bytes = await file.read()
    elif url:
        FILENAME = url
        response = requests.get(FILENAME)
        response.raise_for_status()
        file_bytes = response.content        
    else:
        raise HTTPException(status_code=400, detail="File or URL must be provided")
    
    mime_type, _ = guess_type(FILENAME)
    
    if mime_type not in ["application/pdf", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
        
    result = analyze_content(file_bytes)
    return result


@router.post("/analyze-url")
async def analyze_url(request: URLRequest):
    result = analyze_content(request.url)
    return result
