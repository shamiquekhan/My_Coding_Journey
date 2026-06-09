import random
import string

class Cipher:
    def __init__(self):
        # Define the character set
        self.chars = list(string.ascii_letters + string.digits + string.punctuation)
        # Create a shuffled key for substitution cipher
        self.key = self.chars.copy()
        random.shuffle(self.key)

    def encrypt(self, plaintext):
        # Encrypt each character by substitution
        encrypted_text = ''.join(
            self.key[self.chars.index(char)] if char in self.chars else char 
            for char in plaintext
        )
        return encrypted_text

    def decrypt(self, encrypted_text):
        # Decrypt each character by reverse substitution
        decrypted_text = ''.join(
            self.chars[self.key.index(char)] if char in self.key else char
            for char in encrypted_text
        )
        return decrypted_text

def main():
    cipher = Cipher()
    print("Welcome to the Encryption/Decryption Program!")
    
    plaintext = input("Enter the text to encrypt: ")
    encrypted = cipher.encrypt(plaintext)
    print("Encrypted text:", encrypted)
    
    encrypted_input = input("Enter the text to decrypt: ")
    decrypted = cipher.decrypt(encrypted_input)
    print("Decrypted text:", decrypted)

if __name__ == "__main__":
    main()
