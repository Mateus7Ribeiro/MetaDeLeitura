import multiprocessing
import os

# Configurações de binding
bind = os.getenv("GUNICORN_BIND", "127.0.0.1:5000")
backlog = 2048

# Workers
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "meta_leitura"

# Server mechanics
daemon = False
pidfile = "gunicorn.pid"
umask = 0o007
tmp_upload_dir = None

# SSL (se necessário)
# keyfile = None
# certfile = None

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
