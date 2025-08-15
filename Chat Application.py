import socket
import threading

HOST = "127.0.0.1"  # Localhost
PORT = 5000         # Port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, _client=None):
    for client in clients:
        if client != _client:  # Don't send message back to sender
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"💔 {nickname} left the chat.\n".encode('utf-8'))
            break

def receive_connections():
    print("📡 Server is running and waiting for connections...")
    while True:
        client, address = server.accept()
        print(f"✅ Connected with {address}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"🆕 Nickname is {nickname}")
        broadcast(f"🎉 {nickname} joined the chat!\n".encode('utf-8'))
        client.send("✅ Connected to the server.\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive_connections()

