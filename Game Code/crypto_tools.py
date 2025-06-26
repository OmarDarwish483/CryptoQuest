class CryptoTools:
    @staticmethod
    def caesar_cipher(text, shift, decrypt=False):
        """
        Encrypt or decrypt text using Caesar cipher
        """
        if decrypt:
            shift = -shift
        
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('a') if char.islower() else ord('A')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    @staticmethod
    def vigenere_cipher(text, key, decrypt=False):
        """
        Encrypt or decrypt text using Vigenère cipher
        """
        result = ""
        key_length = len(key)
        key_as_int = [ord(i) for i in key.lower()]
        text_int = [ord(i) for i in text]
        
        for i in range(len(text_int)):
            if text[i].isalpha():
                if decrypt:
                    value = (text_int[i] - key_as_int[i % key_length]) % 26
                else:
                    value = (text_int[i] + key_as_int[i % key_length]) % 26
                result += chr(value + ord('A'))
            else:
                result += text[i]
        return result

    @staticmethod
    def atbash_cipher(text):
        """
        Encrypt or decrypt text using Atbash cipher
        """
        result = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result += chr(90 - (ord(char) - 65))
                else:
                    result += chr(122 - (ord(char) - 97))
            else:
                result += char
        return result

    @staticmethod
    def binary_to_text(binary):
        """
        Convert binary string to text
        """
        binary = binary.replace(" ", "")
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

    @staticmethod
    def text_to_binary(text):
        """
        Convert text to binary string
        """
        return ' '.join(format(ord(char), '08b') for char in text)

    @staticmethod
    def morse_code(text, decrypt=False):
        """
        Convert between text and Morse code
        """
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', ' ': ' '
        }
        
        reverse_morse = {v: k for k, v in morse_dict.items()}
        
        if decrypt:
            return ' '.join(reverse_morse.get(code, '') for code in text.split())
        else:
            return ' '.join(morse_dict.get(char.upper(), '') for char in text) 