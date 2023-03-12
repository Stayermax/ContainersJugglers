from fastapi import FastAPI, File, UploadFile
import yaml
from yaml.loader import SafeLoader
import requests

app = FastAPI()


@app.get("/")
async def main_page():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        current_id = data['current_container_details']['id']
        next_url = f"{data['next_container_details']['url']}:{data['next_container_details']['port']}/id"
        next_id = requests.get(next_url).json()
        container_info = f"Container {current_id} is running. Next container id: {next_id}"
        return container_info


@app.get("/id")
async def main_page():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        current_id = data['current_container_details']['id']
        return current_id


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