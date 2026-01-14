import base64
import re
from email.utils import parseaddr
from bs4 import BeautifulSoup
import dateutil.parser

class EmailParser:
    @staticmethod
    def parse_email(msg):
        headers = msg['payload']['headers']
        email_data = {
            'id': msg['id'],
            'from': '',
            'subject': '',
            'date': '',
            'content': ''
        }
        
        # Extract headers
        for header in headers:
            name = header['name'].lower()
            if name == 'from':
                email_data['from'] = parseaddr(header['value'])[1]
            elif name == 'subject':
                email_data['subject'] = header['value']
            elif name == 'date':
                try:
                    email_data['date'] = dateutil.parser.parse(header['value']).isoformat()
                except:
                    email_data['date'] = header['value']
        
        # Extract body
        email_data['content'] = EmailParser.extract_body(msg['payload'])
        return email_data
    
    @staticmethod
    def extract_body(payload):
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                mime_type = part['mimeType']
                if 'body' in part and 'data' in part['body']:
                    data = part['body']['data']
                    if data:
                        decoded = base64.urlsafe_b64decode(data).decode('utf-8')
                        if mime_type == 'text/plain':
                            body += decoded
                        elif mime_type == 'text/html':
                            soup = BeautifulSoup(decoded, 'html.parser')
                            body += soup.get_text()
        
        elif 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        # Clean up
        body = re.sub(r'\s+', ' ', body).strip()
        return body[:5000]  # Limit to 5000 chars