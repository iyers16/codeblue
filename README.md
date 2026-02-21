# CodeBlue

An AI-powered emergency intake and triage support system for hospital emergency departments. CodeBlue combines real-time computer vision monitoring with LLM-powered medical triage to streamline patient intake and queue management.

## Features

- **AI Triage**: Analyzes patient age and chief complaint using Google Gemini Flash with RAG over the ESI (Emergency Severity Index) handbook to assign an ESI level (1–5)
- **Computer Vision Surveillance**: Dual live camera feeds with MediaPipe pose detection that automatically flags critical events (choking, chest pain, patient down, headache)
- **Patient Queue**: In-memory patient queue sorted by ESI severity with real-time 5-second polling on the nurse dashboard
- **Two-Tab Interface**:
  - **Patient Kiosk** (public): Check-in form with optional vitals input
  - **Nurse Dashboard** (Auth0-protected): Live queue management and camera feeds
- **Auth0 Authentication**: OAuth2 login/logout for the nurse-facing dashboard

## Tech Stack

- **Backend**: Python, Flask, LangChain, ChromaDB, Google Generative AI (Gemini Flash + text-embedding-004), MediaPipe, OpenCV
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (MJPEG video streaming)
- **Auth**: Auth0

## Project Structure

```
codeblue/
├── app.py              # Flask routes, video streaming, API endpoints
├── vision.py           # VisionTriage — MediaPipe pose detection & alert logic
├── services.py         # PatientManager & TriageService (AI analysis)
├── ingest.py           # One-time PDF ingestion script for knowledge base
├── esi_handbook.pdf    # ESI reference document (vectorized into ChromaDB)
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_genai_api_key
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
AUTH0_SECRET=your_flask_session_secret
AUTH0_DOMAIN=your_auth0_domain
```

### 3. Build the knowledge base

Run once to vectorize the ESI handbook into ChromaDB:

```bash
python ingest.py
```

### 4. Configure cameras

Update the IP camera URLs in `app.py` (lines 24–27) to match your camera streams (e.g., from the Android IP Webcam app):

```python
CAMERA_URLS = {
    1: "http://<camera-1-ip>:4747/video",
    2: "http://<camera-2-ip>:4747/video",
}
```

### 5. Run

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/submit` | Submit patient intake form |
| `GET` | `/api/queue` | Fetch all patients (sorted by ESI) |
| `POST` | `/api/complete/<id>` | Mark a patient as resolved |
| `GET` | `/video_feed/<cam_id>` | MJPEG stream for camera 1 or 2 |
| `GET` | `/session` | Check authentication status |
| `GET` | `/login` | Initiate Auth0 login |
| `GET` | `/logout` | Log out |

## ESI Levels

| Level | Label | Description |
|-------|-------|-------------|
| 1 | Code Black | Immediate life threat |
| 2 | Critical | High risk situation |
| 3 | Urgent | Stable but needs resources |
| 4 | Emergent | Minor issue, one resource |
| 5 | Stable | Non-urgent |

## Vision Alerts

The computer vision module detects the following events using body landmark ratios:

- **Choking** — Both hands near the neck
- **Chest Pain** — Hand over the chest center
- **Patient Down** — Head below hips or sudden velocity drop
- **Headache** — Hand near the head

Each alert includes a confidence score and persists for 10 seconds to prevent flickering.
