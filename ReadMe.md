# MapBuddy: Memory Support & Navigation Companion
MapBuddy is a voice-enabled navigation companion designed to help people with short-term memory loss, amnesia, or early-stage dementia travel independently and safely.Unlike traditional GPS apps, MapBuddy reminds users of their trip purpose, gives current location awareness, and helps them re-orient themselves when confused.

# Joy doesn’t depend on memory; it lives in moments.

# Key Features
Trip Purpose Storage: Before starting a trip, users save where they are going and why.
Trip Purpose Reminder: Reminds the user why they left home and where they are going.
Live Location Awareness: Answers “Where am I?” with street-level info and progress updates.
Voice Interaction: Supports voice queries like “What should I do now?” (Prototype phase).
Caregiver Updates: Optional location sharing and trip notifications (future phase).
Google Maps Guidance: Live Google Maps view with the user’s location and navigation.
Safe Return: Helps users find their way home if they forget their goal.
Emergency Mode: Allows users or caregivers to trigger an SOS or alert (future phase).
# Tech Stack
Backend
FastAPI: API layer and server logic
Google Maps API: For map rendering and live navigation
SpeechRecognition: Speech-to-text for voice commands
Jinja2 + HTML: For rendering the live Google Map in a web view
Environment Variables (.env): For securing your API keys

# Frontend (Future Phases)
Gradio UI prototype (voice input/output)
Render.com for prototype hosting
React Native or Flutter mobile app (planned)
Deployment & Ops
Docker: For local containerization (optional for now)
Render / GCP App Engine: Cloud hosting options
Redis + Celery: Background task queueing (future)
WebSockets: For real-time caregiver updates (future)

# Product Roadmap
(refer to the file)
product Roadmap.png

# Local Setup (Prototype)
# Clone the repo
git clone https://github.com/yourname/mapbuddy.git
cd mapbuddy

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.venv\scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Google Maps API Key to a .env file
echo GMAPS_API_KEY=your_google_maps_api_key_here > .env

# Run the FastAPI app
uvicorn app.main:app --reload

# Access the Google Map at:
http://127.0.0.1:8000/map
# Current Prototype Endpoints
Method	Endpoint	Purpose
GET	/ping	Health check
POST	/start_trip	Start a trip with destination/purpose
GET	/map	View Google Map with live location

# Intended Users
People with short-term memory loss, post-traumatic brain injury, or early dementia
Elderly individuals living alone but capable of independent outings
Children walking to school alone (future adaptation)
Tourists in unfamiliar cities
Field workers or hikers on complex walking routes

# Planned Future Enhancements
Real-time route deviation detection
AI-powered route corrections
Remote caregiver alerts and trip controls
Wearable device integrations (Apple Watch, Fitbit, etc.)
Smart assistant integrations (Google Assistant, Alexa, Siri)


