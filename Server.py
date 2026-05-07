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

class ConnectionState:

    def __init__(self):
     # Tunable settings 
        self.sensitivity = 1.0     #what fraction of the touch movement translates to cursor movement
        self.smoothing = 0.8      #how much of the previous movement to retain for smoothing (0-1, higher is smoother)
        self.damping = 0.85        #how much to slow down movement (0-1, lower is more damping)

        self.prev_dx = 0
        self.prev_dy = 0

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
        pyautogui.moveRel(dx * self.sensitivity, dy * self.sensitivity)

    def handle_click(self, data):
        button = data.get("button", "left")
        pyautogui.click(button=button)
    
    def handle_scroll(self, data):
        scroll_x = data.get("scroll_x", 0)
        scroll_y = data.get("scroll_y", 0)

        if scroll_x != 0:
            pyautogui.hscroll(scroll_x)
        if scroll_y != 0:
            pyautogui.scroll(scroll_y)


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