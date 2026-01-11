from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import razorpay
import hmac
import hashlib
from .events_data import get_event_data, EVENTS_DATA
from .config import Config, config
from .models import db, User, OTP, PendingRegistration, GreatStepRegistration
from .email_service import send_verification_email, send_login_otp, send_reset_password_email

app = Flask(__name__)

# Load config based on FLASK_ENV
import os
flask_env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config.get(flask_env, Config))
print(f"[INFO] Loaded {flask_env} configuration, DEBUG={app.config.get('DEBUG', False)}")

# Session configuration for better compatibility
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Create tables if they don't exist (for development)
with app.app_context():
    db.create_all()


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"[DEBUG] login_required check - user_id in session: {session.get('user_id')}")
        if 'user_id' not in session:
            flash('Please sign in to access this page', 'error')
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sample')
def sample():
    return render_template('sample.html')

@app.route('/tmes')
def tmes():
    return render_template('tmes.html')

@app.route('/aboutus')
def about():
    return render_template('about.html')

@app.route('/great-step/events')
def events():
    # Auto redirect to competitions like React does
    return redirect(url_for('competitions'))

@app.route('/great-step/events/competitions')
def competitions():
    return render_template('competitions.html')

@app.route('/great-step/events/workshops')
def workshops():
    return render_template('workshops.html')

@app.route('/great-step/events/panel-discussion')
def panel_discussion():
    return render_template('panel_discussion.html')

# Individual Competition Pages
@app.route('/great-step/events/competitions/QS')
def quiz_spiel():
    event = get_event_data('Quiz_Spiel')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Enviro_CS')
def enviro_cs():
    event = get_event_data('Enviro_CS')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Petro_CS')
def petro_cs():
    event = get_event_data('Petro_CS')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Mine_CS')
def mine_cs():
    event = get_event_data('Mine_CS')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Safety_Hunt')
def safety_hunt():
    event = get_event_data('Safety_Hunt')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Safety_DA')
def safety_da():
    event = get_event_data('Safety_DA')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Geobotics')
def geobotics():
    event = get_event_data('Geobotics')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Pitch_Perfect')
def pitch_perfect():
    event = get_event_data('Pitch_Perfect')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Nmic')
def nmic():
    event = get_event_data('Nmic')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/code_ext')
def code_ext():
    event = get_event_data('code_ext')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Mine_A_Thon')
def mine_a_thon():
    event = get_event_data('Mine_A_Thon')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/gth')
def gth():
    event = get_event_data('gth')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/MS')
def mine_shot():
    event = get_event_data('Mine_Shot')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/quiz')
def publi_quiz():
    event = get_event_data('publiQuiz')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Indu_Design')
def indu_design():
    event = get_event_data('Indu_Design')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/great-step/events/competitions/Mineac')
