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
os.makedirs('new', exist_ok=True)

@app.route('/get_message', methods=['GET'])
def get_message():
    return "Hello from server"

@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        # Get the JSON data from the request
        json_data = request.json

        # Generate a unique filename for the new JSON
        unique_filename = f"new/{uuid.uuid4()}.json"

        # Save the JSON to the "new" folder
        with open(unique_filename, 'w') as f:
            json.dump(json_data, f, indent=4)

        # Move the JSON data to the database folder
        # Note: You may want to also keep it in the "new" folder depending on your needs
        db_filename = f"database/{uuid.uuid4()}.json"
        with open(db_filename, 'w') as f:
            json.dump(json_data, f, indent=4)

        # Generate the age norms plot using the updated data
        NormCreate.create_age_norms_plot('database', unique_filename)  # Adjust the function based on your FakeNormCreate.py

        # Send the updated plot back to the client
        return send_file('age_norms_with_new_data_plot.png', mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def process_game_data(data):
    # Implement your game-specific processing logic here
    # This is just a placeholder example
    if 'level' in data:
        return f"Processed level {data['level']} data"
    return "Processed game data"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)