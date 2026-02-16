# OpenClaw BI Dashboard

Business Intelligence dashboard for monitoring OpenClaw activity, tasks, automation, and metrics.

![Dashboard Preview](https://via.placeholder.com/800x400?text=OpenClaw+BI+Dashboard)

## Features

- **Session Activity** - Current model, token usage, active sessions
- **Token Trends** - 7-day usage visualization with daily breakdown
- **Active Projects** - Task tracking (Jira integration optional)
- **Automation Status** - Cron jobs monitoring
- **Memory Files** - Recent memory updates and activity
- **Real-time Updates** - Auto-refresh every 30 seconds

## Requirements

- Python 3.8+
- Node.js 18+
- OpenClaw installation with workspace directory
- (Optional) Jira credentials for project tracking

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ioxoi/openclaw-bi-dashboard.git
cd openclaw-bi-dashboard
```

### 2. Setup Backend (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Create `backend/.env` file:

```bash
# Required: Path to your OpenClaw workspace
OPENCLAW_WORKSPACE=/path/to/your/clawd

# Optional: Jira integration (leave empty to disable)
ATLASSIAN_URL=https://your-domain.atlassian.net
ATLASSIAN_EMAIL=your-email@example.com
ATLASSIAN_API_KEY=your-api-key
```

### 4. Start Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

Backend runs on: **http://localhost:8000**

### 5. Setup Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:3000**

## Configuration

### Workspace Path

The dashboard needs access to your OpenClaw workspace directory. Set this in `backend/.env`:

```bash
OPENCLAW_WORKSPACE=/home/youruser/clawd
```

### Jira Integration (Optional)

To enable project tracking:

1. Get Jira API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Add credentials to `backend/.env`:

```bash
ATLASSIAN_URL=https://yourcompany.atlassian.net
ATLASSIAN_EMAIL=you@example.com
ATLASSIAN_API_KEY=your-token-here
```

Without Jira credentials, the "Active Projects" panel will show "No active projects found."

## Architecture

**Backend:** Python FastAPI  
**Frontend:** React 18 + Vite + Recharts  
**Data Sources:** 
- OpenClaw sessions (via workspace files)
- Jira REST API (optional)
- Local memory files
- Cron job registry

## API Endpoints

- `GET /api/overview` - High-level metrics
- `GET /api/sessions` - Session activity
- `GET /api/tasks` - Project tracking (requires Jira)
- `GET /api/automation` - Cron jobs status
- `GET /api/metrics/tokens` - Token usage trends
- `GET /api/memory` - Recent memory files

## Development

Run both services in development mode:

```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

## Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
# Built files will be in frontend/dist/
```

### Run Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Serve Frontend

Option 1: Use a web server (nginx, Apache) to serve `frontend/dist/`

Option 2: Use Python's built-in server:

```bash
cd frontend/dist
python3 -m http.server 3000
```

## Troubleshooting

### Backend won't start

- Check Python version: `python3 --version` (need 3.8+)
- Verify workspace path in `.env` exists
- Check if port 8000 is already in use

### Frontend shows "Network Error"

- Ensure backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify `frontend/vite.config.js` proxy settings

### "No data available"

- Check `OPENCLAW_WORKSPACE` path is correct
- Verify OpenClaw has created session/memory files
- Check backend logs for errors

## License

MIT License - Free to use and modify

## Support

For issues or questions, open an issue on GitHub:
https://github.com/ioxoi/openclaw-bi-dashboard/issues