def mineac():
    event = get_event_data('Mineac')
    return render_template('event_detail.html', 
                           event_name=event['name'],
                           event_image=url_for('static', filename=event['image']),
                           info_list=event['info'],
                           rules_url=event.get('rules'),
                           ps_url=event.get('ps'),
                           submission_url=event.get('submission'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('signin.html')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Check if there's a pending registration for this email
            pending = PendingRegistration.query.filter_by(email=email).first()
            if pending:
                if pending.is_valid():
                    # Redirect to complete verification
                    flash('Please complete your email verification first.', 'warning')
                    dev_otp = pending.otp_code if app.debug else None
                    return render_template('verify_otp.html',
                                           email=email,
                                           purpose='signup_verification',
                                           action_url=url_for('verify_signup'),
                                           back_url=url_for('signup'),
                                           dev_otp=dev_otp)
                else:
                    # Pending registration expired, delete it
                    db.session.delete(pending)
                    db.session.commit()
                    flash('Your registration expired. Please sign up again.', 'error')
                    return redirect(url_for('signup'))
            
            flash('Invalid email or password', 'error')
            return render_template('signin.html')
        
        if not user.is_verified:
            flash('Please verify your email first', 'error')
            return render_template('signin.html')
        
        if not user.check_password(password):
            flash('Invalid email or password', 'error')
            return render_template('signin.html')
        
        # Generate and send OTP for login
        otp = OTP.create_otp(user.id, 'login')
        
        success, message = send_login_otp(email, otp.code)
        
        if success:
            session['pending_login_email'] = email
            dev_otp = otp.code if app.debug else None
            return render_template('verify_otp.html',
                                   email=email,
                                   purpose='login',
                                   action_url=url_for('verify_login'),
                                   back_url=url_for('signin'),
                                   dev_otp=dev_otp)
        else:
            flash('Failed to send OTP. Please try again.', 'error')
    
    return render_template('signin.html')


@app.route('/verify-login', methods=['POST'])
def verify_login():
    email = request.form.get('email', '').strip().lower()
    otp_code = request.form.get('otp', '')
    
    if not email or not otp_code:
        flash('Invalid request', 'error')
        return redirect(url_for('signin'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('signin'))
    
    # Validate OTP
    otp = OTP.query.filter_by(user_id=user.id, purpose='login', is_used=False).order_by(OTP.created_at.desc()).first()
    
    if not otp or not otp.is_valid() or otp.code != otp_code:
        # Pass dev_otp for debugging when OTP is wrong
        dev_otp = otp.code if otp and app.debug else None
        return render_template('verify_otp.html',
                               email=email,
                               purpose='login',
                               action_url=url_for('verify_login'),
                               back_url=url_for('signin'),
                               error='Invalid or expired OTP',
                               dev_otp=dev_otp)
    
    # Mark OTP as used
    otp.use()
    
    # Create session
    session['user_id'] = user.id
    session['user_email'] = user.email
    session.permanent = True  # Make session persistent
    session.pop('pending_login_email', None)
    
    print(f"[DEBUG] Login successful for {user.email}, session user_id: {session.get('user_id')}")
    
    flash('Signed in successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        cpassword = request.form.get('cpassword', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        college = request.form.get('college', '').strip()
        year = request.form.get('year', '').strip()
        
        # Validation
        if not email or not password or not cpassword or not first_name or not last_name:
            flash('Please fill in all required fields', 'error')
            return render_template('signup.html')
        
        if password != cpassword:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('signup.html')
        
        # Validate mobile number
        if mobile and (len(mobile) != 10 or not mobile.isdigit()):
            flash('Please enter a valid 10-digit mobile number', 'error')
            return render_template('signup.html')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please sign in.', 'error')
            return render_template('signup.html')
        
        # Create pending registration using the class method (handles OTP generation)
        pending = PendingRegistration.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile if mobile else None,
            college=college if college else None,
            year=year if year else None
        )
        
        # Send verification email with the OTP from pending registration
        success, message = send_verification_email(email, pending.otp_code)
        
        if success:
            session['pending_signup_email'] = email
            # In dev mode, pass OTP to template for display
            dev_otp = pending.otp_code if app.debug else None
            return render_template('verify_otp.html',
                                   email=email,
                                   purpose='signup_verification',
                                   action_url=url_for('verify_signup'),
                                   back_url=url_for('signup'),
                                   dev_otp=dev_otp)
        else:
            flash('Failed to send verification email. Please try again.', 'error')
    
    return render_template('signup.html')


@app.route('/verify-signup', methods=['POST'])
def verify_signup():
    email = request.form.get('email', '').strip().lower()
    otp_code = request.form.get('otp', '')
    
    if not email or not otp_code:
        flash('Invalid request', 'error')
        return redirect(url_for('signup'))
    
    # Find pending registration
    pending = PendingRegistration.query.filter_by(email=email).first()
    if not pending:
        flash('Registration not found. Please sign up again.', 'error')
        return redirect(url_for('signup'))
    
    # Check if pending registration is expired
    if not pending.is_valid():
        db.session.delete(pending)
        db.session.commit()
        flash('Registration expired. Please sign up again.', 'error')
        return redirect(url_for('signup'))
    
    # Validate OTP against the pending registration's otp_code
    if pending.otp_code != otp_code:
        # Pass dev_otp for debugging when OTP is wrong
        dev_otp = pending.otp_code if app.debug else None
        return render_template('verify_otp.html',
                               email=email,
                               purpose='signup_verification',
                               action_url=url_for('verify_signup'),
                               back_url=url_for('signup'),
                               error='Invalid OTP. Please try again.',
                               dev_otp=dev_otp)
    
    # Create actual user account with all profile fields
    user = User(
        email=pending.email,
        password_hash=pending.password_hash,
        first_name=pending.first_name,
        last_name=pending.last_name,
        mobile=pending.mobile,
        college=pending.college,
        year=pending.year,
        is_verified=True
    )
    db.session.add(user)
    
    # Delete pending registration
    db.session.delete(pending)
    db.session.commit()
    
    session.pop('pending_signup_email', None)
    
    flash('Account created successfully! Please sign in.', 'success')
    return redirect(url_for('signin'))

@app.route('/resetPassword', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Please enter your email address', 'error')
            return render_template('reset_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists or not for security
            flash('If your email is registered, you will receive a password reset code.', 'info')
            return render_template('reset_password.html')
        
        # Generate and send reset OTP
        otp = OTP.create_otp(user.id, 'reset')
        
        success, message = send_reset_password_email(email, otp.code)
        
        if success:
            session['pending_reset_email'] = email
            dev_otp = otp.code if app.debug else None
            return render_template('verify_otp.html',
                                   email=email,
                                   purpose='reset',
                                   action_url=url_for('verify_reset'),
                                   back_url=url_for('reset_password'),
                                   dev_otp=dev_otp)
        else:
            flash('Failed to send reset email. Please try again.', 'error')
    
    return render_template('reset_password.html')


@app.route('/verify-reset', methods=['POST'])
def verify_reset():
    email = request.form.get('email', '').strip().lower()
    otp_code = request.form.get('otp', '')
    
    if not email or not otp_code:
        flash('Invalid request', 'error')
        return redirect(url_for('reset_password'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('reset_password'))
    
    # Validate OTP
    otp = OTP.query.filter_by(user_id=user.id, purpose='reset', is_used=False).order_by(OTP.created_at.desc()).first()
    
    if not otp or not otp.is_valid() or otp.code != otp_code:
        # Pass dev_otp for debugging when OTP is wrong
        dev_otp = otp.code if otp and app.debug else None
        return render_template('verify_otp.html',
                               email=email,
                               purpose='reset',
                               action_url=url_for('verify_reset'),
                               back_url=url_for('reset_password'),
                               error='Invalid or expired OTP',
                               dev_otp=dev_otp)
    
    # Mark OTP as used and store reset token in session
    otp.use()
    
    session['reset_verified_email'] = email
    return redirect(url_for('new_password'))


@app.route('/new-password', methods=['GET', 'POST'])
def new_password():
    email = session.get('reset_verified_email')
    
    if not email:
        flash('Please complete the reset process first', 'error')
        return redirect(url_for('reset_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        cpassword = request.form.get('cpassword', '')
        
        if not password or not cpassword:
            flash('Please fill in all fields', 'error')
            return render_template('new_password.html')
        
        if password != cpassword:
            flash('Passwords do not match', 'error')
            return render_template('new_password.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('new_password.html')
        
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            db.session.commit()
            
            session.pop('reset_verified_email', None)
            flash('Password updated successfully! Please sign in.', 'success')
            return redirect(url_for('signin'))
        else:
            flash('User not found', 'error')
            return redirect(url_for('reset_password'))
    
    return render_template('new_password.html', email=email)


@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    """AJAX endpoint to resend OTP with rate limiting"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    purpose = data.get('purpose', '')
    
    if not email or not purpose:
        return jsonify({'success': False, 'message': 'Invalid request'})
    
    # Rate limiting: Check if last OTP was sent within 60 seconds
    last_resend_key = f'last_resend_{email}_{purpose}'
    last_resend_time = session.get(last_resend_key)
    
    if last_resend_time:
        from datetime import datetime
        time_diff = (datetime.utcnow() - datetime.fromisoformat(last_resend_time)).total_seconds()
        if time_diff < 60:
            remaining = int(60 - time_diff)
            return jsonify({'success': False, 'message': f'Please wait {remaining} seconds before resending'})
    
    if purpose == 'signup_verification':
        pending = PendingRegistration.query.filter_by(email=email).first()
        if not pending:
            return jsonify({'success': False, 'message': 'Registration not found'})
        
        # Generate new OTP code and update the pending registration
        pending.otp_code = PendingRegistration.generate_otp()
        pending.created_at = datetime.utcnow()  # Reset expiry time
        db.session.commit()
        
        success, message = send_verification_email(email, pending.otp_code)
    else:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        otp = OTP.create_otp(user.id, purpose)
        
        if purpose == 'login':
            success, message = send_login_otp(email, otp.code)
        elif purpose == 'reset':
            success, message = send_reset_password_email(email, otp.code)
        else:
            return jsonify({'success': False, 'message': 'Invalid purpose'})
    
    if success:
        # Record resend time for rate limiting
        session[last_resend_key] = datetime.utcnow().isoformat()
        return jsonify({'success': True, 'message': 'OTP sent successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP. Please try again.'})


@app.route('/signout')
def signout():
    session.clear()
    flash('You have been signed out', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    if not user:
        # User no longer exists, clear session
        session.clear()
        flash('Your session has expired. Please sign in again.', 'error')
        return redirect(url_for('signin'))
    return render_template('profile.html', user=user)

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Your session has expired. Please sign in again.', 'error')
        return redirect(url_for('signin'))
    
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_new_password = request.form.get('confirm_new_password', '')
    
    # Validate current password
    if not user.check_password(current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('profile'))
    
    # Validate new password
    if len(new_password) < 6:
        flash('New password must be at least 6 characters', 'error')
        return redirect(url_for('profile'))
    
    if new_password != confirm_new_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('profile'))
    
    # Update password
    user.set_password(new_password)
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'success': False, 'message': 'Your session has expired. Please sign in again.', 'redirect': url_for('signin')})
    
    # Update only mobile field (phone number)
    mobile = request.form.get('mobile', '').strip()
    
    if mobile:
        # Validate mobile is 10 digits
        if not mobile.isdigit() or len(mobile) != 10:
            return jsonify({'success': False, 'message': 'Please enter a valid 10-digit mobile number'})
        user.mobile = mobile
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Phone number updated successfully!'})

# ============== PAGE-BASED PROFILE SETTINGS ==============

@app.route('/settings/phone', methods=['GET', 'POST'])
@login_required
def change_phone_page():
    """Standalone page for changing phone number"""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Your session has expired. Please sign in again.', 'error')
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        mobile = request.form.get('mobile', '').strip()
        
        if not mobile:
            flash('Please enter a phone number.', 'error')
            return render_template('change_phone.html', user=user)
        
        if not mobile.isdigit() or len(mobile) != 10:
            flash('Please enter a valid 10-digit mobile number.', 'error')
            return render_template('change_phone.html', user=user)
        
        user.mobile = mobile
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Phone number updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('change_phone.html', user=user)

@app.route('/settings/email', methods=['GET', 'POST'])
@login_required
def change_email_page():
    """Standalone page for changing email address"""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Your session has expired. Please sign in again.', 'error')
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        new_email = request.form.get('new_email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not new_email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('change_email.html', user=user)
        
        if not user.check_password(password):
            flash('Incorrect password.', 'error')
            return render_template('change_email.html', user=user)
        
        if new_email == user.email:
            flash('New email is the same as your current email.', 'error')
            return render_template('change_email.html', user=user)
        
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user:
            flash('This email is already in use.', 'error')
            return render_template('change_email.html', user=user)
        
        # Generate OTP and send to new email
        import random
        otp_code = str(random.randint(100000, 999999))
        
        session['pending_email_change'] = {
            'new_email': new_email,
            'otp_code': otp_code,
            'user_id': user.id
        }
        
        from .email_service import send_login_otp
        success, message = send_login_otp(new_email, otp_code)
        
        if success or app.debug:
            flash('Verification code sent to your new email!', 'success')
            return redirect(url_for('verify_email_change'))
        else:
            flash('Failed to send verification email. Please try again.', 'error')
            return render_template('change_email.html', user=user)
    
    return render_template('change_email.html', user=user)

@app.route('/settings/verify-email', methods=['GET', 'POST'])
@login_required
def verify_email_page():
    """Standalone page for initiating email verification"""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Your session has expired. Please sign in again.', 'error')
        return redirect(url_for('signin'))
    
    if user.is_verified:
        flash('Your email is already verified.', 'info')
        return render_template('verify_email_page.html', user=user)
    
    if request.method == 'POST':
        # Generate OTP
        import random
        otp_code = str(random.randint(100000, 999999))
        
        session['pending_email_verification'] = {
            'email': user.email,
            'otp_code': otp_code,
            'user_id': user.id
        }
        
        from .email_service import send_login_otp
        success, message = send_login_otp(user.email, otp_code)
        
        if success or app.debug:
            flash('Verification code sent to your email!', 'success')
            return redirect(url_for('verify_current_email'))
        else:
            flash('Failed to send verification email. Please try again.', 'error')
            return render_template('verify_email_page.html', user=user)
    
    return render_template('verify_email_page.html', user=user)

@app.route('/change-email', methods=['POST'])
@login_required
def change_email():
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'success': False, 'message': 'Your session has expired. Please sign in again.', 'redirect': url_for('signin')})
    
    new_email = request.form.get('new_email', '').strip().lower()
    password = request.form.get('password', '')
    
    if not new_email or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'})
    
    # Verify password
    if not user.check_password(password):
        return jsonify({'success': False, 'message': 'Incorrect password'})
    
    # Check if email is same as current
    if new_email == user.email:
        return jsonify({'success': False, 'message': 'New email is the same as your current email'})
    
    # Check if email already exists
    existing_user = User.query.filter_by(email=new_email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'This email is already in use'})
    
    # Generate OTP and send to new email
    import random
    otp_code = str(random.randint(100000, 999999))
    
    # Store the pending email change in session
    session['pending_email_change'] = {
        'new_email': new_email,
        'otp_code': otp_code,
        'user_id': user.id
    }
    
    # Send OTP to new email
    from .email_service import send_login_otp
    success, message = send_login_otp(new_email, otp_code)
    
    if success or app.debug:
        dev_otp = otp_code if app.debug else None
        return jsonify({
            'success': True, 
            'message': 'Verification code sent to your new email!',
            'redirect': url_for('verify_email_change'),
            'dev_otp': dev_otp
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to send verification email. Please try again.'})

@app.route('/verify-email-change', methods=['GET', 'POST'])
@login_required
def verify_email_change():
    if 'pending_email_change' not in session:
        flash('No pending email change found.', 'error')
        return redirect(url_for('profile'))
    
    pending = session['pending_email_change']
    new_email = pending['new_email']
    dev_otp = pending['otp_code'] if app.debug else None
    
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()
        
        if otp_code == pending['otp_code']:
            # OTP is correct, update the email
            user = User.query.get(session['user_id'])
            if user:
                user.email = new_email
                user.is_verified = True  # Already verified since they got the OTP
                user.updated_at = datetime.utcnow()
                db.session.commit()
                
                # Clear pending email change
                session.pop('pending_email_change', None)
                
                flash('Email updated successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('User not found.', 'error')
                return redirect(url_for('signin'))
        else:
            flash('Invalid verification code. Please try again.', 'error')
            return render_template('verify_email_change.html',
                                   email=new_email,
                                   dev_otp=dev_otp)
    
    return render_template('verify_email_change.html',
                           email=new_email,
                           dev_otp=dev_otp)

@app.route('/cancel-email-change')
@login_required
def cancel_email_change():
    """Cancel a pending email change"""
    session.pop('pending_email_change', None)
    flash('Email change cancelled.', 'info')
    return redirect(url_for('profile'))

@app.route('/send-email-verification', methods=['POST'])
@login_required
def send_email_verification():
    """Send OTP to user's current email for verification"""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'success': False, 'message': 'Session expired. Please sign in again.', 'redirect': url_for('signin')})
    
    if user.is_verified:
        return jsonify({'success': False, 'message': 'Your email is already verified.'})
    
    # Generate OTP
    import random
    otp_code = str(random.randint(100000, 999999))
    
    # Store in session
    session['pending_email_verification'] = {
        'email': user.email,
        'otp_code': otp_code,
        'user_id': user.id
    }
    
    # Send OTP to user's email
    from .email_service import send_login_otp
    success, message = send_login_otp(user.email, otp_code)
    
    if success or app.debug:
        dev_otp = otp_code if app.debug else None
        return jsonify({
            'success': True,
            'message': 'Verification code sent to your email!',
            'redirect': url_for('verify_current_email'),
            'dev_otp': dev_otp
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to send verification email. Please try again.'})

@app.route('/verify-current-email', methods=['GET', 'POST'])
@login_required
def verify_current_email():
    """Verify user's current email with OTP"""
    if 'pending_email_verification' not in session:
        flash('No pending email verification found.', 'error')
        return redirect(url_for('profile'))
    
    pending = session['pending_email_verification']
    email = pending['email']
    dev_otp = pending['otp_code'] if app.debug else None
    
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()
        
        if otp_code == pending['otp_code']:
            # OTP is correct, verify the email
            user = User.query.get(session['user_id'])
            if user:
                # Make sure email hasn't changed since verification was initiated
                if user.email == pending['email']:
                    user.is_verified = True
                    user.updated_at = datetime.utcnow()
                    db.session.commit()
                    
                    # Clear pending verification
                    session.pop('pending_email_verification', None)
                    
                    flash('Email verified successfully!', 'success')
                    return redirect(url_for('profile'))
                else:
                    flash('Your email has changed. Please start verification again.', 'error')
                    session.pop('pending_email_verification', None)
                    return redirect(url_for('profile'))
            else:
                flash('User not found.', 'error')
                return redirect(url_for('signin'))
        else:
            flash('Invalid verification code. Please try again.', 'error')
            return render_template('verify_current_email.html',
                                   email=email,
                                   dev_otp=dev_otp)
    
    return render_template('verify_current_email.html',
                           email=email,
                           dev_otp=dev_otp)

@app.route('/delete-account')
@login_required
def delete_account():
    user = User.query.get(session['user_id'])
    if user:
        db.session.delete(user)
        db.session.commit()
    
    session.clear()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('home'))

@app.route('/payment')
def payment():
    return render_template('payment.html')


# ==================== GREAT STEP REGISTRATION ====================

def verified_user_required(f):
    """Decorator that requires user to be logged in AND email verified"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please sign in to access this page', 'error')
            return redirect(url_for('signin'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('Session expired. Please sign in again.', 'error')
            return redirect(url_for('signin'))
        
        if not user.is_verified:
            flash('Please verify your email before registering for Great Step.', 'warning')
            return redirect(url_for('profile'))
        
        return f(*args, **kwargs)
    return decorated_function


@app.route('/great-step/register', methods=['GET', 'POST'])
@verified_user_required
def greatstep_register():
    """Great Step event registration page"""
    user = User.query.get(session['user_id'])
    
    # Check if already registered
    if user.is_greatstep_registered:
        flash('You are already registered for Great Step!', 'info')
        return redirect(url_for('profile'))
    
    # Check if there's an existing registration with completed payment
    existing_reg = GreatStepRegistration.query.filter_by(
        email=user.email, 
        payment_status='completed'
    ).first()
    if existing_reg:
        # Update user flag if somehow out of sync
        user.is_greatstep_registered = True
        db.session.commit()
        flash('You are already registered for Great Step!', 'info')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        college = request.form.get('college', '').strip()
        year = request.form.get('year', '').strip()
        
        # Validation
        if not all([first_name, last_name, mobile, college, year]):
            flash('Please fill in all required fields', 'error')
            return render_template('greatstep_register.html', user=user)
        
        if not mobile.isdigit() or len(mobile) != 10:
            flash('Please enter a valid 10-digit mobile number', 'error')
            return render_template('greatstep_register.html', user=user)
        
        # Initialize Razorpay client
        client = razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))
        
        # Create Razorpay order
        amount = Config.GREATSTEP_REGISTRATION_FEE  # Amount in paise
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': f'greatstep_{user.id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
            'notes': {
                'user_email': user.email,
                'event': 'Great Step 2025'
            }
        }
        
        print(f'[DEBUG] Creating Razorpay order with data: {order_data}')
        print(f'[DEBUG] Using Key ID: {Config.RAZORPAY_KEY_ID}')
        
        try:
            order = client.order.create(data=order_data)
            print(f'[DEBUG] Order created successfully: {order}')
        except Exception as e:
            import traceback
            print(f'[ERROR] Razorpay order creation failed: {e}')
            print(f'[ERROR] Traceback: {traceback.format_exc()}')
            flash(f'Failed to create payment order. Please try again.', 'error')
            return render_template('greatstep_register.html', user=user)
        
        # Delete any existing pending registration for this email
        GreatStepRegistration.query.filter_by(
            email=user.email,
            payment_status='pending'
        ).delete()
        
        # Create pending registration record
        registration = GreatStepRegistration(
            email=user.email,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            college=college,
            year=year,
            razorpay_order_id=order['id'],
            amount_paid=amount,
            payment_status='pending'
        )
        db.session.add(registration)
        db.session.commit()
        
        # Render payment page with Razorpay checkout
        return render_template('greatstep_payment.html',
                               user=user,
                               registration=registration,
                               order=order,
                               razorpay_key_id=Config.RAZORPAY_KEY_ID,
                               amount_display=amount // 100)  # Convert paise to rupees for display
    
    return render_template('greatstep_register.html', user=user)


@app.route('/great-step/payment/verify', methods=['POST'])
@verified_user_required
def greatstep_payment_verify():
    """Verify Razorpay payment signature and complete registration"""
    user = User.query.get(session['user_id'])
    
    # Get payment details from request
    razorpay_order_id = request.form.get('razorpay_order_id')
    razorpay_payment_id = request.form.get('razorpay_payment_id')
    razorpay_signature = request.form.get('razorpay_signature')
    
    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        flash('Invalid payment response. Please try again.', 'error')
        return redirect(url_for('greatstep_register'))
    
    # Find the registration record
    registration = GreatStepRegistration.query.filter_by(
        razorpay_order_id=razorpay_order_id,
        email=user.email
    ).first()
    
    if not registration:
        flash('Registration not found. Please try again.', 'error')
        return redirect(url_for('greatstep_register'))
    
    # Verify signature
    try:
        # Generate expected signature
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        expected_signature = hmac.new(
            Config.RAZORPAY_KEY_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if expected_signature != razorpay_signature:
            registration.payment_status = 'failed'
            db.session.commit()
            flash('Payment verification failed. Please contact support.', 'error')
            return redirect(url_for('greatstep_payment_failure'))
        
        # Payment verified successfully
        registration.razorpay_payment_id = razorpay_payment_id
        registration.razorpay_signature = razorpay_signature
        registration.payment_status = 'completed'
        registration.payment_completed_at = datetime.utcnow()
        
        # Update user's registration status
        user.is_greatstep_registered = True
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Registration successful! Welcome to Great Step 2025!', 'success')
        return redirect(url_for('greatstep_payment_success'))
        
    except Exception as e:
        print(f'[ERROR] Payment verification error: {e}')
        registration.payment_status = 'failed'
        db.session.commit()
        flash('Payment verification error. Please contact support.', 'error')
        return redirect(url_for('greatstep_payment_failure'))


@app.route('/great-step/payment/success')
@verified_user_required
def greatstep_payment_success():
    """Payment success page"""
    user = User.query.get(session['user_id'])
    registration = GreatStepRegistration.query.filter_by(
        email=user.email,
        payment_status='completed'
    ).order_by(GreatStepRegistration.created_at.desc()).first()
    
    return render_template('greatstep_success.html', user=user, registration=registration)


@app.route('/great-step/payment/failure')
@verified_user_required
def greatstep_payment_failure():
    """Payment failure page"""
    return render_template('greatstep_failure.html')


if __name__ == '__main__':
    app.run(debug=True)
