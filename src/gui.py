import logging
import os
from tkinter import messagebox, ttk, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from mutagen.mp3 import MP3
import tkinter as tk
from typing import Optional, TypeVar, Generic, Tuple

T = TypeVar('T')

class Constant(Generic[T]):
  """Defines an immutable constant that cannot be modified after creation."""
  def __init__(self, value: T) -> None:
    self._value: T = value

  @property
  def value(self) -> T:
    return self._value

  @value.setter
  def value(self, value: T) -> None:
    raise AttributeError("This Constant is read-only and cannot be reassigned.")

# Constants using Constant class
BACKGROUND_COLOR: Constant[str] = Constant("#262323")
TEXT_COLOR: Constant[str] = Constant("#DFD7D7")
BUTTON_COLOR: Constant[str] = Constant("#423F3F")
HIGHLIGHT_COLOR: Constant[str] = Constant("#a7a7a7")
FONT: Constant[Tuple[str, int, str]] = Constant(("Helvetica", 12, "bold"))
FONT_SMALL: Constant[str] = Constant(("Helvetica", 10))
WINDOW_SIZE: Constant[str] = Constant("420x640")

# Configure logging
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  handlers=[
    logging.FileHandler("player.log"),  # Log to a file
    logging.StreamHandler()             # Log to the console
  ]
)

def create_gui(root: TkinterDnD.Tk, player: object) -> None:
  """Set up the GUI components for the Music Player."""
  try:
    gui = MusicPlayerGUI(root, player)
  except Exception as e:
    logging.error(f"Failed to create GUI: {e}", exc_info=True)
    raise

