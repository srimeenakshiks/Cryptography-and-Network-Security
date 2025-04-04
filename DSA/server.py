import socket
import random
from sympy import mod_inverse

def sign_message(message_hash, p, q, g, x):
    while True:
        k = random.randint(1, q - 1)  # Random nonce k
        r = pow(g, k, p) % q
        if r == 0:  # r must not be 0
            continue
        k_inv = mod_inverse(k, q)  # Compute k^-1 mod q
        s = (k_inv * (message_hash + x * r)) % q
        if s != 0:  # s must not be 0
            break
    return r, s

def server():
    p = int(input("Enter prime p: "))
    q = int(input("Enter prime q (must be a prime factor of p-1): "))
    g = int(input("Enter generator g: "))

    x = random.randint(1, q - 1)  # Private key
    y = pow(g, x, p)  # Public key
    print(f"Public key y = {y}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("\nServer is waiting for a connection...")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    message_hash = int(conn.recv(1024).decode())
    print(f"Received message hash: {message_hash}")

    r, s = sign_message(message_hash, p, q, g, x)
    print(f"Signed hash: (r={r}, s={s})")

    # Send public values & signature to client
    conn.send(f"{p},{q},{g},{y},{r},{s}".encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    server()
