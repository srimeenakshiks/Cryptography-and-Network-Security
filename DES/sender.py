import socket

# Initial Permutation (unused in this simplified version)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Two S-Boxes (defined but not used in this simplified version)
S_BOXES = [
    [  # S1
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [  # S2
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ]
]

# Simplified Feistel function
def feistel_function(right, key):
    return (right ^ key) & 0xFFFFFFFF

# Simplified DES encryption with fixed rounds and basic Feistel logic
def des_encrypt(plain_text_hex, key_hex):
    block = int(plain_text_hex.replace(" ", ""), 16)
    key = int(key_hex.replace(" ", ""), 16) & 0xFFFFFFFFFFFFFF
    left, right = (block >> 32) & 0xFFFFFFFF, block & 0xFFFFFFFF

    for _ in range(16):
        new_right = left ^ feistel_function(right, key)
        left, right = right, new_right & 0xFFFFFFFF

    encrypted_data = ((right & 0xFFFFFFFF) << 32) | (left & 0xFFFFFFFF)
    return f"{encrypted_data:016X}"

# Sender function
def sender():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.bind(("localhost", 12345))
    sender_socket.listen(1)
    print("Waiting for receiver to connect...")
    
    conn, addr = sender_socket.accept()
    print(f"Connected to {addr}")

    plain_text_hex = input("Enter a 64-bit message (hex, 16 characters): ").strip()
    key_hex = input("Enter a 56-bit key (hex, 14 characters): ").strip()

    if len(plain_text_hex.replace(" ", "")) != 16 or len(key_hex.replace(" ", "")) != 14:
        print("Error: Message must be 64 bits (16 hex characters) and key must be 56 bits (14 hex characters).")
        conn.close()
        return

    encrypted_message = des_encrypt(plain_text_hex, key_hex)
    conn.send(encrypted_message.encode())
    print(f"Sent Encrypted Message: {encrypted_message}")
    conn.close()

if __name__ == "__main__":
    sender()
