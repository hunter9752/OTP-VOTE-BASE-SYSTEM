import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import Config

class OTPService:
    def __init__(self):
        self.otp_storage = {}  # Format: {email: {'otp': '123456', 'expiry': datetime}}
    
    def generate_otp(self):
        """Generate a 6-digit random OTP"""
        return str(random.randint(100000, 999999))
    
    def save_otp(self, email, otp):
        """Save OTP with expiry time"""
        expiry = datetime.now() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)
        self.otp_storage[email] = {
            'otp': otp,
            'expiry': expiry
        }
    
    def verify_otp(self, email, otp):
        """Verify if the OTP is correct and not expired"""
        if email not in self.otp_storage:
            return False, "No OTP found for this email. Please request a new OTP."
        
        stored_data = self.otp_storage[email]
        
        # Check if expired
        if datetime.now() > stored_data['expiry']:
            del self.otp_storage[email]
            return False, "OTP has expired. Please request a new OTP."
        
        # Check if OTP matches
        if stored_data['otp'] != otp:
            return False, "Invalid OTP. Please try again."
        
        # OTP is valid, remove it from storage
        del self.otp_storage[email]
        return True, "OTP verified successfully!"
    
    def send_otp_email(self, email, name, otp):
        """Send OTP via email or print to console in testing mode"""
        
        if Config.TESTING_MODE:
            # Testing mode - print to console
            print("\n" + "="*50)
            print(f"📧 OTP EMAIL (Testing Mode)")
            print("="*50)
            print(f"To: {email}")
            print(f"Name: {name}")
            print(f"OTP: {otp}")
            print(f"Valid for: {Config.OTP_EXPIRY_MINUTES} minutes")
            print("="*50 + "\n")
            return True, "OTP sent successfully (check console)"
        
        # Production mode - send actual email
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.SMTP_FROM_EMAIL
            msg['To'] = email
            msg['Subject'] = "Your OTP for Online Voting System"
            
            body = f"""
            <html>
            <body>
                <h2>Hello {name}!</h2>
                <p>Your OTP for the Online Voting System is:</p>
                <h1 style="color: #4CAF50; font-size: 32px;">{otp}</h1>
                <p>This OTP is valid for {Config.OTP_EXPIRY_MINUTES} minutes.</p>
                <p>Please do not share this OTP with anyone. this system is made by Siddhi and her team</p>
                <br>
                <p>Thank you for voting!</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Connect to SMTP server and send
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            return True, "OTP sent successfully to your email"
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False, f"Failed to send OTP: {str(e)}"
    
    def resend_otp(self, email, name):
        """Generate and send a new OTP"""
        otp = self.generate_otp()
        self.save_otp(email, otp)
        return self.send_otp_email(email, name, otp)

# Global OTP service instance
otp_service = OTPService()
