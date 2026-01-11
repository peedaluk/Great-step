"""
Email Service using Brevo (formerly Sendinblue)
Handles sending OTP emails for verification, login, and password reset
"""
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import current_app
import os


def is_dev_mode():
    """Check if we're in development mode (no real email sending)"""
    api_key = current_app.config.get('BREVO_API_KEY') or os.getenv('BREVO_API_KEY', '')
    # Dev mode if no API key or placeholder value
    return not api_key or api_key == 'your-brevo-api-key-here'


def get_api_instance():
    """Get configured Brevo API instance"""
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = current_app.config.get('BREVO_API_KEY') or os.getenv('BREVO_API_KEY')
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_email(to_email, subject, html_content, otp_code=None):
    """
    Send an email using Brevo
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        otp_code: OTP code (for dev mode logging)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Development mode - skip actual email sending
    if is_dev_mode():
        current_app.logger.info(f"[DEV MODE] Email to: {to_email}")
        current_app.logger.info(f"[DEV MODE] Subject: {subject}")
        if otp_code:
            current_app.logger.info(f"[DEV MODE] OTP Code: {otp_code}")
            print(f"\n{'='*50}")
            print(f"[DEV MODE] OTP for {to_email}: {otp_code}")
            print(f"{'='*50}\n")
        return True, "Email sent (dev mode)"
    
    try:
        api_instance = get_api_instance()
        
        sender_email = current_app.config.get('SENDER_EMAIL') or os.getenv('SENDER_EMAIL', 'noreply@tmes.in')
        sender_name = current_app.config.get('SENDER_NAME') or os.getenv('SENDER_NAME', 'TMES IIT Kharagpur')
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": sender_name, "email": sender_email},
            subject=subject,
            html_content=html_content
        )
        
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True, "Email sent successfully"
        
    except ApiException as e:
        error_msg = f"Brevo API Error: {e}"
        current_app.logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Email Error: {str(e)}"
        current_app.logger.error(error_msg)
        return False, error_msg


def get_otp_email_template(otp_code, purpose="verification"):
    """
    Generate HTML email template for OTP
    
    Args:
        otp_code: The OTP code to include
        purpose: Purpose of OTP (verification, login, reset)
    
    Returns:
        str: HTML email content
    """
    purpose_text = {
        "verification": "verify your email address",
        "login": "complete your login",
        "reset": "reset your password"
    }
    
    action_text = purpose_text.get(purpose, "complete your request")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td align="center" style="padding: 40px 0;">
                    <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 30px; background: linear-gradient(135deg, #0E2E50 0%, #1a4a7a 100%); border-radius: 10px 10px 0 0; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">TMES IIT Kharagpur</h1>
                                <p style="color: #94c2f5; margin: 10px 0 0 0; font-size: 14px;">The Mining Engineering Society</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="color: #0E2E50; margin: 0 0 20px 0; font-size: 22px;">Your Verification Code</h2>
                                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                    Please use the following OTP to {action_text}. This code is valid for <strong>10 minutes</strong>.
                                </p>
                                
                                <!-- OTP Code -->
                                <div style="text-align: center; margin: 30px 0;">
                                    <div style="display: inline-block; background: linear-gradient(135deg, #0E2E50 0%, #1a4a7a 100%); padding: 20px 40px; border-radius: 10px;">
                                        <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #ffffff;">{otp_code}</span>
                                    </div>
                                </div>
                                
                                <p style="color: #888888; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0;">
                                    If you didn't request this code, please ignore this email. Do not share this OTP with anyone.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background-color: #f8f9fa; border-radius: 0 0 10px 10px; text-align: center;">
                                <p style="color: #888888; font-size: 12px; margin: 0;">
                                    © 2024 TMES IIT Kharagpur. All rights reserved.
                                </p>
                                <p style="color: #aaaaaa; font-size: 11px; margin: 10px 0 0 0;">
                                    This is an automated message. Please do not reply to this email.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def send_verification_email(email, otp_code):
    """
    Send email verification OTP during signup
    
    Args:
        email: User's email address
        otp_code: Generated OTP code
    
    Returns:
        tuple: (success: bool, message: str)
    """
    subject = "Verify Your Email - TMES IIT Kharagpur"
    html_content = get_otp_email_template(otp_code, "verification")
    return send_email(email, subject, html_content, otp_code)


def send_login_otp(email, otp_code):
    """
    Send login OTP for two-factor authentication
    
    Args:
        email: User's email address
        otp_code: Generated OTP code
    
    Returns:
        tuple: (success: bool, message: str)
    """
    subject = "Login Verification - TMES IIT Kharagpur"
    html_content = get_otp_email_template(otp_code, "login")
    return send_email(email, subject, html_content, otp_code)


def send_reset_password_email(email, otp_code):
    """
    Send password reset OTP
    
    Args:
        email: User's email address
        otp_code: Generated OTP code
    
    Returns:
        tuple: (success: bool, message: str)
    """
    subject = "Password Reset - TMES IIT Kharagpur"
    html_content = get_otp_email_template(otp_code, "reset")
    return send_email(email, subject, html_content, otp_code)
