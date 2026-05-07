import asyncio
import websockets
import json
import http.server
import threading
import os
from pynput.mouse import Controller, Button
import socket

print("Server is running... Waiting for Phone to connect.")

#get local IP address for user convenience
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


# Serve index.html on port 8080
def serve_html():
    folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder)

    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("0.0.0.0", 8080), handler)

    print(f"HTML served at http://{get_local_ip()}:8080")
    
    httpd.serve_forever()


# Run HTML server in background thread
threading.Thread(target=serve_html, daemon=True).start()

class ConnectionState:

    def __init__(self):
     # Tunable settings 
        self.sensitivity = 1.0     #what fraction of the touch movement translates to cursor movement
        self.smoothing = 0.8      #how much of the previous movement to retain for smoothing (0-1, higher is smoother)
        self.damping = 0.85        #how much to slow down movement (0-1, lower is more damping)

        self.prev_dx = 0
        self.prev_dy = 0
        self.mouse = Controller()

    def handle_move(self, data):
        dx = data.get("dx", 0)
        dy = data.get("dy", 0)

        # Ignore micro jitter
        if abs(dx) < 0.8 and abs(dy) < 0.8:
            return

        # Smooth movement
        dx = self.prev_dx * self.smoothing + dx * (1 - self.smoothing)
        dy = self.prev_dy * self.smoothing + dy * (1 - self.smoothing)

        self.prev_dx = dx
        self.prev_dy = dy

        # Damping
        dx *= self.damping
        dy *= self.damping

        # Move cursor
        self.mouse.move(int(dx * self.sensitivity), int(dy * self.sensitivity))

    def handle_click(self, data):
        button = Button.left if data.get("button", "left") == "left" else Button.right
        self.mouse.click(button)

    def handle_scroll(self, data):
        scroll_x = data.get("scroll_x", 0)
        scroll_y = data.get("scroll_y", 0)

        self.mouse.scroll(scroll_x, scroll_y)


# Handle incoming WebSocket connections
async def handle_connection(websocket):
    print("Phone connected.")

    state = ConnectionState()
    
    try:
        async for message in websocket:

            data = json.loads(message)
            event_type = data.get("type")

            # each event type can have its own handler function for better organization
            if event_type == "move":
                state.handle_move(data)
            elif event_type == "click":
                state.handle_click(data)
            elif event_type == "scroll":
                state.handle_scroll(data)

    except websockets.exceptions.ConnectionClosed:
        print("Phone disconnected")


# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket running on port 8765")
        await asyncio.Future()


# Run server
asyncio.run(main())