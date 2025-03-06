from fastapi import FastAPI, UploadFile, File, Query
import whisper
import os

app = FastAPI()
model = whisper.load_model("base")

# Sample dataset for autocomplete
autocomplete_data = [
    "find me a red dress",
    "find me a jacket",
    "find me a blue shirt",
    "find me a black hat"
]

@app.get("/")
def check_server():
    return {"message": "Server is on"}

@app.post("/api/voice-to-text")
async def transcribe_audio(audio: UploadFile = File(...)):
    temp_path = f"temp_audio.wav"
    
    # Save the uploaded file
    with open(temp_path, "wb") as f:
        f.write(await audio.read())

    # Transcribe audio
    result = model.transcribe(temp_path)
    text = result["text"]
    
    # Clean up temporary files
    os.remove(temp_path)

    return {"text": text}

@app.get("/api/autocomplete")
def autocomplete(query: str = Query(..., min_length=1)):
    """Returns matching autocomplete suggestions based on the query."""
    matches = [phrase for phrase in autocomplete_data if phrase.startswith(query.lower())]
    return {"suggestions": matches}