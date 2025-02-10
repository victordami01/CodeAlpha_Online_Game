import asyncio
import websockets
import json
from game import Game  # Ensure your Game class has a to_dict() method

# Game state
games = {}
connected_clients = {}
id_count = 0

async def handler(websocket):  # Remove 'path'
    global id_count

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2

    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        connected_clients[game_id] = [websocket]
        print(f"Creating a new game... {game_id}")
    else:
        if game_id in games:  # ✅ Ensure game exists before modifying it
            games[game_id].ready = True
            connected_clients[game_id].append(websocket)
            p = 1
        else:
            print(f"⚠️ Game {game_id} does not exist. Player disconnected.")
            return  # Exit handler since game was removed

    print(f"Player {p} connected to game {game_id}")  # ✅ Debugging

    await websocket.send(json.dumps({"type": "init", "player": p}))

    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received from Player {p} (Game {game_id}): {data}")  # ✅ Debugging

            if game_id in games:
                game = games[game_id]

                if data["type"] == "move":
                    game.play(p, data["move"])
                    print(f"Player {p} played {data['move']} in Game {game_id}")  # ✅ Debugging

                    # ✅ Broadcast updated game state
                    for client in connected_clients[game_id]:
                        await client.send(json.dumps({"type": "update", "game": game.to_dict()}))

                    if game.bothWent():
                        winner = game.winner()
                        print(f"Game {game_id} result: {winner}")  # ✅ Debugging

                        # ✅ Send result to players
                        for client in connected_clients[game_id]:
                            await client.send(json.dumps({"type": "result", "winner": winner}))

                        await asyncio.sleep(3)  # ⏳ Let players see the result for 3 seconds

                        game.resetWent()  # 🔄 Reset game state AFTER delay

                        # ✅ Send updated game state so players know a new round is starting
                        for client in connected_clients[game_id]:
                            await client.send(json.dumps({"type": "update", "game": game.to_dict()}))

                elif data["type"] == "chat_message":
                    chat_msg = data["message"]
                    print(f"💬 Chat Message from Player {p} in Game {game_id}: {chat_msg}")

                    # ✅ Broadcast chat message to both players
                    for client in connected_clients[game_id]:
                        await client.send(json.dumps({
                            "type": "chat_message",
                            "message": chat_msg,
                            "player": p  # Include player number for UI styling
                        }))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Player {p} disconnected from Game {game_id}")  # ✅ Debugging
        if game_id in connected_clients:
            connected_clients[game_id].remove(websocket)

            if not connected_clients[game_id]:  # If no players left, delete the game
                del games[game_id]
                del connected_clients[game_id]
                print(f"Game {game_id} removed")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):  # No 'legacy_recv=True'
        print("WebSocket server started on port 10000")
        await asyncio.Future()  # Run forever

asyncio.run(main())
