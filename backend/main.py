"""OpenClaw BI Dashboard - FastAPI Backend"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

app = FastAPI(title="OpenClaw BI Dashboard")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLAWD_PATH = Path.home() / "clawd"


@app.get("/")
async def root():
    return {"status": "OpenClaw BI Dashboard API", "version": "0.1.0"}


@app.get("/api/overview")
async def get_overview():
    """Get high-level overview metrics"""
    memory_files = list((CLAWD_PATH / "memory").glob("*.md")) if (CLAWD_PATH / "memory").exists() else []
    
    return {
        "status": "active",
        "workspace": str(CLAWD_PATH),
        "memory_files_count": len(memory_files),
        "last_updated": datetime.now().isoformat(),
    }


@app.get("/api/sessions")
async def get_sessions():
    """Get session activity data"""
    # This would integrate with OpenClaw sessions API
    # For now, return mock data structure
    return {
        "total_sessions": 1,
        "active_session": {
            "key": "main",
            "model": "google/gemini-3-flash-preview",
            "tokens_in": 113000,
            "tokens_out": 8000,
            "started": (datetime.now() - timedelta(hours=8)).isoformat(),
        }
    }


@app.get("/api/tasks")
async def get_tasks():
    """Get task/project tracking"""
    return {
        "active_projects": [
            {
                "id": "KAN-82",
                "title": "BI Dashboard",
                "status": "In Progress",
                "priority": "High",
                "updated": datetime.now().isoformat(),
            },
            {
                "id": "car-financing",
                "title": "Škoda Fabia Financing",
                "status": "Waiting for VWFS",
                "priority": "High",
                "deadline": "2026-03-09",
            },
            {
                "id": "trading-bot",
                "title": "Trading Bot Framework",
                "status": "Phase 1 Complete",
                "priority": "Medium",
                "progress": 20,
            }
        ],
        "completed_today": 1,
    }


@app.get("/api/automation")
async def get_automation():
    """Get cron jobs and automation status"""
    return {
        "cron_jobs": [
            {"name": "Morning motivation", "schedule": "09:00 daily", "status": "active"},
            {"name": "Midday nudge", "schedule": "13:00 daily", "status": "active"},
            {"name": "Evening check", "schedule": "19:00 daily", "status": "active"},
            {"name": "Weekly summary", "schedule": "Sunday 20:00", "status": "active"},
        ],
        "last_heartbeat": datetime.now().isoformat(),
    }


@app.get("/api/memory")
async def get_memory_summary():
    """Get memory/context summary"""
    memory_files = []
    memory_dir = CLAWD_PATH / "memory"
    
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md"), reverse=True)[:7]:
            stat = f.stat()
            memory_files.append({
                "name": f.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    
    return {
        "recent_files": memory_files,
        "memory_dir": str(memory_dir),
    }


@app.get("/api/metrics/tokens")
async def get_token_metrics():
    """Get token usage trends"""
    # Mock data - would pull from actual session logs
    today = datetime.now()
    return {
        "daily": [
            {
                "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
                "tokens_in": 50000 + (i * 5000),
                "tokens_out": 3000 + (i * 300),
            }
            for i in range(7, 0, -1)
        ],
        "current_session": {
            "tokens_in": 113000,
            "tokens_out": 8000,
            "budget": 200000,
            "usage_pct": 60.5,
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
