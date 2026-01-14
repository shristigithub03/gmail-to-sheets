import requests
import base64
import json
from datetime import datetime

class GmailService:
    def __init__(self, api_key, demo_mode=True):
        self.api_key = api_key
        self.demo_mode = demo_mode
        self.base_url = "https://gmail.googleapis.com/gmail/v1"
        
    def get_unread_emails(self, max_results=5):
        """Get unread emails - uses real API if available, mock data for demo"""
        if self.demo_mode:
            print("🔍 [DEMO MODE] Fetching mock emails...")
            return self._get_mock_emails(max_results)
        else:
            # Real API call (requires OAuth token)
            print("📧 Fetching real emails from Gmail API...")
            return self._get_real_emails(max_results)
    
    def _get_real_emails(self, max_results):
        """Real Gmail API call (requires OAuth - for future implementation)"""
        try:
            url = f"{self.base_url}/users/me/messages"
            params = {
                'key': self.api_key,
                'labelIds': ['INBOX', 'UNREAD'],
                'maxResults': max_results
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                emails = data.get('messages', [])
                print(f"✅ Found {len(emails)} real unread emails")
                return emails
            else:
                print(f"⚠️ Gmail API returned {response.status_code}. Using demo data.")
                return self._get_mock_emails(max_results)
                
        except Exception as e:
            print(f"❌ Error accessing Gmail API: {e}")
            return self._get_mock_emails(max_results)
    
    def _get_mock_emails(self, max_results):
        """Generate mock email data for demonstration"""
        mock_emails = []
        for i in range(1, max_results + 1):
            mock_emails.append({
                'id': f'mock_email_{i:03d}',
                'threadId': f'thread_{i:03d}'
            })
        print(f"📧 Generated {len(mock_emails)} mock emails for demonstration")
        return mock_emails
    
    def get_email_details(self, msg_id):
        """Get email details - mock for demo"""
        if self.demo_mode:
            return self._get_mock_email_details(msg_id)
        else:
            # Real implementation would go here
            pass
    
    def _get_mock_email_details(self, msg_id):
        """Create realistic mock email data"""
        mock_data = {
            'mock_email_001': {
                'id': 'mock_email_001',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': 'support@example.com'},
                        {'name': 'Subject', 'value': 'Welcome to Our Service'},
                        {'name': 'Date', 'value': 'Mon, 13 Jan 2026 09:30:00 +0530'}
                    ],
                    'body': {'data': base64.b64encode(b'Thank you for signing up! We are excited to have you.').decode()}
                }
            },
            'mock_email_002': {
                'id': 'mock_email_002',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': 'newsletter@technews.com'},
                        {'name': 'Subject', 'value': 'Weekly Tech Digest'},
                        {'name': 'Date', 'value': 'Mon, 13 Jan 2026 10:15:00 +0530'}
                    ],
                    'body': {'data': base64.b64encode(b'Top stories this week: AI advancements, cloud computing trends, and more.').decode()}
                }
            },
            'mock_email_003': {
                'id': 'mock_email_003',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': 'order@amazon.com'},
                        {'name': 'Subject', 'value': 'Your Order #12345 has shipped'},
                        {'name': 'Date', 'value': 'Mon, 13 Jan 2026 11:45:00 +0530'}
                    ],
                    'body': {'data': base64.b64encode(b'Your order is on the way. Estimated delivery: Jan 15, 2026.').decode()}
                }
            },
            'mock_email_004': {
                'id': 'mock_email_004',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': 'alerts@github.com'},
                        {'name': 'Subject', 'value': 'Repository activity summary'},
                        {'name': 'Date', 'value': 'Mon, 13 Jan 2026 12:30:00 +0530'}
                    ],
                    'body': {'data': base64.b64encode(b'Your repositories had 15 commits in the last 24 hours.').decode()}
                }
            },
            'mock_email_005': {
                'id': 'mock_email_005',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': 'invoice@payments.com'},
                        {'name': 'Subject', 'value': 'Invoice #INV-2026-001'},
                        {'name': 'Date', 'value': 'Mon, 13 Jan 2026 14:20:00 +0530'}
                    ],
                    'body': {'data': base64.b64encode(b'Please find attached your monthly invoice. Amount due: $99.99.').decode()}
                }
            }
        }
        
        # Return specific mock email or default
        return mock_data.get(msg_id, mock_data['mock_email_001'])
    
    def mark_as_read(self, msg_id):
        """Mark email as read - simulated for demo"""
        print(f"✅ [Simulated] Marked email {msg_id} as read")
        return True  # Simulate success