import os

from fastapi import FastAPI, File, UploadFile
import yaml
from yaml.loader import SafeLoader
import requests
import json
import time
app = FastAPI()
global stop_juggle_flag
stop_juggle_flag = False
print(f"stop_juggle_flag was reseted")

@app.get("/")
async def main_page():
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(json.dumps(data, indent=4))
            current_id = data['current_container_details']['current_id']
            return f"Container {current_id} is running"
    except Exception as e:
        return e

@app.get("/id")
async def main_page():
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            current_id = data['current_container_details']['current_id']
            return current_id
    except Exception as e:
        return e

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

@app.get("/start_juggle/")
async def start_juggle():
    global stop_juggle_flag
    stop_juggle_flag = False
    send_file()
    return "Juggling starts"


@app.get("/stop_juggle/")
async def stop_juggle():
    global stop_juggle_flag
    stop_juggle_flag = True
    return "Juggling stopped"


def send_file():
    if len(os.listdir('volume')) > 0:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            next_url = f"http://{data['next_container_details']['next_url']}:{data['next_container_details']['next_port']}/uploadfile/"
        file = {'file': open('volume/ball.txt', 'rb')}
        try:
            resp = requests.post(url=next_url, files=file, timeout=0.5)
        except:
            pass
        os.remove("volume/ball.txt")
        return "Ball was juggled"


@app.post("/uploadfile/")
async def get_file(file: UploadFile = File(...)):
    global stop_juggle_flag
    try:
        contents = file.file.read()
        with open(f"volume/{file.filename}", 'wb') as f:
            f.write(contents)
        update_counter()
        if not stop_juggle_flag:
            print(f"Continue juggling")
            time.sleep(2)
            send_file()
        else:
            print(f"We stopped juggling. Counter is: {get_ball_counter()}")
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/do_i_have_a_ball/")
async def do_i_have_a_ball():
    if len(os.listdir('volume')) > 0:
        return f"Yes, I have ball, counter is {get_ball_counter()}"
    else:
        return f"I don't have a ball"

def get_ball_counter():
    with open('volume/ball.txt', "r") as f:
        counter = int(f.readline())
    return counter

def set_ball_counter(n):
    with open('volume/ball.txt', "w") as f:
        f.write(f"{n}")
def update_counter():
    n = get_ball_counter()
    set_ball_counter(n+1)



