from app import create_app
import logging

logger = logging.getLogger(__name__)
app = create_app()

if __name__ == '__main__':
    app.run(port=5001, debug=True)
