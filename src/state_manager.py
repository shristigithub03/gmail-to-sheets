import json
import os
from datetime import datetime

class StateManager:
    def __init__(self, state_file):
        self.state_file = state_file
        self.state = self.load_state()
    
    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return {'processed_ids': [], 'last_run': None}
        return {'processed_ids': [], 'last_run': None}
    
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def add_processed_id(self, email_id):
        if email_id not in self.state['processed_ids']:
            self.state['processed_ids'].append(email_id)
            self.state['last_run'] = datetime.now().isoformat()
            self.save_state()
    
    def is_processed(self, email_id):
        return email_id in self.state['processed_ids']