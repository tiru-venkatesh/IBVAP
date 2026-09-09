# IBVAP — Intelligent Border Video Analytics Platform

Hackathon-ready software-defined CCTV analytics platform. Existing frontend is preserved; the FastAPI backend adds the analytics and event layer.

## Capabilities
- Human/person and vehicle detection using YOLO
- Vehicle classification and centroid tracking
- Face detection with optional lightweight local profile matching
- ANPR with a dedicated plate model + Tesseract OCR; OpenCV fallback for exploratory video scans
- Virtual fence polygons and intrusion events
- Suspicious activity / loitering heuristic
- Night/low-light movement detection
- Alert generation and persistent event logging
- CCTV image/video upload analysis
- Camera registry, fence settings, watchlist, face profiles
- Assistant API with live database-backed answers
- RTSP stream lifecycle endpoints

## Run
```powershell
cd backend
python -m pip install -r requirements.txt
python fix_opencv.py   # REQUIRED every install - see comment in requirements.txt
$env:TESSERACT_CMD = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://localhost:8000` or `http://localhost:8000/docs`.

## Models
Put these in the project root `models/`:
- `vehicle.pt` — optional custom vehicle detector. If absent, the included `backend/yolo11n.pt` is used.
- `plate.pt` — required for high-confidence model-based ANPR. Without it, video/image analysis can still run vehicle, face and night analytics; ANPR model detection is unavailable.

Do not claim ANPR accuracy without a trained plate detector. The OpenCV plate-region fallback is only a best-effort prototype.

## API groups
`/cameras`, `/alerts`, `/analytics/*`, `/fence/*`, `/watchlist/*`, `/faces/*`, `/streams/*`, `/assistant/chat`.

## Architecture
IP CCTV / uploaded video → FastAPI ingestion → OpenCV + YOLO + OCR + face detection + tracking + fence rules → events/alerts → SQLite → existing dashboard/API clients.
