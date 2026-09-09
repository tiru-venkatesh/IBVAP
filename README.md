# IBVAP — Intelligent Border Video Analytics Platform

A software-defined CCTV intelligence layer for existing IP cameras. The supplied frontend is preserved; the backend provides the analytics, event, alert and configuration APIs.

## Problem → solution mapping

| Requirement | Implementation |
|---|---|
| Human detection | YOLO person class |
| Human tracking | Centroid tracking with persistent track IDs |
| Vehicle detection/classification | YOLO object classes |
| Face detection | OpenCV Haar cascade |
| Face recognition | Optional local profile matching API using normalized face embeddings |
| ANPR | Dedicated `plate.pt` detector + Tesseract OCR; OpenCV fallback for exploratory scans |
| Virtual fence | Configurable polygon zones |
| Intrusion detection | Track centroid entering enabled polygon |
| Suspicious activity | Loitering heuristic + repeated restricted-zone entry |
| Night movement | Brightness threshold combined with detected activity |
| Alerts | Persistent SQLite alert/event log |
| CCTV video | MP4/AVI/MOV/MKV/WEBM upload analysis |
| IP CCTV | Camera registry + RTSP lifecycle endpoints |
| Command/control integration | REST/OpenAPI endpoints |

## Start

```powershell
cd backend
python -m pip install -r requirements.txt
$env:TESSERACT_CMD = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Dashboard: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`

## Models

The project intentionally does not bundle large model weights.

- Put your vehicle model at `models/vehicle.pt` if you have a custom trained model.
- Put your plate detector at `models/plate.pt` for genuine model-based ANPR.
- If `vehicle.pt` is absent, the backend looks for `backend/yolo11n.pt` and otherwise lets Ultralytics resolve `yolo11n.pt`.
- Tesseract must be installed separately for OCR.

**Important:** a generic COCO YOLO model does not detect license plates. A real plate detector is required for reliable ANPR. The OpenCV contour fallback is only a best-effort prototype and should not be presented as production-grade ANPR.

## Main API

- `/api/status`
- `/auth/login`
- `/cameras`
- `/alerts`
- `/analytics/models/status`
- `/analytics/anpr`
- `/analytics/anpr/scan`
- `/analytics/image/analyze`
- `/analytics/video/upload`
- `/analytics/night`
- `/analytics/events`
- `/analytics/summary`
- `/fence/zones`
- `/fence/settings`
- `/fence/polygons`
- `/watchlist/plates`
- `/faces/profiles`
- `/streams/{camera_id}/start|stop|status`
- `/assistant/chat`

## Architecture

`IP CCTV / video upload → FastAPI ingestion → YOLO + OpenCV + OCR + face analytics + tracking → fence/behavior rules → events + alerts → SQLite → dashboard / C2 integration`

## Frontend

`frontend/index.html`, `frontend/app.js`, and `frontend/style.css` are retained from the supplied dashboard. The analytics backend is additive; no frontend redesign is required to run the API.
