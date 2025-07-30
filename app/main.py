from dotenv import load_dotenv
import os
import threading

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.utils import geocode_address
from app.voice import transcribe_and_respond
from app.memory import get_current_trip, save_trip_coordinates, start_trip
from pathlib import Path
import asyncio

# Reminder loop control
reminder_task = None  # Tracks the active async task

def stop_reminder_loop():
    global reminder_task
    if reminder_task:
        reminder_task.cancel()
        reminder_task = None
import pyttsx3
from threading import Thread

def speak_text(text):
    def _speak():
        if os.getenv("RENDER", "false") != "true":
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        else:
            print(f"(Silent cloud reminder): {text}")
    Thread(target=_speak).start()

async def remind_periodically(destination, purpose):
    while True:
        reminder = f"Reminder: You are heading to {destination} for {purpose}."
        speak_text(reminder)  # Updated from send_notification
        await asyncio.sleep(600)

# Load environment variables
load_dotenv()

# Initialize app and MOUNT STATIC FIRST
BASE_DIR = Path(__file__).resolve().parent.parent  # this points to your root (Mapbuddy_clean)

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Then define templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# --- ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    api_key = os.getenv("GMAPS_API_KEY")
    trip = get_current_trip()
    return templates.TemplateResponse("map.html", {
        "request": request,  # <-- this line is required!
        "google_maps_api_key": api_key,
        "trip": trip
    })

@app.get("/ping")
def ping():
    return {"message": "FastAPI is working!"}

@app.post("/start_trip")
async def start_trip_route(destination: str = Form(...), purpose: str = Form(...), test_mode: bool = Form(...)):
    global reminder_task  # Ensure scope access

    lat, lng = geocode_address(destination)
    start_trip(destination, purpose)
    if lat and lng:
        save_trip_coordinates(lat, lng)

    # Assign the task to the global tracker
    reminder_task = asyncio.create_task(remind_periodically(destination, purpose))

    return RedirectResponse(url="/", status_code=302)

@app.get("/reminder")
def reminder():
    data = get_current_trip()
    if not data:
        return {"message": "No trip data found."}
    return {"message": f"You're going to {data['destination']} for {data['purpose']}."}


@app.post("/voice_command")
async def voice_command(file: UploadFile = File(...)):
    contents = await file.read()
    result = transcribe_and_respond(contents)
    return result  



