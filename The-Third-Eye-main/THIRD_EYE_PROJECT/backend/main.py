from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil, os, time
from PIL import Image
from gtts import gTTS
import subprocess

# AI Models
from ultralytics import YOLO

# -----------------------------
# Setup
# -----------------------------
app = FastAPI(title="Third Eye AI")

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# Load Models
# -----------------------------
print("Loading AI Models...")
yolo_model = YOLO("yolov8n.pt")
print("Models Loaded ✅")

# -----------------------------
# Smart Assistive Logic
# -----------------------------
def get_position(x_center):
    if x_center < 0.33:
        return "left"
    elif x_center < 0.66:
        return "center"
    else:
        return "right"

def get_distance(area):
    if area > 50000:
        return "very close"
    elif area > 20000:
        return "near"
    else:
        return "far"

def analyze_scene(image_path):

    results = yolo_model(image_path, conf=0.5)

    objects = []
    warnings = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = yolo_model.names[cls]

            x1, y1, x2, y2 = box.xyxy[0]
            width = x2 - x1
            height = y2 - y1
            area = width * height
            x_center = ((x1 + x2) / 2) / r.orig_shape[1]

            position = get_position(x_center)
            distance = get_distance(area)

            objects.append(name)

            # Generate friendly messages
            if name in ["person", "car", "bicycle"]:
                warnings.append(f"Alert! {name.capitalize()} is {distance} on your {position}. Be careful.")
            elif name in ["chair", "table", "sofa", "bench"]:
                warnings.append(f"{name.capitalize()} detected {distance} on your {position}.")
            elif name in ["stairs"]:
                warnings.append("Stairs ahead. Move carefully.")
            else:
                warnings.append(f"{name.capitalize()} detected {distance} on your {position}.")

    objects = list(set(objects))

    # FINAL MESSAGE
    if len(objects) == 0:
        final_message = "Hmm, I can't see anything clearly. Try moving slowly or improve lighting."
    else:
        if warnings:
            final_message = " ".join(warnings)
        else:
            final_message = f"I see {', '.join(objects)} in front of you."

    return {
        "message": final_message,
        "objects": objects
    }

# -----------------------------
# Text to Speech
# -----------------------------
def generate_audio(text, path):
    tts = gTTS(text, lang="en")
    tts.save(path)
    print("Playing audio:", path)
    # Non-blocking playback
    subprocess.Popen(['cmd', '/c', 'start', '', path], shell=True)

# -----------------------------
# API
# -----------------------------
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    timestamp = int(time.time())
    image_name = f"img_{timestamp}.jpg"
    image_path = os.path.join(UPLOAD_FOLDER, image_name)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Resize image
    img = Image.open(image_path).convert("RGB")
    img.save(image_path)

    # AI Processing
    try:
        result = analyze_scene(image_path)
    except Exception as e:
        return {"ok": False, "error": str(e)}

    # Generate TTS audio
    audio_name = f"scene_{timestamp}.mp3"
    audio_path = os.path.join(AUDIO_FOLDER, audio_name)
    generate_audio(result["message"], audio_path)

    return {
        "ok": True,
        "objects": result["objects"],
        "scene": result["message"],
        "audio": f"/static/audio/{audio_name}"
    }