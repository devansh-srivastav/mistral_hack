import streamlit as st
import requests
from threading import Thread
import datetime

# Shared data to display in Streamlit
messages = []

def handle_slack_event(request):
    data = request.json()
    if 'challenge' in data:
        return {'challenge': data['challenge']}
    
    # Process the event data
    event = data.get('event', {})
    if event.get('type') == 'message' and 'subtype' not in event:
        user = event.get('user')
        text = event.get('text')
        channel = event.get('channel')
        timestamp = datetime.datetime.fromtimestamp(float(event.get('ts')))
        
        # Append the message to the shared list
        messages.append({
            'user': user,
            'text': text,
            'channel': channel,
            'timestamp': timestamp
        })
    
    return {'status': 'OK'}

def start_server():
    import flask
    app = flask.Flask(__name__)
    
    @app.route('/slack/events', methods=['POST'])
    def slack_events():
        response_data = handle_slack_event(flask.request)
        return flask.jsonify(response_data)

    app.run(host='0.0.0.0', port=8000)

# Start the Flask server in a separate thread
Thread(target=start_server).start()

def main():
    st.title("Slack Message Logger")
    st.write("This Streamlit app captures messages from Slack and displays them.")
    
    if messages:
        for message in messages:
            st.write(f"User: {message['user']}")
            st.write(f"Message: {message['text']}")
            st.write(f"Channel: {message['channel']}")
            st.write(f"Timestamp: {message['timestamp']}")
            st.write("---")
    else:
        st.write("No messages received yet.")

if __name__ == "__main__":
    main()
