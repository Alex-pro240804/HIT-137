def decrypt_caesar_cipher(ciphertext, shift_key):
    decrypted_text = ""

    for char in ciphertext:
        # Check if the character is a letter
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            ascii_offset = 65 if char.isupper() else 97

            # Apply the decryption formula
            decrypted_char = chr((ord(char) - ascii_offset - shift_key) % 26 + ascii_offset)
            decrypted_text += decrypted_char
        else:
            # Non-alphabetic characters remain the same
            decrypted_text += char

    return decrypted_text

# Example usage:
ciphertext = "VZ FRYSVFU VZCNGVRAG NAQ N YVGGYR VAFRPHER V ZNXR ZVFGNXR..."

# Try different shift keys to find the correct one
for s in range(1, 27):
    decrypted_message = decrypt_caesar_cipher(ciphertext, s)
    print(f"Shift Key {s}: {decrypted_message}")
