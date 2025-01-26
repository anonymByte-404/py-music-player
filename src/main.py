import logging
from tkinterdnd2 import TkinterDnD
from gui import create_gui
from player import Player

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_application() -> tuple:
  """Initialize the main components of the application: the root window and player instance."""
  logging.info("Initializing the application...")
  root = TkinterDnD.Tk()
  player = Player()
  return root, player

def run_application(root, player):
  """Set up the GUI and run the application."""
  logging.info("Setting up the GUI...")
  create_gui(root, player)
  logging.info("Starting the main application loop.")
  root.mainloop()

def main():
  """Initialize and run the music player application."""
  try:
    root, player = initialize_application()
    run_application(root, player)
  except Exception as e:
    logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
  main()
