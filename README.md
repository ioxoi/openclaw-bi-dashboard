# OpenClaw BI Dashboard

Business Intelligence dashboard for monitoring OpenClaw activity, tasks, automation, and metrics.

## Quick Start

### Backend (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Backend runs on: http://localhost:8000

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:3000

## Features

- **Session Activity** - Current model, token usage
- **Token Trends** - 7-day usage visualization
- **Active Projects** - Task tracking (Jira integration)
- **Automation Status** - Cron jobs monitoring
- **Memory Files** - Recent memory updates
- **Real-time Updates** - Auto-refresh every 30s

## Architecture

**Backend:** Python FastAPI  
**Frontend:** React 18 + Vite + Recharts  
**Data Sources:** 
- OpenClaw sessions API
- Jira (via Atlassian REST API)
- Local memory files
- Cron job registry

## API Endpoints

- `GET /api/overview` - High-level metrics
- `GET /api/sessions` - Session activity
- `GET /api/tasks` - Project tracking
- `GET /api/automation` - Cron jobs status
- `GET /api/metrics/tokens` - Token usage trends
- `GET /api/memory` - Recent memory files

## Development

```bash
# Run both backend + frontend in dev mode
cd backend && source venv/bin/activate && python main.py &
cd frontend && npm run dev
```

## Production Deployment

```bash
# Build frontend
cd frontend && npm run build

# Run backend with production server
cd backend && source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

## License

Private - All Rights Reserved
