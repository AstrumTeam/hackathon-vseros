from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from functools import wraps
from backend import Backend
from io import BytesIO
import zipfile
import os

app = FastAPI()

backend = Backend()

def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

def video_file_required(func):
    @wraps(func)
    async def wrapper(file: UploadFile = File(...)):
        # Проверка MIME-типа файла
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid video format.")
        
        # Если файл корректен, продолжаем выполнение оригинальной функции
        return await func(file)
    
    return wrapper


@app.post("/api/get/clips")
async def get_clips(file: UploadFile):
    ensure_directory_exists("videos")

    file_location = f"videos/{file.filename}"
    
    with open(file_location, "wb") as video:
        video.write(await file.read())
    
    clip_names = backend.work(file.filename)
    # clip_names = []

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for clip_name in clip_names:
            if os.path.exists(clip_name):
                with open(clip_name, "rb") as file:
                    zip_file.writestr(os.path.basename(clip_name), file.read())
            else:
                return {"error": f"File {clip_name} not found"}

    zip_buffer.seek(0)

    return StreamingResponse(zip_buffer, media_type="application/x-zip-compressed", headers={"Content-Disposition": "attachment; filename=clips.zip"})