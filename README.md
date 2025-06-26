
# 🔒 Crypto Quest: The Secret Message

![Crypto Quest Banner](https://res.cloudinary.com/dl4vtrbqr/image/upload/v1750945726/icon_yik8ls.png)


## 📜 Description

Crypto Quest is an interactive text-based adventure game designed to teach cryptography through engaging puzzles and challenges. In this exciting quest, you take on the role of a codebreaker navigating through various rooms, each containing unique cryptographic puzzles. Your mission is to solve these puzzles and uncover a mysterious secret. Each room presents encrypted messages that, when decrypted, reveal clues to help you progress further.

## ✨ Features

- **Multiple Rooms**: Each room offers unique cryptographic challenges.
- **Various Encryption Methods**: Includes puzzles based on Caesar cipher, Vigenère cipher, and more.
- **Collectible Tools**: Gather cryptographic tools and keys to aid in solving puzzles.
- **Progressive Difficulty**: Challenges become increasingly complex as you advance.
- **Interactive Commands**: Use commands like `look`, `take`, `use`, and `solve` to interact with the game.
- **Educational Content**: Learn about different cryptographic techniques and their historical context.

## 🛠️ Setup

### Prerequisites

- Ensure you have **Python 3.7+** installed on your system.

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/OmarDarwish483/CryptoQuest.git
   cd CryptoQuest
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the game:
   ```sh
   python main.py
   ```

## 🎮 How to Play

### Commands

- **`look`**: Look around the current room.
- **`inventory`**: Check your collected items.
- **`take [item]`**: Pick up an item.
- **`use [item]`**: Use an item.
- **`solve [puzzle]`**: Attempt to solve a puzzle.
- **`help`**: Show available commands.
- **`quit`**: Exit the game.

### Gameplay Tips

- **Collect Cryptographic Tools**: These tools will help you solve puzzles more efficiently.
- **Decrypt Messages**: Find clues hidden within encrypted messages to progress.
- **Explore Each Room**: Look for items and clues that might be hidden.
- **Use Commands Wisely**: Commands like `help` can provide guidance when you're stuck.

## 🎨 Game Assets

### Rooms and Items

- **Entrance Room**: Introduces the basics of the Caesar cipher.
- **Library Room**: Focuses on RSA encryption and asymmetric cryptography.
- **Study Room**: Emphasizes the importance of private keys.
- **Vault Room**: The final challenge where you find the treasure.

### Puzzles

- **Caesar Cipher**: Shift letters by a fixed number of positions.
- **Vigenère Cipher**: Use a keyword to encrypt and decrypt messages.
- **Atbash Cipher**: Reverse the alphabet to encode messages.
- **Binary and Morse Code**: Convert between text and binary/Morse code.

## 🔍 Technologies Used

- **Python**: The core programming language.
- **SymPy**: For prime number generation and modular arithmetic.
- **Pillow**: For image processing and modern visual styling.
- **Pygame**: For sound effects and interactive elements.
- **Requests**: For downloading and handling external resources.

## 📈 Possible Improvements

- **Additional Encryption Methods**: Include more complex cryptographic algorithms.
- **Multiplayer Mode**: Allow players to collaborate or compete in solving puzzles.
- **Graphical User Interface (GUI)**: Enhance the game with a visual interface.
- **Extended Educational Content**: Provide more in-depth explanations and historical context.

## 📊 Contributors

### Omar Hany Darwish

- **GitHub**: [OmarHanyDarwish](https://github.com/OmarDarwish483)
- **LinkedIn**: [Omar Hany Darwish](https://www.linkedin.com/in/omardrwish/)
- **Email**: darwishomar158@gmail.com

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Special thanks to the open-source community for their contributions and support.
- Inspired by the rich history and fascinating world of cryptography.

## 🎯 Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

---

**Crypto Quest: The Secret Message** is more than just a game; it's an educational journey through the world of cryptography. Join the quest and unlock the secrets hidden within!


## 📚 Additional Resources

- **Discrete.ipynb**: A Jupyter notebook demonstrating RSA key generation and encryption/decryption processes.
- **crypto_tools.py**: A Python module containing various cryptographic functions.
- **game_assets.py**: Handles game assets like images, sounds, and color schemes.
- **game_data.py**: Contains game data, including room descriptions, puzzles, and items.

### Discrete.ipynb

This Jupyter notebook provides a hands-on example of generating RSA keys and using them for encryption and decryption. It includes functions for:

- Generating prime numbers.
- Creating public and private RSA keys.
- Encrypting and decrypting messages using RSA.

### crypto_tools.py

This module includes static methods for various cryptographic functions:

- **Caesar Cipher**: Encrypt and decrypt text using a Caesar cipher.
- **Vigenère Cipher**: Encrypt and decrypt text using a Vigenère cipher.
- **Atbash Cipher**: Encrypt and decrypt text using an Atbash cipher.
- **Binary to Text**: Convert binary strings to text.
- **Text to Binary**: Convert text to binary strings.
- **Morse Code**: Convert between text and Morse code.

### game_assets.py

This script manages game assets such as images, sounds, and color schemes. It includes functions for:

- Downloading and resizing images from URLs.
- Loading images with modern styling.
- Defining color schemes and room backgrounds.

### game_data.py

This module contains the game's data, including:

- Room descriptions and available items.
- Puzzles and their solutions.
- Item descriptions and educational information.
- Game messages and hints.
