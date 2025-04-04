import socket
import binascii
from Crypto.Cipher import AES

class AESClient:
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
    def encrypt(plaintext, key_bytes):
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted_message = cipher.encrypt(plaintext)
        return encrypted_message

if __name__ == "__main__":
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))
        print("Connected to the server.")

        while True:
            plaintext_input = input("Enter plaintext (32 hex characters / 16 bytes): ").strip()
            key_input = input("Enter encryption key (32 hex characters / 16 bytes): ").strip()

            aes_obj = AESClient()
            try:
                plaintext = aes_obj.hex_string_to_byte_array(plaintext_input)
                key_bytes = aes_obj.hex_string_to_byte_array(key_input)
            except ValueError:
                print("Invalid hex format. Ensure both plaintext and key are valid hex.")
                continue

            if len(plaintext) != 16 or len(key_bytes) != 16:
                print("Invalid length. Ensure both plaintext and key are exactly 16 bytes.")
                continue

            ciphertext = aes_obj.encrypt(plaintext, key_bytes)
            ciphertext_hex = AESClient.bytes_to_hex(ciphertext)
            client_socket.send(ciphertext_hex.encode("utf-8"))
            print(f"Ciphertext sent to server: {ciphertext_hex}")

            command = input("Type 'exit' to quit or press Enter to continue: ").strip()
            if command.lower() == "exit":
                client_socket.send("exit".encode("utf-8"))
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if client_socket:
            client_socket.close()
        print("Client disconnected.")
