import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    
    message = input("Enter message to hash: ")
    client_socket.send(message.encode())
    
    sha1_hash = client_socket.recv(1024).decode()
    print(f"Received SHA-1 Hash from Server: {sha1_hash}")
    
    client_socket.close()

if __name__ == "__main__":
    client()
