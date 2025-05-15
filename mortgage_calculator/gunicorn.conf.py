import multiprocessing
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gunicorn config
bind = "127.0.0.1:5001"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
accesslog = "-"
errorlog = "-"
loglevel = "info"
