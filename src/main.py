import logging
from tkinterdnd2 import TkinterDnD
from tkinter import Tk
from gui import create_gui  # Import the function here
from player import Player

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def initialize_application() -> tuple[TkinterDnD.Tk, Player]:
    """Initialize root window and player instance."""
    logging.info("Initializing the application...")
    try:
        root: TkinterDnD.Tk = TkinterDnD.Tk()
        player: Player = Player()
        return root, player
    except Exception as e:
        logging.error(f"Failed to initialize application: {e}", exc_info=True)
        raise

def run_application(root: TkinterDnD.Tk, player: Player) -> None:
    """Set up GUI and run the application."""
    logging.info("Setting up the GUI...")
    try:
        create_gui(root, player)  # Initialize the GUI here
        logging.info("Starting the main application loop.")
        root.mainloop()
    except Exception as e:
        logging.error(f"An error occurred while running the application: {e}", exc_info=True)
        raise

def main() -> None:
    """Run the music player app."""
    try:
        root, player = initialize_application()
        run_application(root, player)
    except Exception as e:
        logging.critical(f"Application crashed: {e}", exc_info=True)
    finally:
        logging.info("Application shutdown.")

if __name__ == "__main__":
    main()
