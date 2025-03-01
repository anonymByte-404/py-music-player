import logging
from tkinterdnd2 import TkinterDnD
from gui import create_gui
from player import Player

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()         # Log to the console
    ]
)

def initialize_application() -> tuple:
    """
    Initialize the main components of the application: the root window and player instance.
    
    Returns:
        tuple: A tuple containing the root window (TkinterDnD.Tk) and the Player instance.
    """
    logging.info("Initializing the application...")
    try:
        root = TkinterDnD.Tk()
        player = Player()
        return root, player
    except Exception as e:
        logging.error(f"Failed to initialize application: {e}", exc_info=True)
        raise

def run_application(root, player):
    """
    Set up the GUI and run the application.
    
    Args:
        root: The root window of the application.
        player: The Player instance to be used in the GUI.
    """
    logging.info("Setting up the GUI...")
    try:
        create_gui(root, player)
        logging.info("Starting the main application loop.")
        root.mainloop()
    except Exception as e:
        logging.error(f"An error occurred while running the application: {e}", exc_info=True)
        raise

def main():
    """Initialize and run the music player application."""
    try:
        root, player = initialize_application()
        run_application(root, player)
    except Exception as e:
        logging.critical(f"Application crashed: {e}", exc_info=True)
    finally:
        logging.info("Application shutdown.")

if __name__ == "__main__":
    main()