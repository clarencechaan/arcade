import socket, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 4003))

while True:
    data = "I'm logged"
    data = pickle.dumps(data)
    server.send(data)
    data = server.recv(1024)
    data = pickle.loads(data)
    print(data)

server.close()