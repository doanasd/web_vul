import base64
import itertools
import string

def xor_cipher_decrypt(ciphertext, key):
    return bytes([b ^ key for b in ciphertext])

def polyalphabetic_decrypt(ciphertext, key):
    key_length = len(key)
    plaintext = []
    for i, char in enumerate(ciphertext):
        key_char = key[i % key_length]
        decrypted_char = chr((char - ord(key_char)) % 256)
        plaintext.append(decrypted_char)
    return ''.join(plaintext)

def polyalphabetic_brute_force(ciphertext):
    print("Starting brute force for polyalphabetic cipher...")
    for key_guess in itertools.product(string.ascii_letters + string.digits, repeat=16):
        key = ''.join(key_guess)
        try:
            plaintext = polyalphabetic_decrypt(ciphertext, key)
            if "flag" in plaintext.lower():
                print(f"Successful key: {key}")
                return plaintext
        except Exception:
            continue
        if key_guess[0:2] == ('A', 'A'):  # Example debug: show progress for first keys
            print(f"Testing key: {key}")
    return "Unable to decrypt polyalphabetic"

def focused_decrypt(hex_data):
    ciphertext = bytes.fromhex(hex_data)

    # Focused XOR decryption with key = 4
    xor_key = 4
    xor_decrypted = xor_cipher_decrypt(ciphertext, xor_key)
    print(f"XOR decryption successful: {xor_decrypted}")

    # Base64 decoding
    try:
        poly_encrypted = base64.b64decode(xor_decrypted)
        print(f"Base64 decoding successful: {poly_encrypted}")
    except Exception as e:
        print(f"Base64 decoding failed: {e}")
        return "Base64 decoding failed"

    # Brute-force polyalphabetic decryption
    plaintext = polyalphabetic_brute_force(poly_encrypted)
    return plaintext

if __name__ == "__main__":
    with open("output.txt", "r") as f:
        encrypted_data = f.read().strip().split("\n")

    decrypted_flag_parts = [focused_decrypt(part) for part in encrypted_data]
    print("Decrypted FLAG:", ''.join(decrypted_flag_parts))
