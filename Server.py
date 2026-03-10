import asyncio            #wait react loop
import websocket         #real time communication
import json               #data format
import pyautogui          #control mouse and keyboard

# Screen Size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

print("Server is running... Waiting for Phone to connect.")

# Handle incoming WebSocket connections

async def handle_connection(websocket):
    print("Phone connected.")

    async for message in websocket:
            try:
                  
                data = json.loads(message)
                
                x = int(data['x'] * SCREEN_WIDTH)  # Scale x coordinate to screen width
                y = int(data['y'] * SCREEN_HEIGHT) # Scale y coordinate to screen height

                pyautogui.moveTo(x, y)  # Move mouse to the calculated position

            except:
                 pass
            

# Server Start

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever


# Server Run

asyncio.run(main())
            
