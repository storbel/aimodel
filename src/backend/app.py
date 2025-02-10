# src/backend/app.py
from flask import Flask, request, jsonify
from settings.settings_manager import SettingsManager
import yaml
import os

app = Flask(__name__)
settings_manager = SettingsManager()

@app.route('/settings', methods=['GET'])
def get_settings():
    return jsonify(settings_manager.get_settings())

@app.route('/settings', methods=['POST'])
def update_settings():
    new_settings = request.get_json()
    try:
        settings_manager.update_settings(new_settings)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/settings/validate', methods=['POST'])
def validate_settings():
    settings = request.get_json()
    validation_result = settings_manager.validate_settings(settings)
    return jsonify(validation_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# src/backend/settings/settings_manager.py
class SettingsManager:
    def __init__(self, config_path="/config/settings.yaml"):
        self.config_path = config_path
        
    def get_settings(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
            
    def update_settings(self, new_settings):
        self.validate_settings(new_settings)
        with open(self.config_path, 'w') as f:
            yaml.dump(new_settings, f)
            
    def validate_settings(self, settings):
        required_keys = ['document_sources', 'extraction', 'preprocessing', 
                        'vectorization', 'faiss', 'chatbot']
        
        errors = []
        for key in required_keys:
            if key not in settings:
                errors.append(f"Missing required section: {key}")
                
        return {"valid": len(errors) == 0, "errors": errors}