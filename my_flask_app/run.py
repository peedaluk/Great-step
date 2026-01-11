from dotenv import load_dotenv
load_dotenv()  # Load .env file before importing app

from app import app
import os

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    print(f"[INFO] Starting server with debug={debug_mode}, FLASK_ENV={os.environ.get('FLASK_ENV')}")
    print(f"[INFO] Brevo API Key configured: {'Yes' if os.environ.get('BREVO_API_KEY') and os.environ.get('BREVO_API_KEY') != 'your-brevo-api-key-here' else 'No'}")
    app.run(debug=debug_mode)