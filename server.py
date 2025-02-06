import socket
from _thread import *
import sys

server = "192.168.137.30"  # Accept connections from any IP
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(f"Binding error: {e}")
    sys.exit()  # Exit if binding fails

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(string):
    try:
        x, y = map(int, string.split(","))
        return x, y
    except ValueError:
        return 0, 0  # Default if parsing fails

def make_pos(tup):
    return f"{tup[0]},{tup[1]}"

pos = [(0, 0), (100, 100)]

def threaded_client(conn, player):
    try:
        conn.send(str.encode(make_pos(pos[player])))

        while True:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break

            pos[player] = read_pos(data)
            reply = pos[1] if player == 0 else pos[0]

            print(f"Received: {data}, Sending: {reply}")
            conn.sendall(str.encode(make_pos(reply)))

    except Exception as e:
        print(f"Error in thread: {e}")

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