class MusicPlayerGUI:
  def __init__(self, root: TkinterDnD.Tk, player: object) -> None:
    self.root = root
    self.player = player
    self.track_listbox: Optional[tk.Listbox] = None
    self.status_bar: Optional[tk.Label] = None
    self.progress_bar: Optional[ttk.Progressbar] = None
    self.play_button: Optional[tk.Button] = None
    self.repeat_button: Optional[tk.Button] = None
    self.setup_gui()

  def setup_gui(self) -> None:
    """Initialize the GUI for the Desktop Music Player."""
    try:
      self.configure_root_window()
      self.create_title_label()
      self.create_playlist_section()
      self.create_volume_controls()
      self.create_buttons()
      self.create_status_bar()
      self.create_progress_bar()
      self.configure_drag_and_drop()
      self.bind_keyboard_shortcuts()
      self.update_ui()
      self.root.protocol("WM_DELETE_WINDOW", self.handle_close)
    except Exception as e:
      logging.error(f"Failed to create GUI: {e}", exc_info=True)
      raise

  def configure_root_window(self) -> None:
    """Configure the main application window."""
    self.root.title("Desktop Music Player")
    self.root.geometry(WINDOW_SIZE.value)
    self.root.resizable(False, False)
    self.root.config(bg=BACKGROUND_COLOR.value)

  def create_title_label(self) -> None:
    """Create the title label for the application."""
    title_label = tk.Label(
      self.root,
      text="Desktop Music Player",
      font=("Helvetica", 16, "bold"),
      pady=10,
      bg=BACKGROUND_COLOR.value,
      fg=TEXT_COLOR.value
    )
    title_label.pack()

  def create_playlist_section(self) -> None:
    """Create the playlist display area with scrollbar."""
    playlist_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR.value)
    playlist_frame.pack(pady=5)

    self.track_listbox = tk.Listbox(
      playlist_frame,
      width=53,
      height=12,
      font=FONT_SMALL.value,
      bg=BACKGROUND_COLOR.value,
      fg=TEXT_COLOR.value,
      selectbackground=HIGHLIGHT_COLOR.value,
      selectforeground=BACKGROUND_COLOR.value
    )
    self.track_listbox.grid(row=0, column=0)

    scrollbar = tk.Scrollbar(
      playlist_frame,
      orient=tk.VERTICAL,
      command=self.track_listbox.yview,
      bg=BUTTON_COLOR.value
    )
    scrollbar.grid(row=0, column=1, sticky="ns")
    self.track_listbox.config(yscrollcommand=scrollbar.set)

  def create_volume_controls(self) -> None:
    """Create the volume slider controls."""
    volume_label = tk.Label(
      self.root,
      text="Volume",
      font=FONT.value,
      bg=BACKGROUND_COLOR.value,
      fg=TEXT_COLOR.value
    )
    volume_label.pack(pady=(5, 0))

    volume_slider = tk.Scale(
      self.root,
      from_=0,
      to=100,
      orient=tk.HORIZONTAL,
      command=lambda value: self.set_volume(float(value) / 100),
      length=350,
      bg=BACKGROUND_COLOR.value,
      fg=TEXT_COLOR.value,
      sliderlength=20
    )
    volume_slider.set(50)
    volume_slider.pack(pady=(0, 5), padx=5)

  def set_volume(self, value: float) -> None:
    """Set the volume for the music player."""
    self.player.set_volume(value)

  def create_buttons(self) -> None:
    """Create the control buttons."""
    button_frame_1 = tk.Frame(self.root, bg=BACKGROUND_COLOR.value)
    button_frame_1.pack(pady=5)

    self.create_control_button(button_frame_1, "Load Folder", self.load_folder).grid(row=0, column=0, padx=5)
    self.create_control_button(button_frame_1, "Add File", self.add_file).grid(row=0, column=1, padx=5)

    self.create_control_button(self.root, "Remove Track", self.remove_selected_track, width=38).pack(pady=5)

    button_frame_2 = tk.Frame(self.root, bg=BACKGROUND_COLOR.value)
    button_frame_2.pack(pady=5)

    self.create_control_button(button_frame_2, "Move Up", lambda: self.move_track(up=True)).grid(row=0, column=0, padx=5)
    self.create_control_button(button_frame_2, "Move Down", lambda: self.move_track(up=False)).grid(row=0, column=1, padx=5)

    self.create_control_button(self.root, "Shuffle", self.shuffle_playlist, width=38).pack(pady=5)

    self.repeat_button = self.create_control_button(self.root, "Repeat", self.toggle_repeat, width=38)
    self.repeat_button.pack(pady=5)

    self.play_button = self.create_control_button(self.root, "Play", self.toggle_play, width=38, bg="green", fg="white")
    self.play_button.pack(pady=5)

  def create_control_button(self, parent: tk.Widget, text: str, command: callable, width: int = 18, bg: str = BACKGROUND_COLOR.value, fg: str = TEXT_COLOR.value) -> tk.Button:
    """Helper function to create a styled button."""
    return tk.Button(
      parent,
      text=text,
      command=command,
      width=width,
      font=FONT.value,
      bd=3,
      bg=bg,
      fg=fg
    )

  def create_status_bar(self) -> None:
    """Create the status bar to display current track info."""
    self.status_bar = tk.Label(
      self.root,
      text="No track playing",
      bd=1,
      relief=tk.SUNKEN,
      anchor=tk.W,
      font=FONT_SMALL.value,
      bg=BACKGROUND_COLOR.value,
      fg=TEXT_COLOR.value
    )
    self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

  def create_progress_bar(self) -> None:
    """Create a progress bar to show playback progress."""
    self.progress_bar = ttk.Progressbar(
      self.root,
      orient=tk.HORIZONTAL,
      length=400,
      mode="determinate"
    )
    self.progress_bar.pack(pady=5)

  def configure_drag_and_drop(self) -> None:
    """Configure drag-and-drop functionality for the application."""
    def handle_dragged_files(event) -> None:
      paths = self.root.tk.splitlist(event.data)
      for path in paths:
        if os.path.isdir(path):
          self.player.load_folder(path)
        elif os.path.isfile(path) and path.endswith(".mp3"):
          self.player.add_file(path)
        else:
          messagebox.showwarning("Unsupported File", f"Cannot add: {os.path.basename(path)}")
      self.update_playlist_display()

    self.root.drop_target_register(DND_FILES)
    self.root.dnd_bind("<<Drop>>", handle_dragged_files)

  def bind_keyboard_shortcuts(self) -> None:
    """Bind keyboard shortcuts for common actions."""
    self.root.bind("<space>", lambda event: self.toggle_play())

  def update_ui(self) -> None:
    """Update the UI periodically."""
    self.update_playlist_display()
    self.update_status_bar()
    self.update_progress_bar()
    self.monitor_repeat_mode()
    self.root.after(1000, self.update_ui)

  def update_playlist_display(self) -> None:
    """Update the playlist display to reflect the current state."""
    self.track_listbox.delete(0, tk.END)
    for index, track in enumerate(self.player.playlist):
      try:
        audio = MP3(track)
        duration = int(audio.info.length)
        mins, secs = divmod(duration, 60)
        duration_str = f"{mins}:{secs:02d}"
      except Exception as e:
        logging.error(f"Error reading track duration: {e}")
        duration_str = "Unknown"
      track_name = os.path.basename(track)
      display_name = f"> {track_name} ({duration_str})" if index == self.player.current_track_index else f"{track_name} ({duration_str})"
      self.track_listbox.insert(tk.END, display_name)
    self.highlight_current_track()

  def highlight_current_track(self) -> None:
    """Highlight the currently playing track in the playlist."""
    if self.player.is_playing and self.player.current_track_index is not None:
      self.track_listbox.select_clear(0, tk.END)
      self.track_listbox.select_set(self.player.current_track_index)
      self.track_listbox.see(self.player.current_track_index)

  def update_status_bar(self) -> None:
    """Update the status bar with the current track details."""
    if self.player.is_playing and self.player.current_track_index is not None:
      track = self.player.playlist[self.player.current_track_index]
      self.status_bar.config(text=f"Now Playing: {os.path.basename(track)}")
    else:
      self.status_bar.config(text="No track playing")

  def update_progress_bar(self) -> None:
    """Update the progress bar based on the current playback position."""
    if self.player.is_playing:
      position = self.player.get_position()
      self.progress_bar["value"] = position
    else:
      self.progress_bar["value"] = 0

  def monitor_repeat_mode(self) -> None:
    """Monitor the repeat mode and update the button state."""
    if self.player.repeat:
      self.repeat_button.config(bg="blue")
    else:
      self.repeat_button.config(bg=BUTTON_COLOR.value)

  def toggle_play(self) -> None:
    """Toggle between play and pause."""
    if self.player.is_playing:
      self.player.pause()
      self.play_button.config(text="Play")
    else:
      self.player.play()
      self.play_button.config(text="Pause")

  def toggle_repeat(self) -> None:
    """Toggle repeat mode."""
    self.player.toggle_repeat()
    self.monitor_repeat_mode()

  def load_folder(self) -> None:
    """Load a folder and add all mp3 files to the playlist."""
    folder = filedialog.askdirectory()
    if folder:
      self.player.load_folder(folder)
      self.update_playlist_display()

  def add_file(self) -> None:
    """Add a file to the playlist."""
    file = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file:
      self.player.add_file(file)
      self.update_playlist_display()

  def remove_selected_track(self) -> None:
    """Remove the selected track from the playlist."""
    try:
      selected_index = self.track_listbox.curselection()[0]
      self.player.remove_track(selected_index)
      self.update_playlist_display()
    except IndexError:
      pass

  def move_track(self, up: bool) -> None:
    """Move the selected track up or down in the playlist."""
    try:
      selected_index = self.track_listbox.curselection()[0]
      self.player.move_track(selected_index, up)
      self.update_playlist_display()
    except IndexError:
      pass

  def shuffle_playlist(self) -> None:
    """Shuffle the playlist."""
    self.player.shuffle_playlist()
    self.update_playlist_display()

  def handle_close(self) -> None:
    """Handle window close event."""
    self.player.stop()
    self.root.quit()
