import os
from google.cloud import speech
import re
from fastapi.responses import JSONResponse
from app.memory import start_trip
import traceback

def transcribe_and_respond(audio_bytes):
    try:
        print("Transcription initiated")

        # Set credentials path 
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", "/etc/secrets/google-credentials.json"
        )
        print("GOOGLE_APPLICATION_CREDENTIALS:", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

        # Google Speech client setup
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            language_code="en-US"
        )
        response = client.recognize(config=config, audio=audio)

        # Extract text
        if response.results:
            text = " ".join(result.alternatives[0].transcript for result in response.results).lower().strip()
            print("Transcript:", text)
        else:
            print("No results returned from Google Speech API")
            return JSONResponse(content={
                "destination": "", "purpose": "", "message": "No speech recognized."
            })

        # Parse destination and purpose
        destination_match = re.search(r"(?:destination is|go to|going to|visit|head to) ([\w\s]+?)(?: and| for| to|$)", text)
        purpose_match = re.search(r"(?:purpose is|for|to|in order to|to do) ([\w\s]+)", text)

        destination = destination_match.group(1).strip() if destination_match else ""
        purpose = purpose_match.group(1).strip() if purpose_match else ""
        print(f"Destination: {destination}")
        print(f"Purpose: {purpose}")

        # Start trip and reminder
        if destination and purpose:
            start_trip(destination, purpose)
            try:
                from app.main import remind_periodically, reminder_task
                import asyncio
                if reminder_task:
                    reminder_task.cancel()
                reminder_task = asyncio.create_task(remind_periodically(destination, purpose))
            except Exception as e:
                print(f"Reminder error: {e}")

            return JSONResponse(content={
                "destination": destination, "purpose": purpose,
                "message": f"Trip to {destination} for {purpose} saved."
            })

        elif destination:
            return JSONResponse(content={
                "destination": destination, "purpose": "",
                "message": f"Got destination ('{destination}') but couldn’t extract purpose."
            })

        elif purpose:
            return JSONResponse(content={
                "destination": "", "purpose": purpose,
                "message": f"Captured purpose ('{purpose}') but missed destination."
            })

        return JSONResponse(content={
            "destination": "", "purpose": "", "message": f"Couldn't extract destination or purpose from: \"{text}\""
        })

    except Exception as e:
        print("Voice command error:", str(e))
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
