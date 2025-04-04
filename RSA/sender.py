import socket

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def generate_keys():
    p = int(input("Enter a prime number p: "))
    q = int(input("Enter another prime number q: "))
    if p == q:
        print("Error: p and q should be different.")
        return None
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = int(input("Enter the public key e (a prime number): "))
    if gcd(e, phi_n) != 1:
        print("Error: e is not coprime with φ(n). Choose another e.")
        return None
    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    cipher_text = mod_exp(message, e, n)
    return cipher_text

def sender():
    public_key, private_key = generate_keys()
    if not public_key:
        return
    message = int(input("Enter the message m (as an integer): "))
    cipher_text = encrypt(message, public_key)
    print(f"Encrypted message (ciphertext): {cipher_text}")
    print(f"Public modulus n: {public_key[1]}")

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.bind(('localhost', 12345))
    sender_socket.listen(1)
    print("Waiting for receiver to connect...")
    conn, addr = sender_socket.accept()
    conn.send(f"{cipher_text},{public_key[0]},{public_key[1]},{private_key[0]}".encode())
    conn.close()
    sender_socket.close()
    print("Encrypted message and keys sent to receiver.")

if __name__ == "__main__":
    sender()
