import socket
from sympy import mod_inverse

def verify_signature(message_hash, p, q, g, y, r, s):
    print("\n--- Signature Verification ---")
    if r <= 0 or r >= q or s <= 0 or s >= q:
        print("Signature INVALID: r or s out of bounds")
        return False

    w = mod_inverse(s, q)  # Compute w = s^-1 mod q
    u1 = (message_hash * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q  # Correct modular reduction

    print(f"Computed u1 = {u1}, u2 = {u2}, w = {w}")
    print(f"Computed v = {v}, Received r = {r}")

    if v == r:
        print("\nSignature is VALID! Message is authentic.")
        return True
    else:
        print("\nSignature is INVALID! Message may be tampered.")
        return False

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    message_hash = int(input("Enter message hash (integer): "))
    client_socket.send(str(message_hash).encode())

    data = client_socket.recv(1024).decode()
    p, q, g, y, r, s = map(int, data.split(','))
    print(f"\nClient received: p={p}, q={q}, g={g}, y={y}, r={r}, s={s}")

    verify_signature(message_hash, p, q, g, y, r, s)

    client_socket.close()

if __name__ == "__main__":
    client()
