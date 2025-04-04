import socket

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def decrypt(cipher_text, private_key):
    d, n = private_key
    plain_text = mod_exp(cipher_text, d, n)
    return plain_text

def receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.connect(('localhost', 12345))
    data = receiver_socket.recv(1024).decode()
    cipher_text, e, n, d = map(int, data.split(","))
    receiver_socket.close()

    print(f"Encrypted message (ciphertext) received from sender: {cipher_text}")
    print(f"Public modulus n received from sender: {n}")
    print(f"Public key e received from sender: {e}")

    private_key = (d, n)
    decrypted_message = decrypt(cipher_text, private_key)
    print(f"Decrypted message (plaintext): {decrypted_message}")

if __name__ == "__main__":
    receiver()
