class GameData:
    # Room descriptions and available items
    ROOMS = {
        'entrance': {
            'description': 'Welcome to the Cryptography Learning Center! This room introduces you to the basics of the Caesar cipher, one of the simplest encryption techniques.',
            'items': ['note', 'caesar_key'],
            'puzzles': ['entrance_puzzle'],
            'exits': ['library']
        },
        'library': {
            'description': 'The RSA Learning Room. Here you\'ll learn about asymmetric cryptography and the RSA algorithm, one of the first public-key cryptosystems.',
            'items': ['rsa_key'],
            'puzzles': ['library_puzzle'],
            'exits': ['entrance', 'study']
        },
        'study': {
            'description': 'The Private Key Study Room. This room focuses on the importance of private keys in asymmetric cryptography and their role in digital signatures.',
            'items': ['private_key'],
            'puzzles': ['study_puzzle'],
            'exits': ['library', 'vault']
        },
        'vault': {
            'description': 'The Treasure Room of Cryptography. This is where you\'ll find the final treasure, protected by the knowledge you\'ve gained about RSA and asymmetric cryptography.',
            'items': ['treasure_key'],
            'puzzles': ['vault_puzzle'],
            'exits': ['study']
        }
    }

    # Puzzles and their solutions
    PUZZLES = {
        'entrance_puzzle': {
            'type': 'caesar',
            'encrypted_text': 'KHOOR',
            'hint': 'Try shifting the letters by 3 positions',
            'solution': 'HELLO',
            'reward': 'caesar_key'
        },
        'library_puzzle': {
            'type': 'caesar',
            'encrypted_text': 'DWWDFN',
            'hint': 'Shift each letter by 3 positions',
            'solution': 'ATTACK',
            'reward': 'rsa_key'
        },
        'study_puzzle': {
            'type': 'caesar',
            'encrypted_text': 'WKH',
            'hint': 'Try shifting the letters by 3 positions',
            'solution': 'THE',
            'reward': 'private_key'
        },
        'vault_puzzle': {
            'type': 'caesar',
            'encrypted_text': 'FDU',
            'hint': 'Shift each letter by 3 positions',
            'solution': 'CAR',
            'reward': 'treasure_key'
        }
    }

    # Items and their descriptions
    ITEMS = {
        'note': {
            'description': 'A note with important information',
            'usable': True,
            'educational_info': '''The Caesar Cipher is one of the earliest known encryption techniques. 
It works by shifting each letter in the plaintext by a fixed number of positions down the alphabet.
For example, with a shift of 3:
A -> D, B -> E, C -> F, ..., Z -> C
This cipher was used by Julius Caesar to protect military messages.'''
        },
        'caesar_key': {
            'description': 'A key for Caesar cipher',
            'usable': True,
            'educational_info': '''The Caesar Cipher is named after Julius Caesar, who used it to protect his military communications.
The key represents the number of positions each letter is shifted in the alphabet.
Modern computers can easily break this cipher by trying all 25 possible shifts.'''
        },
        'rsa_key': {
            'description': 'A key for RSA encryption',
            'usable': True,
            'educational_info': '''RSA (Rivest-Shamir-Adleman) is a public-key cryptosystem widely used for secure data transmission.
It uses two keys: a public key for encryption and a private key for decryption.
The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers.'''
        },
        'private_key': {
            'description': 'A private key for decryption',
            'usable': True,
            'educational_info': '''Private keys are kept secret and used for decryption in asymmetric cryptography.
They are mathematically related to public keys but cannot be derived from them.
Keeping private keys secure is crucial for maintaining the security of encrypted communications.'''
        },
        'treasure_key': {
            'description': 'A key to open the treasure',
            'usable': True,
            'educational_info': '''Keys have been used for security since ancient times.
Modern cryptographic keys are digital and much more complex than physical keys.
The strength of a cryptographic system often depends on the length and randomness of its keys.'''
        },
        'treasure': {
            'description': 'The final treasure',
            'usable': False,
            'educational_info': '''Cryptography has evolved from simple ciphers to complex algorithms.
Modern cryptography is essential for:
- Secure online transactions
- Protecting personal data
- Ensuring privacy in communications
- Verifying digital identities'''
        }
    }

    # Game messages
    MESSAGES = {
        'welcome': 'Welcome to Crypto Quest: The Secret Message!\nYou are a codebreaker who must solve various cryptographic puzzles to find the treasure.',
        'help': '''Available commands:
- look: Look around the current room
- inventory: Check your collected items
- take [item]: Pick up an item
- use [item]: Use an item
- solve [puzzle]: Attempt to solve a puzzle
- help: Show this help message
- quit: Exit the game''',
        'invalid_command': 'I don\'t understand that command.',
        'item_not_found': 'That item is not here.',
        'puzzle_not_found': 'That puzzle is not available here.',
        'puzzle_solved': 'Congratulations! You solved the puzzle!',
        'puzzle_failed': 'That\'s not the correct solution. Try again!',
        'game_complete': 'Congratulations! You have found the treasure and completed the game!'
    } 