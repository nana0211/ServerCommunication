from flask import Flask, request, jsonify
import json
import pandas as pd

app = Flask(__name__)

@app.route('/get_message', methods=['GET'])
def get_message():
    return "Hello from server"


@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        # Get the JSON data from the request
        json_data = request.json

        # Convert JSON to DataFrame
        df = pd.DataFrame([json_data])

        # Save DataFrame to CSV
        csv_filename = 'output.csv'
        df.to_csv(csv_filename, index=False)

        return jsonify({"message": "Successfully converted to CSV"}), 200
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