from google.cloud import speech
import re
from fastapi.responses import JSONResponse
from app.memory import start_trip

def transcribe_and_respond(audio_bytes):
    # Step 1: Transcribe speech to text using Google Cloud
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    # Step 2: Extract the transcribed text
    if response.results:
        text = " ".join(result.alternatives[0].transcript for result in response.results)
        text = text.lower().strip()
    else:
        return JSONResponse(content={
            "destination": "",
            "purpose": "",
            "message": "No speech recognized."
        })

    # Step 3: Use regex to extract destination and purpose
    destination_match = re.search(r"(?:destination is|go to|going to|visit|head to) ([\w\s]+?)(?: and| for| to|$)", text)
    purpose_match = re.search(r"(?:purpose is|for|to|in order to|to do) ([\w\s]+)", text)

    destination = destination_match.group(1).strip() if destination_match else ""
    purpose = purpose_match.group(1).strip() if purpose_match else ""

    # Step 4: Respond accordingly
    if destination and purpose:
        start_trip(destination, purpose)

        # Start periodic reminders (only for valid destination + purpose)
        try:
            from app.main import remind_periodically, reminder_task
            import asyncio

            if reminder_task:
                reminder_task.cancel()

            reminder_task = asyncio.create_task(remind_periodically(destination, purpose))
        except Exception as e:
            print(f"Reminder task not started due to: {e}")

        return JSONResponse(content={
            "destination": destination,
            "purpose": purpose,
            "message": f"Trip to {destination} for {purpose} saved."
        })

    elif destination:
        return JSONResponse(content={
            "destination": destination,
            "purpose": "",
            "message": f"Got destination ('{destination}') but couldn’t extract the purpose. Try saying 'to study' or 'for a meeting'."
        })

    elif purpose:
        return JSONResponse(content={
            "destination": "",
            "purpose": purpose,
            "message": f"Captured purpose ('{purpose}'), but missed the destination. Try saying 'go to Redmond Library'."
        })

    # Step 5: Fallback if both are missing
    return JSONResponse(content={
        "destination": "",
        "purpose": "",
        "message": f"Couldn’t clearly extract destination or purpose from: \"{text}\". Try saying something like 'Go to Redmond Library to study'."
    })