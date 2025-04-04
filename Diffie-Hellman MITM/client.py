import socket

# Diffie-Hellman parameters (prime p and generator g)
p = 23  # Prime number
g = 5   # Generator

# Alice (Client) code
def alice():
    # Get Alice's private key from the user
    private_key_alice = int(input("Enter Alice's private key: "))

    # Alice computes public key
    public_key_alice = pow(g, private_key_alice, p)
    print(f"Alice's public key: {public_key_alice}")

    # Alice connects to the attacker (thinking it's Bob)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))
    print("Connection established with Bob...")

    # Step 1: Send Alice's public key to attacker
    client_socket.send(str(public_key_alice).encode())

    # Step 2: Receive the attacker's public key (pretending to be Bob)
    attacker_public_key = int(client_socket.recv(1024).decode())
    print(f"Alice received public key from Bob: {attacker_public_key}")

    # Step 3: Alice computes the shared secret with the attacker (Darth)
    alice_shared_secret = pow(attacker_public_key, private_key_alice, p)
    print(f"Alice's shared secret (with Bob): {alice_shared_secret}")

    # Close connection
    client_socket.close()

if __name__ == "__main__":
    alice()
