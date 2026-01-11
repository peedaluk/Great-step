# TMES (The Mining Engineering Society) - AI Coding Instructions

## Project Overview
TMES is an event management platform for IIT Kharagpur's "GREAT STEP" mining engineering fest. The main application is a **Flask + Jinja2** server-rendered web app located in `my_flask_app/`.

> **Note:** The `src/` (React), `myproject/` (Django), and `public/` directories are legacy/source files from a migration. Focus on `my_flask_app/` for all new development.

## Architecture

```
my_flask_app/
├── app/
│   ├── __init__.py      # All routes (main application file)
│   ├── config.py        # Environment-based configuration
│   ├── models.py        # SQLAlchemy models (User, OTP, GreatStepRegistration)
│   ├── email_service.py # Brevo email sending with OTP templates
│   ├── events_data.py   # Event information dictionary
│   ├── static/          # CSS, JS, images, videos
│   └── templates/       # Jinja2 HTML templates
├── run.py               # Entry point
├── requirements.txt     # Python dependencies
└── Procfile             # Gunicorn deployment config
```

## Key Models (`app/models.py`)

| Model | Purpose |
|-------|---------|
| `User` | Auth, profile, includes `is_greatstep_registered` flag |
| `OTP` | Time-limited codes for login/signup/reset |
| `PendingRegistration` | Temp storage before email verification |
| `GreatStepRegistration` | Standalone event registration with payment data |

## Authentication Flow
1. **Signup**: Form → `PendingRegistration` created → OTP email → Verify → `User` created
2. **Login**: Form → Password check → OTP email → Verify → Session created
3. **Great Step Registration**: Requires login + verified email → Form → Razorpay payment → `GreatStepRegistration` record + `User.is_greatstep_registered = True`

## Key Decorators
```python
@login_required           # User must be logged in (session['user_id'] exists)
@verified_user_required   # User must be logged in AND email verified
```

## Payment Integration (Razorpay)
- Config keys: `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` in `.env`
- Fee: `GREATSTEP_REGISTRATION_FEE` (in paise, default 50000 = ₹500)
- Flow: Create order → Razorpay checkout → Verify signature → Update DB

## Adding a New Event
1. Add to `app/events_data.py` with keys: `name`, `image`, `info[]`, `prize`, `rules`, `ps`, `teamLen`
2. Add route in `app/__init__.py` using `event_detail.html` template
3. Image goes in `app/static/images/Events/`

## Template Patterns
- All templates extend `base.html`
- Use `{% block content %}` for page content
- Flash messages: `{% with messages = get_flashed_messages(with_categories=true) %}`
- Toast notifications via `showToast(message, type)` JS function

## Commands

```bash
cd my_flask_app
pip install -r requirements.txt   # Install dependencies
python run.py                      # Dev server (port 5000)
flask db migrate -m "message"      # Create migration
flask db upgrade                   # Apply migrations
```

## Environment Variables (`.env`)
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...      # Railway provides this
BREVO_API_KEY=your-brevo-key
SENDER_EMAIL=noreply@tmes.in
SENDER_NAME=TMES IIT Kharagpur
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=your_secret
GREATSTEP_REGISTRATION_FEE=50000   # Amount in paise
```

## Dev Mode Features
- No `BREVO_API_KEY` → OTP printed to console
- `app.debug=True` → OTP shown on verification pages (`dev_otp` variable)
- SQLite used if no `DATABASE_URL`

## Database Migrations
After modifying `models.py`:
```bash
flask db migrate -m "Add new column"
flask db upgrade
```
