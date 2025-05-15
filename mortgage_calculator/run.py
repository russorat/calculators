from app import create_app
import ngrok
import logging
from config import Config

logger = logging.getLogger(__name__)
app = create_app()

def setup_ngrok():
    try:
        listener = ngrok.forward(
            "localhost:5001",
            authtoken=app.config['NGROK_AUTH_TOKEN'],
            domain=app.config['NGROK_DOMAIN']
        )
        logger.info(f"ngrok tunnel established at: {listener.url()}")
    except Exception as e:
        logger.error(f"Error setting up ngrok: {str(e)}")
        raise

def cleanup_ngrok():
    try:
        ngrok.disconnect()
        logger.info("Disconnected ngrok tunnel")
    except Exception as e:
        logger.error(f"Error disconnecting ngrok tunnel: {str(e)}")

if __name__ == '__main__':
    setup_ngrok()
    try:
        app.run(port=5001, debug=True)
    finally:
        cleanup_ngrok()
