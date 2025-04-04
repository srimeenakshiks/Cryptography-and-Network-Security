import socket
import sys
import binascii
from Crypto.Cipher import AES

class AESSERVER:
    @staticmethod
    def hex_string_to_byte_array(hex_str):
        try:
            return bytes.fromhex(hex_str)
        except ValueError:
            raise ValueError("Invalid hex string format")

    @staticmethod
    def bytes_to_hex(byte_array):
        return binascii.hexlify(byte_array).decode("utf-8").upper()

    @staticmethod
    def decrypt(encrypted_message, key_bytes):
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message

if __name__ == "__main__":
    server_socket = None
    client_socket = None

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 12345))
        server_socket.listen(1)
        print("Server started. Waiting for client connection...")

        client_socket, _ = server_socket.accept()
        print("Client connected!")

        while True:
            encrypted_message_hex = client_socket.recv(1024).decode("utf-8")
            if not encrypted_message_hex or encrypted_message_hex.lower() == "exit":
                print("Client disconnected.")
                break

            print(f"Encrypted Message received (in hex): {encrypted_message_hex.upper()}")
            key = input("Enter Key (16 hex digits): ")

            aes_obj = AESSERVER()
            try:
                encrypted_message = aes_obj.hex_string_to_byte_array(encrypted_message_hex)
                key_bytes = aes_obj.hex_string_to_byte_array(key)
            except Exception as e:
                print("Invalid key format. Ensure the key is 16 hex digits.")
                continue

            if len(key_bytes) != 16:
                print("Invalid key length. Ensure the key is 16 hex digits.")
                continue

            decrypted_message = aes_obj.decrypt(encrypted_message, key_bytes)
            print(f"Server: Decrypted Message: 0x{AESSERVER.bytes_to_hex(decrypted_message)}")

            client_socket.send(AESSERVER.bytes_to_hex(decrypted_message).encode("utf-8"))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if client_socket:
            client_socket.close()
        if server_socket:
            server_socket.close()
