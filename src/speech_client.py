import asyncio
import websockets
import speech_recognition as sr

async def send_audio():
    uri = "ws://localhost:9000/ws/speech-to-text"  # Match server address & port
    async with websockets.connect(uri) as websocket:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for speech... (Press Ctrl+C to stop)")

            while True:
                try:
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio)  # Convert speech to text
                    print(f"Recognized: {text}")
                    
                    await websocket.send(text)  # Send to WebSocket server
                    response = await websocket.recv()  # Receive suggestions
                    print(response)

                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError:
                    print("Speech Recognition service unavailable.")
                except KeyboardInterrupt:
                    print("Stopping...")
                    break

asyncio.run(send_audio())