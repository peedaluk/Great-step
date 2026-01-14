import os
from app import app  # This imports the flask variable 'app'

# Optional: Load .env only if it exists (Good for local dev, ignored on Vercel)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Vercel looks for a variable named 'app' in this file.
# Since we imported it above, it is ready to go!

if __name__ == '__main__':
    # This block is ONLY run on your computer, NOT on Vercel
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"[INFO] Starting server with debug={debug_mode}")
    # Verify API key locally without crashing if missing
    api_key = os.environ.get('BREVO_API_KEY')
    has_key = 'Yes' if api_key and api_key != 'your-brevo-api-key-here' else 'No'
    print(f"[INFO] Brevo API Key configured: {has_key}")
    
    app.run(debug=debug_mode)