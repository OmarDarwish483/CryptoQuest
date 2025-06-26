import os
import sys
from PIL import Image, ImageTk
import requests
from io import BytesIO
import pygame
import logging

# Initialize pygame for sound
pygame.mixer.init()

# Modern color scheme
COLORS = {
    'background': '#1A1A2E',  # Dark blue background
    'text': '#E6E6E6',        # Light gray text
    'button': '#4A90E2',      # Blue button
    'button_hover': '#357ABD', # Darker blue on hover
    'success': '#2ECC71',     # Green for success
    'error': '#E74C3C',       # Red for errors
    'warning': '#F1C40F',     # Yellow for warnings
    'easy': '#2ECC71',        # Green for easy puzzles
    'medium': '#F1C40F',      # Yellow for medium puzzles
    'hard': '#E74C3C',        # Red for hard puzzles
    'accent': '#FF6B6B',      # Coral accent color
    'secondary': '#4ECDC4',   # Turquoise secondary color
    'tertiary': '#45B7D1',    # Light blue tertiary color
    'overlay': 'rgba(0, 0, 0, 0.5)'  # Semi-transparent black overlay
}

# Room backgrounds with modern styling
ROOM_BACKGROUNDS = {
    'entrance': 'assets/entrance__0.jpg',
    'library': 'assets/shelve_2.jpg',
    'study': 'assets/cryptograp_0.jpg',
    'vault': 'assets/gl_2.jpg'
}

# Item icons with modern styling
ITEM_ICONS = {
    'note': 'assets/memory.png',
    'caesar_key': 'assets/caesar-cipher.png',
    'rsa_key': 'assets/key (2).png',
    'private_key': 'assets/key (1).png',
    'treasure_key': 'assets/key.png',
    'treasure': 'assets/treasure-chest.png'
}

# Puzzle difficulties with modern styling
PUZZLE_DIFFICULTIES = {
    'entrance_puzzle': 'easy',
    'library_puzzle': 'easy',
    'study_puzzle': 'easy',
    'vault_puzzle': 'easy'
}

def download_image(url, size=None):
    """Download and resize an image from URL"""
    try:
        print(f"Downloading image from {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        image = Image.open(BytesIO(response.content))
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        return None

def load_image(filename, size=None):
    """Load an image with error handling and modern styling"""
    try:
        # Check if we're running as a bundled executable
        if getattr(sys, 'frozen', False):
            # We're running in a bundle
            base_path = sys._MEIPASS
        else:
            # We're running in normal Python environment
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the full path
        full_path = os.path.join(base_path, filename)
        
        # Load the image
        image = Image.open(full_path)
        
        # Resize if size is specified
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        
        # Apply modern styling
        image = image.convert('RGBA')
        
        # Create a new image with a dark overlay
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 64))
        image = Image.alpha_composite(image, overlay)
        
        return ImageTk.PhotoImage(image)
    except Exception as e:
        logging.error(f"Error loading image {filename}: {str(e)}")
        # Return a default image or None
        return None

def get_difficulty_color(difficulty):
    """Get modern color for difficulty level"""
    return COLORS.get(difficulty, COLORS['medium'])