import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
from PIL import Image, ImageTk
import json
from crypto_tools import CryptoTools
from game_data import GameData
import pyfiglet
from colorama import Fore, Style
from game_assets import (
    COLORS, ROOM_BACKGROUNDS, ITEM_ICONS,
    PUZZLE_DIFFICULTIES, load_image,
    get_difficulty_color
)
import math

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        self.configure(style='Hover.TButton')
        
    def on_leave(self, e):
        self.configure(style='TButton')

class CryptoQuestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Quest: The Secret Message")
        self.root.geometry("1280x720")
        self.root.configure(bg=COLORS['background'])

        # Initialize game state
        self.current_room = 'entrance'
        self.inventory = []
        self.solved_puzzles = set()
        self.crypto_tools = CryptoTools()
        self.game_data = GameData()
        self.progress = 0
        self.score = 0
        self.achievements = set()

        # Initialize image storage
        self.room_images = {}
        self.item_images = {}
        
        # Load images and create styles
        self.load_images()
        self.create_styles()

        # Create main layout
        self.create_main_layout()
        self.create_room_view()
        self.create_inventory_view()
        self.create_puzzle_view()
        self.create_status_bar()
        
        # Initialize game
        self.update_room_display()
        self.update_inventory_display()
        self.update_progress()

    def load_images(self):
        """Load all game images with modern styling"""
        print("Loading room backgrounds...")
        # Load room backgrounds
        for room, path in ROOM_BACKGROUNDS.items():
            print(f"Loading room background for {room} from {path}")
            self.room_images[room] = load_image(path, (400, 300))
            if self.room_images[room] is None:
                print(f"Failed to load room background for {room}")

        print("Loading item icons...")
        # Load item icons
        for item, path in ITEM_ICONS.items():
            print(f"Loading item icon for {item} from {path}")
            self.item_images[item] = load_image(path, (32, 32))
            if self.item_images[item] is None:
                print(f"Failed to load item icon for {item}")

    def create_styles(self):
        """Create modern styles with enhanced visual effects"""
        style = ttk.Style()
        
        # Configure theme settings
        style.theme_use('clam')
        
        # Base styles
        style.configure('TButton', 
                       background=COLORS['button'],
                       foreground=COLORS['background'],
                       padding=10,
                       relief='flat',
                       font=('Helvetica', 10))
        style.configure('Hover.TButton',
                       background=COLORS['button_hover'],
                       foreground=COLORS['background'],
                       padding=10,
                       relief='flat',
                       font=('Helvetica', 10, 'bold'))
        style.configure('TFrame',
                       background=COLORS['background'])
        style.configure('TLabel',
                       background=COLORS['background'],
                       foreground=COLORS['text'],
                       font=('Helvetica', 10))
        style.configure('TLabelframe',
                       background=COLORS['background'],
                       foreground=COLORS['text'])
        style.configure('TLabelframe.Label',
                       background=COLORS['background'],
                       foreground=COLORS['text'],
                       font=('Helvetica', 11, 'bold'))
        
        # Enhanced hover styles
        style.configure('Hover.TFrame',
                       background=COLORS['button_hover'])
        style.configure('Hover.TLabel',
                       foreground=COLORS['accent'],
                       font=('Helvetica', 10, 'bold'))
        
        # Progress bar style
        style.configure('TProgressbar',
                       background=COLORS['accent'],
                       troughcolor=COLORS['background'],
                       thickness=10)

    def create_main_layout(self):
        # Main container with modern look
        self.main_container = ttk.Frame(self.root, style='TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left panel (Room and Inventory)
        self.left_panel = ttk.Frame(self.main_container, style='TFrame')
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right panel (Puzzle and Controls)
        self.right_panel = ttk.Frame(self.main_container, style='TFrame')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_room_view(self):
        # Room frame with modern styling
        self.room_frame = ttk.LabelFrame(self.left_panel, text="Current Room", style='TLabelframe')
        self.room_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Room background with overlay and items
        self.room_canvas = tk.Canvas(self.room_frame, bg=COLORS['background'])
        self.room_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Room description with modern font
        self.room_text = scrolledtext.ScrolledText(self.room_frame, 
                                                 wrap=tk.WORD,
                                                 height=4,
                                                 bg=COLORS['background'],
                                                 fg=COLORS['text'],
                                                 font=('Helvetica', 10))
        self.room_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.room_text.configure(state='disabled')

        # Navigation buttons with modern look
        self.nav_frame = ttk.Frame(self.room_frame, style='TFrame')
        self.nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.prev_button = ModernButton(self.nav_frame, 
                                      text="← Previous Room",
                                      command=self.previous_room)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = ModernButton(self.nav_frame,
                                      text="Next Room →",
                                      command=self.next_room)
        self.next_button.pack(side=tk.RIGHT, padx=5)

    def create_inventory_view(self):
        # Inventory frame with modern styling
        self.inventory_frame = ttk.LabelFrame(self.left_panel, text="Inventory", style='TLabelframe')
        self.inventory_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inventory items with drag-and-drop support
        self.inventory_canvas = tk.Canvas(self.inventory_frame, bg=COLORS['background'])
        self.inventory_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.inventory_scrollbar = ttk.Scrollbar(self.inventory_frame, 
                                               orient="vertical",
                                               command=self.inventory_canvas.yview)
        self.inventory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.inventory_canvas.configure(yscrollcommand=self.inventory_scrollbar.set)
        
        self.inventory_items_frame = ttk.Frame(self.inventory_canvas, style='TFrame')
        self.inventory_canvas.create_window((0, 0), 
                                          window=self.inventory_items_frame,
                                          anchor="nw")

    def create_puzzle_view(self):
        # Puzzle frame with modern styling
        self.puzzle_frame = ttk.LabelFrame(self.right_panel, text="Current Puzzle", style='TLabelframe')
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Puzzle display with visual elements
        self.puzzle_canvas = tk.Canvas(self.puzzle_frame, bg=COLORS['background'])
        self.puzzle_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Puzzle controls
        self.puzzle_controls = ttk.Frame(self.puzzle_frame, style='TFrame')
        self.puzzle_controls.pack(fill=tk.X, padx=5, pady=5)

        self.solve_button = ModernButton(self.puzzle_controls,
                                       text="Solve Puzzle",
                                       command=self.solve_current_puzzle)
        self.solve_button.pack(side=tk.LEFT, padx=5)
        
        self.credits_button = ModernButton(self.puzzle_controls,
                                         text="Credits",
                                         command=self.show_credits)
        self.credits_button.pack(side=tk.RIGHT, padx=5)

    def create_status_bar(self):
        # Status bar with modern look
        self.status_frame = ttk.Frame(self.root, style='TFrame')
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

        # Status text
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.status_frame,
                                    textvariable=self.status_var,
                                    style='TLabel')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.status_frame,
                                          length=200,
                                          mode='determinate',
                                          style='TProgressbar')
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        
        # Score display
        self.score_label = ttk.Label(self.status_frame,
                                   text=f"Score: {self.score}",
                                   style='TLabel')
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        # Achievement indicator
        self.achievement_label = ttk.Label(self.status_frame,
                                         text="Achievements: 0",
                                         style='TLabel')
        self.achievement_label.pack(side=tk.RIGHT, padx=5)

    def update_room_display(self):
        """Update the room display with current items and description"""
        room = self.game_data.ROOMS[self.current_room]
        
        # Update room background
        if self.current_room in self.room_images:
            self.room_canvas.delete("all")
            self.room_canvas.create_image(0, 0,
                                        image=self.room_images[self.current_room],
                                        anchor="nw")
        
        # Update room description
        self.room_text.configure(state='normal')
        self.room_text.delete(1.0, tk.END)
        self.room_text.insert(tk.END, f"{room['description']}\n\n", "title")
        
        # Show available puzzles
        if room['puzzles']:
            self.room_text.insert(tk.END, "\nAvailable puzzles:\n", "subtitle")
            for puzzle in room['puzzles']:
                if puzzle not in self.solved_puzzles:
                    difficulty = PUZZLE_DIFFICULTIES.get(puzzle, 'medium')
                    self.room_text.insert(tk.END,
                                        f"• {puzzle} ({difficulty.upper()})\n",
                                        f"difficulty_{difficulty}")
        
        self.room_text.configure(state='disabled')
        
        # Place items on the room canvas
        self.place_items_on_canvas(room['items'])

    def place_items_on_canvas(self, items):
        """Place items on the room canvas with clickable functionality"""
        if not items:
            return
            
        # Calculate positions for items
        canvas_width = self.room_canvas.winfo_width()
        canvas_height = self.room_canvas.winfo_height()
        
        # Center items in the middle of the canvas
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # If there's only one item, place it in the center
        if len(items) == 1:
            item = items[0]
            item_frame = ttk.Frame(self.room_canvas, style='TFrame')
            item_frame.bind('<Enter>', lambda e, i=item: self.on_item_hover(e, i))
            item_frame.bind('<Leave>', lambda e: self.on_item_leave(e))
            item_frame.bind('<Button-1>', lambda e, i=item: self.take_item(i))
            
            if item in self.item_images:
                item_image = self.item_images[item]
                icon_label = ttk.Label(item_frame,
                                     image=item_image,
                                     style='TLabel')
                icon_label.image = item_image
                icon_label.pack(pady=5)
            
            name_label = ttk.Label(item_frame,
                                 text=item,
                                 style='TLabel')
            name_label.pack(pady=5)
            
            # Ensure the item stays within bounds
            x = max(50, min(center_x, canvas_width - 50))
            y = max(50, min(center_y, canvas_height - 50))
            
            self.room_canvas.create_window(x, y,
                                         window=item_frame,
                                         anchor="center",
                                         tags=("item", item))
        else:
            # For multiple items, arrange them in a circle around the center
            # Use a smaller radius to ensure items stay within bounds
            radius = min(canvas_width, canvas_height) // 4
            angle_step = 360 / len(items)
            
            for i, item in enumerate(items):
                angle = math.radians(i * angle_step)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                # Ensure the item stays within bounds
                x = max(50, min(x, canvas_width - 50))
                y = max(50, min(y, canvas_height - 50))
                
                item_frame = ttk.Frame(self.room_canvas, style='TFrame')
                item_frame.bind('<Enter>', lambda e, i=item: self.on_item_hover(e, i))
                item_frame.bind('<Leave>', lambda e: self.on_item_leave(e))
                item_frame.bind('<Button-1>', lambda e, i=item: self.take_item(i))
                
                if item in self.item_images:
                    item_image = self.item_images[item]
                    icon_label = ttk.Label(item_frame,
                                         image=item_image,
                                         style='TLabel')
                    icon_label.image = item_image
                    icon_label.pack(pady=5)
                
                name_label = ttk.Label(item_frame,
                                     text=item,
                                     style='TLabel')
                name_label.pack(pady=5)
                
                self.room_canvas.create_window(x, y,
                                             window=item_frame,
                                             anchor="center",
                                             tags=("item", item))

    def on_item_hover(self, event, item):
        """Handle item hover effect with enhanced visual feedback"""
        widget = event.widget
        widget.configure(style='Hover.TFrame')
        self.root.config(cursor="hand2")
        
        # Add glow effect
        for child in widget.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(style='Hover.TLabel')
        
        # Show item description in status bar
        description = self.game_data.ITEMS[item]['description']
        self.status_var.set(f"Click to take: {description}")

    def on_item_leave(self, event):
        """Handle item leave effect"""
        widget = event.widget
        widget.configure(style='TFrame')
        self.root.config(cursor="")
        
        # Remove glow effect
        for child in widget.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(style='TLabel')
        
        self.status_var.set("")

    def take_item(self, item):
        """Take an item from the room"""
        if item in self.game_data.ROOMS[self.current_room]['items']:
            self.inventory.append(item)
            self.game_data.ROOMS[self.current_room]['items'].remove(item)
            self.update_room_display()
            self.update_inventory_display()
            self.status_var.set(f"Took {item}")
            
            # Show success message
            messagebox.showinfo("Item Collected",
                              f"You collected the {item}!\n\n{self.game_data.ITEMS[item]['description']}")
        else:
            self.status_var.set("Item not found")

    def update_inventory_display(self):
        # Clear existing items
        for widget in self.inventory_items_frame.winfo_children():
            widget.destroy()
        
        if not self.inventory:
            ttk.Label(self.inventory_items_frame,
                     text="Your inventory is empty.",
                     style='TLabel').pack(pady=5)
        else:
            for item in self.inventory:
                item_frame = ttk.Frame(self.inventory_items_frame, style='TFrame')
                item_frame.pack(fill=tk.X, pady=2)
                
                if item in self.item_images:
                    icon_label = ttk.Label(item_frame,
                                         image=self.item_images[item],
                                         style='TLabel')
                    icon_label.image = self.item_images[item]
                    icon_label.pack(side=tk.LEFT, padx=5)
                
                ttk.Label(item_frame,
                         text=f"{item}: {self.game_data.ITEMS[item]['description']}",
                         style='TLabel').pack(side=tk.LEFT)
                
                # Add use button
                use_button = ModernButton(item_frame,
                                        text="Use",
                                        command=lambda i=item: self.use_item(i))
                use_button.pack(side=tk.RIGHT, padx=5)
        
        self.inventory_items_frame.update_idletasks()
        self.inventory_canvas.configure(scrollregion=self.inventory_canvas.bbox("all"))

    def solve_current_puzzle(self):
        """Solve the current puzzle in the room"""
        # Get current puzzle
        room = self.game_data.ROOMS[self.current_room]
        if not room['puzzles']:
            messagebox.showinfo("No Puzzle",
                              "There are no puzzles in this room.")
            return
        
        # Find first unsolved puzzle
        current_puzzle_name = None
        for puzzle in room['puzzles']:
            if puzzle not in self.solved_puzzles:
                current_puzzle_name = puzzle
                break
        
        if current_puzzle_name:
            self.solve_puzzle(current_puzzle_name)
        else:
            messagebox.showinfo("All Puzzles Solved",
                              "You have solved all puzzles in this room!")

    def solve_puzzle(self, puzzle_name):
        """Solve a puzzle with the given name"""
        if puzzle_name not in self.game_data.PUZZLES:
            messagebox.showerror("Error",
                               "Puzzle not found!")
            return
        
        # Get the puzzle data
        puzzle_data = self.game_data.PUZZLES[puzzle_name]
        
        # Create puzzle-specific interface
        self.create_puzzle_interface(puzzle_data)
        
        # Show puzzle dialog
        dialog = PuzzleDialog(self.root, puzzle_data, self.crypto_tools)
        result = dialog.show()
        
        if result:
            self.solved_puzzles.add(puzzle_name)
            if puzzle_data['reward']:
                self.inventory.append(puzzle_data['reward'])
                messagebox.showinfo("Success!",
                                  f"You solved the puzzle and received: {puzzle_data['reward']}")
            self.update_progress()
            self.update_inventory_display()
            self.check_achievements()

    def create_puzzle_interface(self, puzzle):
        # Clear previous puzzle interface
        for widget in self.puzzle_canvas.winfo_children():
            widget.destroy()
        
        # Create puzzle-specific interface based on type
        if puzzle['type'] == 'caesar':
            self.create_caesar_interface(puzzle)
        elif puzzle['type'] == 'vigenere':
            self.create_vigenere_interface(puzzle)
        elif puzzle['type'] == 'morse':
            self.create_morse_interface(puzzle)
        elif puzzle['type'] == 'binary':
            self.create_binary_interface(puzzle)

    def create_caesar_interface(self, puzzle):
        """Create Caesar cipher interface with hardcoded answers and alphabet reference"""
        frame = ttk.Frame(self.puzzle_canvas, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(frame,
                 text="Caesar Cipher",
                 style='TLabel').pack(pady=5)
        
        # Alphabet reference
        alphabet_frame = ttk.Frame(frame, style='TFrame')
        alphabet_frame.pack(pady=5)
        
        # Original alphabet
        style = ttk.Style()
        style.configure('Mono.TLabel', font=('Courier', 12))  # Use Courier or another monospace font

    # Original and shifted alphabets
        original = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        shifted = "D E F G H I J K L M N O P Q R S T U V W X Y Z A B C"

    # Create labels with monospace font
        ttk.Label(alphabet_frame,
              text=f"Original: {original}",
              style='Mono.TLabel').pack()
        ttk.Label(alphabet_frame,
              text=f"Shift=3:  {shifted}",
              style='Mono.TLabel').pack()
        
        # Encrypted text
        ttk.Label(frame,
                 text="Encrypted Text:",
                 style='TLabel').pack(pady=5)
        ttk.Label(frame,
                 text=puzzle['encrypted_text'],
                 style='TLabel').pack(pady=5)
        
        # Shift controls
        shift_frame = ttk.Frame(frame, style='TFrame')
        shift_frame.pack(pady=5)
        
        ttk.Label(shift_frame,
                 text="Shift:",
                 style='TLabel').pack(side=tk.LEFT, padx=5)
        
        self.shift_var = tk.IntVar(value=0)
        shift_scale = ttk.Scale(shift_frame,
                              from_=0,
                              to=3,  # Only goes up to 3 since that's our solution
                              variable=self.shift_var,
                              orient=tk.HORIZONTAL,
                              command=lambda v: self.update_caesar_preview(puzzle['encrypted_text'], int(float(v))))
        shift_scale.pack(side=tk.LEFT, padx=5)
        
        # Preview text with larger font
        self.preview_label = ttk.Label(frame,
                                     text="",
                                     style='TLabel',
                                     font=('Helvetica', 14, 'bold'))
        self.preview_label.pack(pady=10)
        
        # Character-by-character preview
        self.char_preview_frame = ttk.Frame(frame, style='TFrame')
        self.char_preview_frame.pack(pady=5)
        
        # Initialize character labels
        self.char_labels = []
        for i in range(len(puzzle['encrypted_text'])):
            label = ttk.Label(self.char_preview_frame,
                            text="",
                            style='TLabel',
                            font=('Helvetica', 12))
            label.pack(side=tk.LEFT, padx=2)
            self.char_labels.append(label)
        
        # Hint button
        ttk.Button(frame,
                  text="Show Hint",
                  command=lambda: self.show_puzzle_hint(puzzle)).pack(pady=5)
        
        # Educational information
        ttk.Label(frame,
                 text="Educational Tip:",
                 style='TLabel',
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        ttk.Label(frame,
                 text="Use the alphabet reference above to see how each letter shifts.\n"
                      "For example, with shift=3: A→D, B→E, C→F, etc.\n"
                      "Move the slider to see the decryption in action.",
                 style='TLabel',
                 wraplength=300).pack(pady=5)
        
        # Initialize with the encrypted text
        for i, char in enumerate(puzzle['encrypted_text']):
            self.char_labels[i].configure(text=char)

    def update_caesar_preview(self, text, shift):
        """Update Caesar cipher preview with correct shifts"""
        # Calculate the decrypted text based on the shift
        decrypted = self.crypto_tools.caesar_cipher(text, -shift)
        
        # Update each character individually
        for i, char in enumerate(decrypted):
            self.char_labels[i].configure(text=char)
            
            # Color the character when it's in the correct position
            if shift == 3:  # At shift 3, all characters are correct
                self.char_labels[i].configure(foreground=COLORS['success'])
            else:
                self.char_labels[i].configure(foreground=COLORS['text'])
        
        # Update the full preview
        self.preview_label.configure(text=decrypted)
        
        # Add visual feedback when correct
        if shift == 3:
            self.preview_label.configure(foreground=COLORS['success'])
        else:
            self.preview_label.configure(foreground=COLORS['text'])

    def create_vigenere_interface(self, puzzle):
        """Create Vigenère cipher interface"""
        frame = ttk.Frame(self.puzzle_canvas, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(frame,
                 text="Vigenère Cipher",
                 style='TLabel').pack(pady=5)
        
        # Encrypted text
        ttk.Label(frame,
                 text="Encrypted Text:",
                 style='TLabel').pack(pady=5)
        ttk.Label(frame,
                 text=puzzle['encrypted_text'],
                 style='TLabel').pack(pady=5)
        
        # Key entry
        key_frame = ttk.Frame(frame, style='TFrame')
        key_frame.pack(pady=5)
        ttk.Label(key_frame,
                 text="Key:",
                 style='TLabel').pack(side=tk.LEFT, padx=5)
        self.key_var = tk.StringVar()
        ttk.Entry(key_frame,
                 textvariable=self.key_var).pack(side=tk.LEFT, padx=5)
        
        # Preview text
        self.preview_label = ttk.Label(frame,
                                     text="",
                                     style='TLabel')
        self.preview_label.pack(pady=5)
        
        # Update preview when key changes
        self.key_var.trace_add('write', lambda *args: self.update_vigenere_preview(puzzle['encrypted_text']))

    def update_vigenere_preview(self, text):
        """Update Vigenère cipher preview"""
        key = self.key_var.get()
        if key:
            decrypted = self.crypto_tools.vigenere_cipher(text, key, decrypt=True)
            self.preview_label.configure(text=decrypted)

    def create_morse_interface(self, puzzle):
        """Create Morse code interface"""
        frame = ttk.Frame(self.puzzle_canvas, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(frame,
                 text="Morse Code",
                 style='TLabel').pack(pady=5)
        
        # Encrypted text
        ttk.Label(frame,
                 text="Morse Code:",
                 style='TLabel').pack(pady=5)
        ttk.Label(frame,
                 text=puzzle['encrypted_text'],
                 style='TLabel').pack(pady=5)
        
        # Preview text
        self.preview_label = ttk.Label(frame,
                                     text="",
                                     style='TLabel')
        self.preview_label.pack(pady=5)
        
        # Decode button
        ttk.Button(frame,
                  text="Decode",
                  command=lambda: self.update_morse_preview(puzzle['encrypted_text'])).pack(pady=5)

    def update_morse_preview(self, text):
        """Update Morse code preview"""
        try:
            decrypted = self.crypto_tools.morse_to_text(text)
            self.preview_label.configure(text=decrypted)
        except Exception as e:
            self.preview_label.configure(text=f"Error: {str(e)}")

    def create_binary_interface(self, puzzle):
        """Create binary code interface"""
        frame = ttk.Frame(self.puzzle_canvas, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(frame,
                 text="Binary Code",
                 style='TLabel').pack(pady=5)
        
        # Encrypted text
        ttk.Label(frame,
                 text="Binary:",
                 style='TLabel').pack(pady=5)
        ttk.Label(frame,
                 text=puzzle['encrypted_text'],
                 style='TLabel').pack(pady=5)
        
        # Preview text
        self.preview_label = ttk.Label(frame,
                                     text="",
                                     style='TLabel')
        self.preview_label.pack(pady=5)
        
        # Decode button
        ttk.Button(frame,
                  text="Decode",
                  command=lambda: self.update_binary_preview(puzzle['encrypted_text'])).pack(pady=5)

    def update_binary_preview(self, text):
        """Update binary code preview"""
        try:
            decrypted = self.crypto_tools.binary_to_text(text)
            self.preview_label.configure(text=decrypted)
        except Exception as e:
            self.preview_label.configure(text=f"Error: {str(e)}")

    def check_achievements(self):
        # Check and award achievements
        achievements = {
            'first_puzzle': len(self.solved_puzzles) >= 1,
            'half_way': len(self.solved_puzzles) >= len(self.game_data.PUZZLES) // 2,
            'master_cryptographer': len(self.solved_puzzles) == len(self.game_data.PUZZLES),
            'treasure_hunter': 'treasure' in self.inventory
        }
        
        for achievement, condition in achievements.items():
            if condition and achievement not in self.achievements:
                self.achievements.add(achievement)
                self.show_achievement(achievement)
                self.score += 100
                self.update_score()

    def show_achievement(self, achievement):
        # Show achievement popup with animation
        messagebox.showinfo("Achievement Unlocked!",
                          f"You unlocked the '{achievement}' achievement!")

    def update_score(self):
        self.score_label.configure(text=f"Score: {self.score}")
        self.achievement_label.configure(text=f"Achievements: {len(self.achievements)}")

    def update_progress(self):
        total_puzzles = len(self.game_data.PUZZLES)
        solved_puzzles = len(self.solved_puzzles)
        self.progress = (solved_puzzles / total_puzzles) * 100
        self.progress_bar['value'] = self.progress

    def previous_room(self):
        current_index = list(self.game_data.ROOMS.keys()).index(self.current_room)
        if current_index > 0:
            self.current_room = list(self.game_data.ROOMS.keys())[current_index - 1]
            self.update_room_display()

    def next_room(self):
        current_index = list(self.game_data.ROOMS.keys()).index(self.current_room)
        if current_index < len(self.game_data.ROOMS) - 1:
            self.current_room = list(self.game_data.ROOMS.keys())[current_index + 1]
            self.update_room_display()

    def use_item(self, item):
        """Use an item with educational information"""
        if item in self.inventory:
            if self.game_data.ITEMS[item]['usable']:
                # Show educational information
                educational_info = self.game_data.ITEMS[item]['educational_info']
                messagebox.showinfo(f"Educational Information - {item}", educational_info)
                
                # Get current puzzle
                room = self.game_data.ROOMS[self.current_room]
                current_puzzle = None
                for puzzle in room['puzzles']:
                    if puzzle not in self.solved_puzzles:
                        current_puzzle = puzzle
                        break
                
                if current_puzzle:
                    puzzle = self.game_data.PUZZLES[current_puzzle]
                    self.status_var.set(f"Used {item} - Check the educational information!")
                else:
                    self.status_var.set(f"No active puzzle to use {item} on")
            else:
                self.status_var.set(f"Can't use {item}")
        else:
            self.status_var.set("Item not in inventory")

    def get_item_effect(self, item, puzzle):
        """Get the effect of using an item on a puzzle"""
        item_effects = {
            'caesar_key': {
                'caesar': "The key reveals the correct shift value for the Caesar cipher.",
                'default': "This key is specifically for Caesar cipher puzzles."
            },
            'vigenere_key': {
                'vigenere': "The key reveals the correct keyword for the Vigenère cipher.",
                'default': "This key is specifically for Vigenère cipher puzzles."
            },
            'morse_decoder': {
                'morse': "The decoder helps translate Morse code into readable text.",
                'default': "This decoder is specifically for Morse code puzzles."
            },
            'binary_converter': {
                'binary': "The converter helps translate binary code into readable text.",
                'default': "This converter is specifically for binary code puzzles."
            },
            'note': {
                'all': "The note contains important clues about the current puzzle."
            }
        }
        
        effect = item_effects.get(item, {}).get(puzzle['type'])
        if not effect:
            effect = item_effects.get(item, {}).get('default', "This item has no effect here.")
        
        return effect

    def show_puzzle_hint(self, puzzle):
        """Show puzzle hint with computer science context"""
        hint = puzzle.get('hint', 'No hint available.')
        computer_science_context = {
            'caesar': "The Caesar cipher is one of the earliest known encryption techniques, used by Julius Caesar to protect military messages. In computer science, it's a simple example of substitution ciphers and is often used to teach basic cryptography concepts.",
            'vigenere': "The Vigenère cipher is a method of encrypting alphabetic text using a simple form of polyalphabetic substitution. It was considered unbreakable for centuries and is an important step in the evolution of cryptography.",
            'morse': "Morse code was developed in the 1830s for telegraphy. In computer science, it's an example of a binary encoding system, where each character is represented by a unique sequence of dots and dashes.",
            'binary': "Binary code is the fundamental language of computers, using only 0s and 1s. Each character in the ASCII table can be represented by an 8-bit binary number, making it essential for data storage and transmission."
        }
        
        context = computer_science_context.get(puzzle['type'], '')
        full_hint = f"{hint}\n\nComputer Science Context:\n{context}"
        messagebox.showinfo("Puzzle Hint", full_hint)

    def show_credits(self):
        """Show credits dialog with team members"""
        credits_text = """Crypto Quest: The Secret Message

Development Team:
• Jasmin Nasser
• Omar Hany Darwish
• Bassant Mohamed
• Basmala Salah

Thank you for playing!"""
        
        messagebox.showinfo("Credits", credits_text)

class PuzzleDialog:
    def __init__(self, parent, puzzle, crypto_tools):
        self.parent = parent
        self.puzzle = puzzle
        self.crypto_tools = crypto_tools
        self.result = False
        
    def show(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Solve Puzzle")
        dialog.geometry("400x300")
        dialog.configure(bg=COLORS['background'])
        
        # Puzzle content
        ttk.Label(dialog,
                 text=self.puzzle['encrypted_text'],
                 style='TLabel').pack(pady=10)
        
        ttk.Label(dialog,
                 text=f"Hint: {self.puzzle['hint']}",
                 style='TLabel').pack(pady=5)
        
        # Solution entry
        solution_var = tk.StringVar()
        ttk.Entry(dialog,
                 textvariable=solution_var).pack(pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog, style='TFrame')
        button_frame.pack(pady=10)
        
        ModernButton(button_frame,
                    text="Submit",
                    command=lambda: self.check_solution(dialog, solution_var.get())).pack(side=tk.LEFT, padx=5)
        
        ModernButton(button_frame,
                    text="Cancel",
                    command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        dialog.transient(self.parent)
        dialog.grab_set()
        self.parent.wait_window(dialog)
        return self.result
    
    def check_solution(self, dialog, solution):
        if solution.upper() == self.puzzle['solution']:
            self.result = True
            dialog.destroy()
        else:
            messagebox.showerror("Incorrect",
                               "That's not the correct solution. Try again!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoQuestGUI(root)
    root.mainloop()