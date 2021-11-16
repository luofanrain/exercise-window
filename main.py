from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import Body
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
import pyttsx3
from time import sleep
import webbrowser
import socket
app = FastAPI()
templates = Jinja2Templates(directory="view")
chromePath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath)) 

engine = pyttsx3.init()
def speakText(data):
	# voices = engine.getProperty('voices')  
    engine.say(data.content)
    engine.runAndWait()

class SpeakModel(BaseModel):
    content: str=""

@app.post("/speak")
async def speak(data:SpeakModel):
    try:
        speakText(data)
        return JSONResponse(status_code=200, content={"msg": "执行成功"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"msg": "操作失败"})

@app.get("/")
def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

if __name__ == '__main__':
    import uvicorn
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port = 3000
    url = f"http://{ip}:{port}/"
    webbrowser.get('chrome').open_new_tab(url)
    uvicorn.run('main:app', reload=True, host='0.0.0.0',port=port)