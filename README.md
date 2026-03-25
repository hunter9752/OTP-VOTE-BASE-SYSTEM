# 🗳️ VoteSecure - Modern OTP-Based Voting System

A secure, modern electronic voting system built with Python Flask and PostgreSQL (Supabase). Features a beautiful glassmorphism UI with smooth animations and OTP authentication for secure voting.

## ✨ Features

- 🎨 **Modern UI/UX**: Glassmorphism design with smooth animations
- 🔐 **OTP Authentication**: Email-based OTP verification for security
- 🗳️ **Multiple Parties**: Vote for BJP, Congress, AAP, or NOTA
- 🛡️ **Duplicate Prevention**: Each user can vote only once
- 📊 **Live Results**: Real-time vote counting with animated progress bars
- 🎉 **Celebrations**: Confetti animation on successful vote
- 📱 **Responsive**: Mobile-first design that works on all devices
- ♿ **Accessible**: ARIA labels and keyboard navigation support

## 🎨 Design Features

- **Glassmorphism UI**: Modern frosted glass effect with backdrop blur
- **Gradient Backgrounds**: Animated gradient backgrounds with particle effects
- **Smooth Animations**: Entrance animations, hover effects, and transitions
- **Interactive Elements**: 3D card effects, ripple buttons, animated progress bars
- **Google Fonts**: Inter for body text, Poppins for headings
- **Font Awesome Icons**: Beautiful icons throughout the interface
- **Confetti Celebration**: Animated confetti when vote is successfully cast
- **Auto-dismiss Alerts**: Notifications that fade out automatically

## 🚀 Tech Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL (Supabase)
- **Frontend**: HTML5, CSS3 (Modern CSS with Variables), JavaScript (ES6+)
- **Fonts**: Google Fonts (Inter, Poppins)
- **Icons**: Font Awesome 6
- **Animations**: Canvas Confetti, CSS Keyframes
- **Authentication**: Email-based OTP

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "c:\SIDDHI PROJECT"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - The database URL is already configured in `config.py`
   - For email OTP, update SMTP settings in `.env` (optional - uses console output by default)

4. **Initialize the database**:
   The database tables will be created automatically when you first run the app.

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   Open your browser and go to: `http://localhost:5000`

3. **Voting Flow**:
   - Enter your name and email on the login page
   - Check console/terminal for OTP (in testing mode)
   - Enter the 6-digit OTP
   - Select your preferred candidate (BJP, Congress, AAP, or NOTA)
   - Submit your vote
   - View the live results

## Project Structure

```
SIDDHI PROJECT/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database operations
├── otp_service.py         # OTP generation and email
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with modern nav
│   ├── index.html        # Homepage with features
│   ├── login.html        # Login form
│   ├── verify_otp.html   # OTP verification
│   ├── vote.html         # Voting interface
│   └── results.html      # Results dashboard
└── static/              # Static assets
    ├── style.css         # Modern CSS with glassmorphism
    ├── script.js         # Interactive JavaScript
    ├── AAP.jpeg          # Party logos
    ├── BJP.jpeg
    ├── CONGRSS.png
    └── NOTa.png
```

## Configuration

### Testing Mode (Default)
- OTP is printed to console instead of sending email
- Set `TESTING_MODE=True` in `.env`

### Production Mode
- Set `TESTING_MODE=False` in `.env`
- Configure SMTP settings in `.env`:
  ```
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=your-email@gmail.com
  SMTP_PASSWORD=your-app-password
  ```

## Security Features

- ✅ OTP-based authentication
- ✅ 5-minute OTP expiry
- ✅ Session management
- ✅ Duplicate voting prevention
- ✅ Email verification

## Candidates

The system includes the following parties:
1. **BJP** (Bharatiya Janata Party) - 🪷
2. **Congress** (Indian National Congress) - ✋
3. **AAP** (Aam Aadmi Party) - 🧹
4. **NOTA** (None of the Above) - ❌

## License

This is a student project for educational purposes.

## Support

For issues or questions, check the code comments or modify the system as needed.
