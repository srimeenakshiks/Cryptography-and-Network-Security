import socket
import random
import time

# Diffie-Hellman parameters (prime p and generator g)
p = 23  # Prime number
g = 5   # Generator

# Darth (Attacker) generates two sets of private/public keys
def attacker():
    private_key_darth_to_alice = random.randint(1, p - 1)
    private_key_darth_to_bob = random.randint(1, p - 1)
    
    public_key_darth_to_alice = pow(g, private_key_darth_to_alice, p)
    public_key_darth_to_bob = pow(g, private_key_darth_to_bob, p)

    print(f"Darth's public key to Alice: {public_key_darth_to_alice}")
    print(f"Darth's public key to Bob: {public_key_darth_to_bob}")

    # Attacker listens to both Alice and Bob
    attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attacker_socket.bind(('localhost', 5001))
    attacker_socket.listen(2)
    print("Darth is listening for connections...")

    # Accept connections from both Alice and Bob
    alice_conn, alice_addr = attacker_socket.accept()
    print(f"Alice connected. Address: {alice_addr}")
    bob_conn, bob_addr = attacker_socket.accept()
    print(f"Bob connected. Address: {bob_addr}")

    # Alice sends her public key to attacker
    alice_public_key = int(alice_conn.recv(1024).decode())
    print(f"Alice's public key (intercepted by Darth): {alice_public_key}")

    # Darth sends his public key to Alice (pretending to be Bob)
    alice_conn.send(str(public_key_darth_to_alice).encode())

    # Bob sends his public key to attacker
    bob_public_key = int(bob_conn.recv(1024).decode())
    print(f"Bob's public key (intercepted by Darth): {bob_public_key}")

    # Darth sends his public key to Bob (pretending to be Alice)
    bob_conn.send(str(public_key_darth_to_bob).encode())

    # Alice computes the shared secret with Darth (thinking it's Bob)
    alice_shared_secret = pow(public_key_darth_to_alice, private_key_darth_to_alice, p)
    print(f"Alice's shared secret (with Darth): {alice_shared_secret}")

    # Bob computes the shared secret with Darth (thinking it's Alice)
    bob_shared_secret = pow(public_key_darth_to_bob, private_key_darth_to_bob, p)
    print(f"Bob's shared secret (with Darth): {bob_shared_secret}")

    # Attacker computes shared secrets with both Alice and Bob
    attacker_shared_secret_with_alice = pow(alice_public_key, private_key_darth_to_alice, p)
    attacker_shared_secret_with_bob = pow(bob_public_key, private_key_darth_to_bob, p)

    print(f"Darth's shared secret key with Alice: {attacker_shared_secret_with_alice}")
    print(f"Darth's shared secret key with Bob: {attacker_shared_secret_with_bob}")

    print("Darth is now listening to the conversation between Alice and Bob...")
    time.sleep(5)

    # Close connections
    alice_conn.close()
    bob_conn.close()

if __name__ == "__main__":
    attacker()
