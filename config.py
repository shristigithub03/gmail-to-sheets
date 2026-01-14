import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API KEY (GET FROM GOOGLE CLOUD)
API_KEY = "AIzaSyCwAjDBZpEyX9FYxncheo91bGnvVBxB9fQ"  # ⚠️ REPLACE WITH YOUR ACTUAL API KEY

# Google Sheet Configuration
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # ⚠️ REPLACE WITH YOUR ACTUAL SHEET ID
SHEET_NAME = "Processed_Emails"

# Processing Configuration
MAX_EMAILS = 5  # Process 5 emails per run for demo
STATE_FILE = os.path.join(BASE_DIR, 'last_processed.json')

# Demo mode (set to False for real implementation with OAuth)
DEMO_MODE = True