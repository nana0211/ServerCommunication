from flask import Flask, request, jsonify, send_file
import json
import pandas as pd
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import NormCreate

app = Flask(__name__)

# Ensure the folders exist
os.makedirs('database', exist_ok=True)
# Ensure the base directory exists
BASE_DIR = 'device_data'
os.makedirs(BASE_DIR, exist_ok=True)

#Helper Function 
def clear_new_folder(dir):
    """Delete all files in the 'new' folder."""
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
@app.route('/get_message', methods=['GET'])
def get_message():
    return "Hello from server"

@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        #Clear the folder
        # Get the device ID from headers
        device_id = request.headers.get('Device-ID')
        if not device_id:
            return jsonify({"error": "Device ID not provided"}), 400
        
        app.logger.info(f"Received request from device: {device_id}")
        
        # Create a unique folder for the device if it doesn't exist
        device_folder = os.path.join(BASE_DIR, device_id)
        os.makedirs(device_folder, exist_ok=True)
        
        clear_new_folder(device_folder)
        
        # Get the JSON data from the request
        json_data = request.json
        app.logger.info(f"Received JSON: {json_data}")
        
        # Generate a unique filename for the new JSON
         # Generate a unique filename for the new JSON
        unique_filename = os.path.join(device_folder, f"{uuid.uuid4()}.json")
        app.logger.info(f"Unique FileName: {unique_filename}")
        # Save the JSON to the "new" folder
        with open(unique_filename, 'w') as f:
            json.dump(json_data, f, indent=4)

        # Generate the age norms plot using the updated data
        NormCreate.create_age_norms_plot('database', unique_filename)  # Adjust the function based on your FakeNormCreate.py
        
        #Move the JSON data to the database folder to extend the dataset. 
        #Note: You may want to also keep it in the "new" folder depending on your needs
        db_filename = f"database/{uuid.uuid4()}.json"
        with open(db_filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        
        # Send the updated plot back to the client
        return send_file('age_norms_with_new_data_plot.png', mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_image', methods=['GET'])
def get_image():
    try:
        # Serve the generated image
        return send_file('age_norms_with_new_data_plot.png', mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)