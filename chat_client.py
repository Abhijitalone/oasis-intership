import socket
import threading

HOST = "127.0.0.1"  # Server's IP address
PORT = 5000         # Must match the server port

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("⚠ Connection closed.")
            client.close()
            break

def send_messages():
    while True:
        message = input("")
        client.send(f"{nickname}: {message}".encode('utf-8'))

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()
