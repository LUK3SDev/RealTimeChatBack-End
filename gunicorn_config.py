# gunicorn_config.py

import multiprocessing

# Specifica il worker asincrono di Uvicorn
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8000'
timeout = 300
keepalive = 2