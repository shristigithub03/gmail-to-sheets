import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from src.gmail_service import GmailService
from src.sheets_service import SheetsService
from src.email_parser import EmailParser
from src.state_manager import StateManager

def main():
    print("=" * 70)
    print("📧 GMAIL TO GOOGLE SHEETS AUTOMATION")
    print("🎯 COMPLETE WORKING PROTOTYPE")
    print("=" * 70)
    print(f"📁 Config: API Key = {API_KEY[:20]}...")
    print(f"📊 Sheet ID: {SPREADSHEET_ID}")
    print(f"🔧 Demo Mode: {DEMO_MODE}")
    print("=" * 70)
    
    # Initialize services
    print("\n[1/4] 🔐 Initializing services...")
    gmail = GmailService(API_KEY, demo_mode=DEMO_MODE)
    sheets = SheetsService(API_KEY)
    
    print("[2/4] 💾 Loading state manager...")
    state = StateManager(STATE_FILE)
    
    print("[3/4] 📧 Fetching emails...")
    messages = gmail.get_unread_emails(MAX_EMAILS)
    
    if not messages:
        print("⚠️ No emails to process.")
        return
    
    print(f"📨 Processing {len(messages)} email(s)...")
    print("-" * 70)
    
    # Process emails
    processed = 0
    failed = 0
    
    for msg in messages:
        msg_id = msg['id']
        
        # Check for duplicates
        if state.is_processed(msg_id):
            print(f"⏭️  Skipped (already processed): {msg_id}")
            continue
        
        print(f"📝 Processing: {msg_id}")
        
        # Get email details
        email_raw = gmail.get_email_details(msg_id)
        if not email_raw:
            print(f"   ❌ Failed to get email details")
            failed += 1
            continue
        
        # Parse email
        email_data = EmailParser.parse_email(email_raw)
        if not email_data:
            print(f"   ❌ Failed to parse email")
            failed += 1
            continue
        
        # Append to Google Sheets
        result = sheets.append_data(SPREADSHEET_ID, SHEET_NAME, email_data)
        
        if result:
            # Mark as read
            gmail.mark_as_read(msg_id)
            
            # Update state
            state.add_processed_id(msg_id)
            processed += 1
            
            print(f"   ✅ Successfully processed")
            print(f"   📨 From: {email_data.get('from', 'N/A')}")
            print(f"   📝 Subject: {email_data.get('subject', 'N/A')[:40]}")
        else:
            failed += 1
            print(f"   ❌ Failed to save to sheet")
        
        print()
    
    # Summary
    print("=" * 70)
    if processed > 0:
        print(f"✅ SUCCESS: {processed} email(s) processed and saved to Google Sheets")
    else:
        print("⚠️ No emails were processed")
    
    if failed > 0:
        print(f"⚠️ {failed} email(s) failed to process")
    
    print(f"📊 Total emails in database: {len(state.state['processed_ids'])}")
    print(f"💾 State file: {STATE_FILE}")
    print("=" * 70)
    
    # Implementation notes
    if DEMO_MODE:
        print("\n📋 IMPLEMENTATION NOTES:")
        print("✅ Working prototype with complete architecture")
        print("✅ API Key authentication for Google Sheets")
        print("✅ Mock data for Gmail (OAuth verification pending)")
        print("✅ Duplicate prevention with state management")
        print("✅ Ready for OAuth 2.0 integration")
        print("\n🔧 For production: Enable OAuth 2.0 with gmail.modify scope")

if __name__ == '__main__':
    main()