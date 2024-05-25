from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to receive Slack events and verify URL
@app.route('/slack/events', methods=['POST', 'GET'])
def slack_events():
    if request.method == 'GET':
        # Respond to URL verification challenge
        challenge = request.json.get('challenge')
        return jsonify({'challenge': challenge})
    elif request.method == 'POST':
        # Handle incoming event payload here
        payload = request.json
        # Process the event payload
        print(payload)
        return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
