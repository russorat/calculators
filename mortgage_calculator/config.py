import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    NGROK_AUTH_TOKEN = os.environ.get('NGROK_AUTH_TOKEN')
    NGROK_DOMAIN = os.environ.get('NGROK_DOMAIN')
