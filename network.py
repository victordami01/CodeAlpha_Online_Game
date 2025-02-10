import asyncio
import websockets
import json

class Network:
    def __init__(self):
        self.server_url = "wss://codealpha-online-game.onrender.com"  # Use WebSocket Secure (wss)
        self.player = None
        self.websocket = None  # WebSocket connection

    async def connect(self):
        """Connects to the WebSocket server and initializes the player ID."""
        try:
            self.websocket = await websockets.connect(self.server_url)
            player_data = await self.websocket.recv()
            self.player = json.loads(player_data)["player"]  # Expecting JSON format
            return self.player
        except Exception as e:
            print(f"Connection Error: {e}")
            return None

    async def send(self, data):
        """Sends a message to the server and waits for a response."""
        try:
            await self.websocket.send(json.dumps(data))  # Send data as JSON
            response = await self.websocket.recv()  # Wait for response
            return json.loads(response)  # Convert response back to Python dict
        except Exception as e:
            print(f"Send Error: {e}")
            return None

    async def close(self):
        """Closes the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
