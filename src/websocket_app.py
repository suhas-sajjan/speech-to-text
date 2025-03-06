from fastapi import FastAPI, WebSocket
import difflib

app = FastAPI()

# Sample list of suggestions (Modify this as needed)
suggestions_list = ["hello world", "how are you", "good morning", "fastapi tutorial", "real-time processing", "speech recognition"]

def get_suggestions(text):
    """Finds the best matching suggestions from the list."""
    matches = difflib.get_close_matches(text.lower(), suggestions_list, n=3, cutoff=0.4)
    return matches if matches else ["No suggestions found"]

@app.websocket("/ws/speech-to-text")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()  # Receive text from client
            print(f"Received: {data}")
            suggestions = get_suggestions(data)
            await websocket.send_text(f"Suggestions: {', '.join(suggestions)}")  # Send suggestions back
        except Exception as e:
            print(f"Error: {e}")
            break  # Exit loop if connection closes