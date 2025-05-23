# Financial Application with Gradio

This is a web application built with Gradio that includes authentication (login and registration) features with SQLite database integration, as well as a comprehensive user financial profile system.

## Features

- User registration with email, username, and password
- Secure password storage using salt and hash
- User login authentication
- Comprehensive financial user profile
- Dashboard interface after successful login
- SQLite database for data persistence

## User Profile Information

The application collects detailed financial profile information including:

- Basic information (name, age)
- Investment experience
- Financial goals and timeline
- Risk tolerance and income level
- Portfolio preferences and asset preferences
- Investment frequency
- Behavioral profile (emotional state, loss reaction)
- Financial literacy and confidence
- Decision-making style
- Information consumption preferences
- Trust in AI advisors

This information is used to provide personalized financial recommendations and advice.

## Requirements

- Python 3.6+
- Gradio
- SQLite3

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install gradio
```

## Usage

1. Run the application:

```bash
python app.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually http://127.0.0.1:7860)
3. Register a new account or login with existing credentials
4. After successful login, you'll be redirected to the dashboard
5. Complete your financial profile
6. Access your financial dashboard with personalized recommendations

## Project Structure

- `app.py`: Main application file with Gradio interface
- `database.py`: Database handling, user authentication and profile management
- `users.db`: SQLite database file (created automatically on first run)

## Customization

You can extend the dashboard with additional functionality by modifying the dashboard section in `app.py`. #   L L M - S E N G - P R O J E C T  
 