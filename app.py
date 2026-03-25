from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from database import db
from otp_service import otp_service
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Database will be initialized on first request
db_initialized = False

def init_db_if_needed():
    global db_initialized
    if not db_initialized:
        try:
            db.init_db()
            db_initialized = True
            print("✅ Database initialized successfully!")
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize database: {e}")
            print("Database will be initialized when first accessed.")

@app.route('/')
def index():
    """Home page"""
    init_db_if_needed()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login - just name and email"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        if not name or not email:
            flash('Please provide both name and email', 'error')
            return render_template('login.html')
        
        # Save voter info
        try:
            db.save_voter(name, email)
            
            # Generate and send OTP
            otp = otp_service.generate_otp()
            otp_service.save_otp(email, otp)
            success, message = otp_service.send_otp_email(email, name, otp)
            
            if success:
                # Store user info in session
                session['email'] = email
                session['name'] = name
                session['otp_verified'] = False
                
                flash(message, 'success')
                return redirect(url_for('verify_otp'))
            else:
                flash(message, 'error')
                return render_template('login.html')
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """OTP verification page"""
    if 'email' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        
        if not otp:
            flash('Please enter OTP', 'error')
            return render_template('verify_otp.html')
        
        email = session['email']
        success, message = otp_service.verify_otp(email, otp)
        
        if success:
            session['otp_verified'] = True
            flash(message, 'success')
            return redirect(url_for('vote'))
        else:
            flash(message, 'error')
            return render_template('verify_otp.html')
    
    return render_template('verify_otp.html')

@app.route('/resend-otp')
def resend_otp():
    """Resend OTP to user"""
    if 'email' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    email = session['email']
    name = session['name']
    
    success, message = otp_service.resend_otp(email, name)
    flash(message, 'success' if success else 'error')
    
    return redirect(url_for('verify_otp'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    """Voting page"""
    # Check if user is logged in and OTP verified
    if 'email' not in session or not session.get('otp_verified'):
        flash('Please login and verify OTP first', 'error')
        return redirect(url_for('login'))
    
    email = session['email']
    
    # Check if already voted
    if db.check_if_voted(email):
        flash('You have already voted!', 'warning')
        return redirect(url_for('results'))
    
    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        
        if not candidate_id:
            flash('Please select a candidate', 'error')
            candidates = db.get_candidates()
            return render_template('vote.html', candidates=candidates)
        
        # Record vote
        success, message = db.record_vote(email, int(candidate_id))
        
        if success:
            flash(message, 'success')
            return redirect(url_for('results'))
        else:
            flash(message, 'error')
            candidates = db.get_candidates()
            return render_template('vote.html', candidates=candidates)
    
    # GET request - show voting form
    candidates = db.get_candidates()
    return render_template('vote.html', candidates=candidates)

@app.route('/results')
def results():
    """Display voting results"""
    results, total_votes = db.get_results()
    return render_template('results.html', results=results, total_votes=total_votes)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
