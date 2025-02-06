import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.137.30"  # Make sure this is the correct IP of the server
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("Failed to connect to server")
            return "0,0"

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            return "0,0"

    def getPos(self):
        return self.pos

if __name__ == "__main__":
    n = Network()
    print("Connected to server, received:", n.getPos())