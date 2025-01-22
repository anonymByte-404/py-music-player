from tkinterdnd2 import TkinterDnD
from gui import create_gui
from player import Player

def main():
  """Initialize and run the music player application."""
  try:
    root = TkinterDnD.Tk()
    player = Player()
    create_gui(root, player)
    root.mainloop()
  except Exception as e:
    print(f"An error occured: {e}")

if __name__ == "__main__":
  main()
