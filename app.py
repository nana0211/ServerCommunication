from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/get_message', methods=['GET'])
def get_message():
    return "Hello from server"


@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        # Get the JSON data from the request
        request_data = request.json
        device_id = request_data['deviceID']
        json_data = json.loads(request_data['data'])

        # Process the JSON data
        # This is where you'd implement your game-specific logic
        processed_result = process_game_data(json_data)

        return jsonify({
            'status': 'success',
            'message': f'Data processed successfully for device {device_id}',
            'result': processed_result
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

def process_game_data(data):
    # Implement your game-specific processing logic here
    # This is just a placeholder example
    if 'level' in data:
        return f"Processed level {data['level']} data"
    return "Processed game data"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)