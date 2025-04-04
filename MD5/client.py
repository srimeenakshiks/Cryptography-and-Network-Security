import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    message = input("Enter message to hash: ")
    client_socket.send(message.encode())
    md5_hash = client_socket.recv(1024).decode()
    print(f"Received MD5 Hash from Server: {md5_hash}")
    client_socket.close()

if __name__ == "__main__":
    client()
