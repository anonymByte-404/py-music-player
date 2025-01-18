import tkinter as tk
from player import Player
from gui import create_gui

def main():
  """Initialize and run the music player application."""
  player = Player()
  root = tk.Tk()
  create_gui(root, player)
  root.mainloop()

if __name__ == "__main__":
  main()
