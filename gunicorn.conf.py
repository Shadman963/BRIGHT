"""
Production Gunicorn configuration for Bright Edu Consultancy.
"""
import multiprocessing
import os

port = os.environ.get("PORT", "8000")
bind = os.environ.get("GUNICORN_BIND", f"0.0.0.0:{port}")
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get("GUNICORN_THREADS", 2))
worker_class = "gthread"
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# Prevent memory leaks with max requests limit
max_requests = 1000
max_requests_jitter = 50
