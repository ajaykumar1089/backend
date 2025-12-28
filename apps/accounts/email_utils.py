from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_verification_email(user):
    """Send email verification email to user"""
    
    # Use existing verification token (should be generated before calling this function)
    token = user.verification_token
    
    # If no token exists, generate one
    if not token:
        token = user.generate_verification_token()
        user.save(update_fields=['verification_token', 'verification_token_expires'])
    
    # Create verification URL
    verification_url = f"{settings.SITE_URL}/auth/verify?token={token}"
    
    # Email context
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'TravellerClicks',
    }
    
    # Email subject
    subject = 'Verify your TravellerClicks account'
    
    # Create email content (HTML version)
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Verification</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #1976d2; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .button {{ display: inline-block; padding: 12px 24px; background-color: #1976d2; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }}
            .footer {{ padding: 20px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to TravellerClicks!</h1>
            </div>
            <div class="content">
                <h2>Hi {user.username}!</h2>
                <p>Thank you for registering with TravellerClicks. To complete your registration and activate your account, please verify your email address.</p>
                
                <p>Click the button below to verify your email:</p>
                
                <a href="{verification_url}" class="button">Verify Email Address</a>
                
                <p>If the button above doesn't work, you can also copy and paste this link into your browser:</p>
                <p><a href="{verification_url}">{verification_url}</a></p>
                
                <p><strong>Note:</strong> This verification link will expire in 24 hours for security reasons.</p>
                
                <p>If you didn't create an account with TravellerClicks, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>© 2025 TravellerClicks. All rights reserved.</p>
                <p>This is an automated email. Please do not reply to this message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    plain_message = f"""
    Welcome to TravellerClicks!
    
    Hi {user.username}!
    
    Thank you for registering with TravellerClicks. To complete your registration and activate your account, please verify your email address.
    
    Please click on the following link to verify your email:
    {verification_url}
    
    Note: This verification link will expire in 24 hours for security reasons.
    
    If you didn't create an account with TravellerClicks, please ignore this email.
    
    © 2025 TravellerClicks. All rights reserved.
    """
    
    try:
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send verification email to {user.email}: {str(e)}")
        return False


def send_welcome_email(user):
    """Send welcome email after successful verification"""
    subject = 'Welcome to TravellerClicks - Your Account is Active!'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to TravellerClicks</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4caf50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 30px; background-color: #f9f9f9; }}
            .button {{ display: inline-block; padding: 12px 24px; background-color: #1976d2; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Account Verified Successfully!</h1>
            </div>
            <div class="content">
                <h2>Welcome to TravellerClicks, {user.username}!</h2>
                <p>Congratulations! Your email has been successfully verified and your account is now active.</p>
                
                <p>You can now:</p>
                <ul>
                    <li>Browse and book bikes, cars, and campervans</li>
                    <li>Find amazing hotels and accommodations</li>
                    <li>Share your travel stories</li>
                    <li>Connect with fellow travelers</li>
                </ul>
                
                <a href="{settings.SITE_URL}/auth/login" class="button">Login to Your Account</a>
                
                <p>Thank you for joining our community of travel enthusiasts!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Account Verified Successfully!
    
    Welcome to TravellerClicks, {user.username}!
    
    Congratulations! Your email has been successfully verified and your account is now active.
    
    You can now login and start exploring our platform at: {settings.SITE_URL}/auth/login
    
    Thank you for joining our community of travel enthusiasts!
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False