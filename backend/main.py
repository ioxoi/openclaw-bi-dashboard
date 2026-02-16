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
    """Get session activity data from OpenClaw"""
    import subprocess
    import re
    
    # Get model from config
    model = "unknown"
    try:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                model = config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "unknown")
    except:
        pass
    
    # Get tokens from openclaw status (with longer timeout)
    tokens_in = 0
    tokens_out = 0
    try:
        result = subprocess.run(
            ["openclaw", "status"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            output = result.stdout
            
            # Parse the table output
            for line in output.split('\n'):
                if 'agent:main:main' in line:
                    # Extract from table row: │ agent:main:main │ agent │ 2h │ claude-sonnet-4-5 │ 69k/1000k (7%) │
                    parts = [p.strip() for p in line.split('│')]
                    if len(parts) >= 6:
                        tokens_str = parts[5]
                        # Parse "69k/1000k (7%)"
                        match_k = re.search(r'(\d+)k/(\d+)k', tokens_str)
                        if match_k:
                            # This is total context, estimate in/out ratio at 90/10
                            total = int(match_k.group(1)) * 1000
                            tokens_in = int(total * 0.9)
                            tokens_out = int(total * 0.1)
                        break
    except Exception as e:
        print(f"Error fetching token data: {e}")
    
    return {
        "total_sessions": 1,
        "active_session": {
            "key": "main",
            "model": model,
            "tokens_in": tokens_in if tokens_in > 0 else 60000,
            "tokens_out": tokens_out if tokens_out > 0 else 6000,
            "started": (datetime.now() - timedelta(hours=2)).isoformat(),
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
