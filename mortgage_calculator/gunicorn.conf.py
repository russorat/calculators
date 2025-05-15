import multiprocessing
import os
import ngrok
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

def on_starting(server):
    """Setup ngrok when Gunicorn starts"""
    try:
        listener = ngrok.forward(
            "localhost:5001",
            authtoken=os.getenv('NGROK_AUTH_TOKEN'),
            domain=os.getenv('NGROK_DOMAIN')
        )
        logging.info(f"ngrok tunnel established at: {listener.url()}")
    except Exception as e:
        logging.error(f"Error setting up ngrok: {str(e)}")
        raise

def on_exit(server):
    """Cleanup ngrok when Gunicorn exits"""
    try:
        ngrok.disconnect()
        logging.info("Disconnected ngrok tunnel")
    except Exception as e:
        logging.error(f"Error disconnecting ngrok tunnel: {str(e)}")
