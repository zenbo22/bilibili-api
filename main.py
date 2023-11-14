# Main.py
from fastapi import FastAPI
import uvicorn

from upload_blibli import router_blibliUpload, router_hello

app = FastAPI()

app.include_router(router_hello, prefix="/hello", tags=["hello"])
app.include_router(router_blibliUpload, prefix="/upload/bilibili", tags=["bilibili"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
