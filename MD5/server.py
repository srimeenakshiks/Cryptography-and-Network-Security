import socket
import struct
import math

# MD5 Constants
A, B, C, D = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)
S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
K = [int(abs(2**32 * abs(math.sin(i + 1)))) for i in range(64)]  # Precomputed table

# Left Rotate function
def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

# Padding the message
def md5_padding(message):
    original_length = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', original_length)
    return message

# Processing 512-bit chunks
def md5_process(message):
    global A, B, C, D
    for i in range(0, len(message), 64):
        chunk = message[i:i + 64]
        X = list(struct.unpack('<16I', chunk))
        a, b, c, d = A, B, C, D
        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16
            f = (f + a + K[i] + X[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(f, S[i])) & 0xFFFFFFFF
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

# MD5 Hash Function
def md5(message):
    global A, B, C, D
    A, B, C, D = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)
    padded_message = md5_padding(message.encode())
    md5_process(padded_message)
    return ''.join(f'{x:08x}' for x in [A, B, C, D])

# Server Code
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Server is listening on port 5000...")
    
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    
    data = conn.recv(1024).decode()
    print(f"Received data: {data}")
    
    md5_hash = md5(data)
    print(f"MD5 Hash: {md5_hash}")
    
    conn.send(md5_hash.encode())
    conn.close()

if __name__ == "__main__":
    server()
