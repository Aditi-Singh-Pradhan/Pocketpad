import asyncio
import websockets
import json
import pyautogui
import http.server
import threading
import os

# Prevent accidental stop if cursor hits corner
pyautogui.FAILSAFE = False

# Screen Size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

print("Server is running... Waiting for Phone to connect.")


# Serve index.html on port 8080
def serve_html():
    folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder)

    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("0.0.0.0", 8080), handler)

    print("HTML served at http://192.168.137.1:8080")
    httpd.serve_forever()


# Run HTML server in background thread
threading.Thread(target=serve_html, daemon=True).start()


# Handle incoming WebSocket connections
async def handle_connection(websocket):
    print("Phone connected.")

    # Tunable settings 
    sensitivity = 1.0     #what fraction of the touch movement translates to cursor movement
    smoothing = 0.8      #how much of the previous movement to retain for smoothing (0-1, higher is smoother)
    damping = 0.85        #how much to slow down movement (0-1, lower is more damping)

    prev_dx = 0
    prev_dy = 0

    try:
        async for message in websocket:

            data = json.loads(message)

            dx = data.get("dx", 0)
            dy = data.get("dy", 0)

            # Ignore micro jitter
            if abs(dx) < 0.8 and abs(dy) < 0.8:
                continue

            # Smooth movement
            dx = prev_dx * smoothing + dx * (1 - smoothing)
            dy = prev_dy * smoothing + dy * (1 - smoothing)

            prev_dx = dx
            prev_dy = dy

            # Damping
            dx *= damping
            dy *= damping

            # Move cursor
            pyautogui.moveRel(dx * sensitivity, dy * sensitivity)

    except websockets.exceptions.ConnectionClosed:
        print("Phone disconnected")


# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket running on port 8765")
        await asyncio.Future()


# Run server
asyncio.run(main())