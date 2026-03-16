# Uvicorn configuration for Horilla-CRM
# This file is invoked directly: python docker/uvicorn.conf.py
# Mirrors the gunicorn.conf.py pattern used in Horilla-HR

import multiprocessing
import os

import uvicorn

# Bind settings
host = os.environ.get("UVICORN_HOST", "0.0.0.0")
port = int(os.environ.get("UVICORN_PORT", "8000"))

# Worker settings
workers = int(
    os.environ.get(
        "UVICORN_WORKERS", max(2, min(multiprocessing.cpu_count() * 2 + 1, 8))
    )
)

# Logging
log_level = os.environ.get("UVICORN_LOG_LEVEL", "info")

# Development settings
reload = os.environ.get("UVICORN_RELOAD", "false").lower() == "true"

# WebSocket settings (CRM uses Django Channels for real-time notifications)
ws_ping_interval = 20
ws_ping_timeout = 20

# ASGI lifespan
lifespan = "on"

# Process naming
proc_name = "horilla-crm"

if __name__ == "__main__":
    uvicorn.run(
        "horilla.asgi:application",
        host=host,
        port=port,
        workers=workers,
        log_level=log_level,
        reload=reload,
        ws_ping_interval=ws_ping_interval,
        ws_ping_timeout=ws_ping_timeout,
        lifespan=lifespan,
    )
