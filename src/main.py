import tkinter as tk
from player import Player
from gui import create_gui

def main():
    # Initialize the player instance
    player = Player()

    # Initialize the root window for the GUI
    root = tk.Tk()

    # Create the GUI with the player object
    create_gui(root, player)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
