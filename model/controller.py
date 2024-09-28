from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend import Backend
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Разрешенные источники (например, ваш Angular-приложение)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы (например, GET, POST и т.д.)
    allow_headers=["*"],  # Разрешенные заголовки (например, Content-Type, Authorization и т.д.)
)


backend = Backend()

def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


@app.post("/api/create/clips")
async def get_clips(video: UploadFile,
                    subtitles: str = Form(...),
                    fields: str = Form(...),
                    face_tracking: str = Form(...),
                    humor: str = Form(...),
                    clickbait: str = Form(...),
                    threshold: str = Form(...),
                    min_length: int = Form(...),
                    max_length: int = Form(...)):
    video_data = {
        "subtitles": subtitles.lower() == 'true',
        "fields": fields.lower() == 'true',
        "face_tracking": face_tracking.lower() == 'true',
        "humor": humor.lower() == 'true',
        "clickbait": clickbait.lower() == 'true',
        "threshold": float(threshold),
        "min_length": min_length,
        "max_length": max_length,
    }
    file = video

    ensure_directory_exists("videos")
    ensure_directory_exists("results")

    file_location = f"videos/{file.filename}"
    
    with open(file_location, "wb") as video:
        video.write(await file.read())
    
    clip_names = backend.work(file.filename,
                              subtitles=video_data["subtitles"],
                              fields=video_data["fields"],
                              face_tracking=video_data["face_tracking"],
                              humor=video_data["humor"],
                              clickbait=video_data["clickbait"],
                              threshold=video_data["threshold"],
                              min_length=video_data["min_length"],
                              max_length=video_data["max_length"])
    print(clip_names)
    return {'clips': clip_names}

@app.get("/api/get/file/id/{file_id}")
async def get_clip_by_id(file_id: str):
    video_path = f"results/{file_id}.mp4"
    
    # Проверяем, существует ли файл
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Отдаём файл через FileResponse
    return FileResponse(video_path, media_type="video/mp4")


@app.get("/api/delete/file/id/{file_id}")
async def delete_clip_by_id(file_id: str):
    video_path = f"results/{file_id}.mp4"
    
    # Проверяем, существует ли файл
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        # Удаляем файл
        os.remove(video_path)
        return {"message": f"Video {file_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the video")