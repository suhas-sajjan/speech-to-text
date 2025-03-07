from fastapi import FastAPI, UploadFile, File, Query
import whisper
import os
from pydub import AudioSegment
import ffmpeg

app = FastAPI()
model = whisper.load_model("base")

autocomplete_data = [
    "find me a red dress",
    "find me a jacket",
]

@app.get("/")
def check_server():
    return {"message": "Server is on"}

@app.post("/api/voice-to-text")
async def transcribe_audio(audio: UploadFile = File(...)):
    temp_path = "temp_audio.wav"
    try:
        with open(temp_path, "wb") as f:
            f.write(await audio.read())
        result = model.transcribe(temp_path)
        text = result["text"]
        os.remove(temp_path)
        return {"text": text}
    except Exception as e:
        return {"error": f"Transcription failed: {str(e)}"}

@app.post("/api/voice-to-text-noisy")
async def transcribe_noisy_audio(audio: UploadFile = File(...)):
    temp_input_path = "temp_input.wav"
    try:
        with open(temp_input_path, "wb") as f:
            f.write(await audio.read())
        result = model.transcribe(temp_input_path)
        text = result["text"]
        os.remove(temp_input_path)
        return {"text": text}
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

@app.get("/api/autocomplete")
def autocomplete(query: str = Query(..., min_length=1)):
    try:
        matches = [phrase for phrase in autocomplete_data if phrase.startswith(query.lower())]
        return {"suggestions": matches}
    except Exception as e:
        return {"error": f"Autocomplete failed: {str(e)}"}