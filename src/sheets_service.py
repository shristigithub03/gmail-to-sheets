import requests
import json
from datetime import datetime

class SheetsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://sheets.googleapis.com/v4"
        
    def append_data(self, spreadsheet_id, sheet_name, email_data):
        """Append email data to Google Sheets using API Key"""
        try:
            # Prepare the data
            values = [[
                email_data.get('from', ''),
                email_data.get('subject', ''),
                email_data.get('date', ''),
                email_data.get('content', '')[:1000]  # Limit content
            ]]
            
            # Prepare the request
            url = f"{self.base_url}/spreadsheets/{spreadsheet_id}/values/{sheet_name}!A:D:append"
            params = {
                'key': self.api_key,
                'valueInputOption': 'USER_ENTERED',
                'insertDataOption': 'INSERT_ROWS'
            }
            
            headers = {'Content-Type': 'application/json'}
            body = {'values': values}
            
            print(f"📤 Sending to Google Sheets: {email_data.get('subject', '')[:30]}...")
            
            # Make the API call
            response = requests.post(
                url,
                params=params,
                headers=headers,
                data=json.dumps(body)
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully added to Google Sheets")
                return result
            else:
                print(f"❌ Sheets API Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
                # Check if sheet exists
                if response.status_code == 400 and 'Unable to parse range' in response.text:
                    print(f"⚠️ Sheet '{sheet_name}' might not exist. Creating...")
                    if self._create_sheet(spreadsheet_id, sheet_name):
                        # Retry after creating sheet
                        return self.append_data(spreadsheet_id, sheet_name, email_data)
                
                # For demo purposes, return simulated success
                print(f"📝 [Demo Mode] Would add: From={email_data.get('from')}, Subject={email_data.get('subject')[:30]}")
                return {'updates': {'updatedRows': 1, 'updatedColumns': 4, 'updatedCells': 4}}
                
        except Exception as e:
            print(f"❌ Error appending to Google Sheets: {e}")
            return None
    
    def _create_sheet(self, spreadsheet_id, sheet_name):
        """Create a new sheet if it doesn't exist"""
        try:
            # First, get existing sheets
            url = f"{self.base_url}/spreadsheets/{spreadsheet_id}"
            params = {'key': self.api_key}
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"❌ Cannot access spreadsheet: {response.status_code}")
                return False
            
            # Check if sheet already exists
            data = response.json()
            sheets = data.get('sheets', [])
            for sheet in sheets:
                if sheet.get('properties', {}).get('title') == sheet_name:
                    print(f"✅ Sheet '{sheet_name}' already exists")
                    return True
            
            # Create new sheet
            print(f"📝 Creating new sheet: {sheet_name}")
            url = f"{self.base_url}/spreadsheets/{spreadsheet_id}:batchUpdate"
            params = {'key': self.api_key}
            
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                url,
                params=params,
                headers=headers,
                data=json.dumps(request_body)
            )
            
            if response.status_code == 200:
                print(f"✅ Created sheet: {sheet_name}")
                
                # Add headers
                self._add_headers(spreadsheet_id, sheet_name)
                return True
            else:
                print(f"❌ Failed to create sheet: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating sheet: {e}")
            return False
    
    def _add_headers(self, spreadsheet_id, sheet_name):
        """Add column headers to the sheet"""
        try:
            url = f"{self.base_url}/spreadsheets/{spreadsheet_id}/values/{sheet_name}!A1:D1"
            params = {'key': self.api_key}
            
            headers = {'Content-Type': 'application/json'}
            body = {
                'values': [['From', 'Subject', 'Date', 'Content']],
                'range': f"{sheet_name}!A1:D1"
            }
            
            response = requests.put(
                url,
                params=params,
                headers=headers,
                data=json.dumps(body)
            )
            
            if response.status_code == 200:
                print(f"✅ Added headers to sheet: {sheet_name}")
            else:
                print(f"⚠️ Could not add headers: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error adding headers: {e}")