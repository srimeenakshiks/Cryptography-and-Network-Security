import socket

# Diffie-Hellman parameters (prime p and generator g)
p = 23  # Prime number
g = 5   # Generator

# Bob (Client) code
def bob():
    # Get Bob's private key from the user
    private_key_bob = int(input("Enter Bob's private key: "))

    # Bob computes public key
    public_key_bob = pow(g, private_key_bob, p)
    print(f"Bob's public key: {public_key_bob}")

    # Bob connects to the attacker (thinking it's Alice)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))
    print("Connection established with Alice...")

    # Step 1: Send Bob's public key to attacker
    client_socket.send(str(public_key_bob).encode())

    # Step 2: Receive the attacker's public key (pretending to be Alice)
    attacker_public_key = int(client_socket.recv(1024).decode())
    print(f"Bob received public key from Alice: {attacker_public_key}")

    # Step 3: Bob computes the shared secret with the attacker (Darth)
    bob_shared_secret = pow(attacker_public_key, private_key_bob, p)
    print(f"Bob's shared secret (with Alice): {bob_shared_secret}")

    # Close connection
    client_socket.close()

if __name__ == "__main__":
    bob()
