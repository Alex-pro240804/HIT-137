def decrypt_caesar_cipher(ciphertext, shift_key=13):
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

# Given cryptogram
ciphertext = "VZ FRYSVFU VZCNGVRAG NAQ N YVGGYR VAFRPHER V ZNXR ZVFGNXR V NZ BHGF BS PBAGEBY NAQMG GVZRQ UNEQ GB UNAQYR OHG VS LBH PNAG UNAQYR ZR NG ZL JBEFG GURA LBH FHER NF URYYQBAR QRFRER ZR NG ZL ORFG ZNEVYLA ZBAEBR"

# Decrypt the cryptogram using shift key 13
decrypted_message = decrypt_caesar_cipher(ciphertext, 13)
print(decrypted_message)
