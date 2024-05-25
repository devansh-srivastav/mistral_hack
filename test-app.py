import streamlit as st
import asyncio
from aiohttp import web
import datetime

# Shared data to display in Streamlit
messages = []

async def handle_slack_event(request):
    data = await request.json()
    if 'challenge' in data:
        return web.json_response({'challenge': data['challenge']})
    
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
    
    return web.json_response({'status': 'OK'})

async def start_server():
    app = web.Application()
    app.router.add_post('/slack/events', handle_slack_event)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8000)  # Using port 8000 as Streamlit typically uses 8501
    await site.start()

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
    # Use asyncio to run both the Streamlit app and the aiohttp server
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    main()
