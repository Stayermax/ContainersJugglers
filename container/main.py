from fastapi import FastAPI, File, UploadFile
import yaml
from yaml.loader import SafeLoader
import requests

app = FastAPI()

@app.get("/status")
async def main_page():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        current_id = data['current_container_details']['current_id']
        next_url = f"http://{data['next_container_details']['next_url']}:{data['next_container_details']['next_port']}/id"
        print(next_url)
        next_id = requests.get(url=next_url).json()
        container_info = f"Container {current_id} is running. Next container id: {next_id}"
        return container_info

@app.get("/id")
async def main_page():
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            current_id = data['current_container_details']['current_id']
            return current_id
    except Exception as e:
        return e

@app.post("/files/")
async def create_file(file: bytes = File()):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}