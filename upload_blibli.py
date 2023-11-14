# A.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio

from bilibili_api import sync, video_uploader, Credential

router_blibliUpload = APIRouter()

class VideoUploadRequest(BaseModel):
    SESSDATA: str
    BILI_JCT: str
    BUVID3: str
    path: str
    title: str
    description: str
    cover: str

router_hello = APIRouter()
@router_hello.get("/")
async def read_root():
    return {"Hello": "World"}

@router_blibliUpload.post("/")
async def upload_video(request: VideoUploadRequest):
    try:
        credential = Credential(sessdata=request.SESSDATA, bili_jct=request.BILI_JCT, buvid3=request.BUVID3)
        meta = {
            "act_reserve_create": 0,
            "copyright": 1,
            "source": "",
            "desc": request.description,
            "desc_format_id": 0,
            "dynamic": "",
            "interactive": 0,
            "no_reprint": 1,
            "open_elec": 0,
            "origin_state": 0,
            "subtitles": {
                "lan": "",
                "open": 0
            },
            "tag": "生活",
            "tid": 138,
            "title": request.title,
            "up_close_danmaku": False,
            "up_close_reply": False,
            "up_selection_reply": False,
            "dtime": 0
        }
        page = video_uploader.VideoUploaderPage(path=request.path, title=request.title, description=request.description)
        uploader = video_uploader.VideoUploader([page], meta, credential, cover=request.cover)

        @uploader.on("__ALL__")
        async def event_handler(data):
            print(data)

        await uploader.start()

        return {"message": "Video uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

