from tkinterdnd2 import TkinterDnD
import tkinter as tk
from gui import create_gui
from player import Player

def main():
  """Initialize and run the music player application."""
  root = TkinterDnD.Tk()
  player = Player()
  create_gui(root, player)
  root.mainloop()

if __name__ == "__main__":
  main()
