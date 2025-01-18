import tkinter as tk
from tkinter import filedialog, messagebox
import os

def create_gui(root, player):
  """Create the GUI for the music player."""
  root.title("Desktop Music Player")
  root.geometry("400x380")

  # Playlist Listbox
  track_listbox = tk.Listbox(root, width=40, height=10)
  track_listbox.pack(pady=10)

  def update_playlist():
    """Update the playlist display."""
    track_listbox.delete(0, tk.END)
    for track in player.playlist:
      track_listbox.insert(tk.END, os.path.basename(track))
    highlight_first_track()

  def highlight_first_track():
    """Highlight the first song in the playlist."""
    if player.playlist:
      track_listbox.select_set(0)

  def load_folder():
    """Load MP3 files from a folder and update the playlist."""
    folder = filedialog.askdirectory()
    if folder:
      player.load_folder(folder)
      update_playlist()

  def add_file():
    """Add a single MP3 file to the playlist."""
    file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file:
      player.add_file(file)
      update_playlist()

  def toggle_repeat():
    """Toggle the repeat functionality."""
    player.toggle_repeat()
    update_repeat_button_style()

  def update_repeat_button_style():
    """Update the repeat button style based on the repeat state."""
    if player.repeat:
      repeat_button.config(bg="red", fg="white")
    else:
      repeat_button.config(bg="white", fg="black")

  def toggle_play():
    """Play or stop the currently selected track."""
    selected_track_index = track_listbox.curselection()
    if not selected_track_index:
      messagebox.showwarning("No Track Selected", "Please select a track to play.")
      return
    track_index = selected_track_index[0]
    player.toggle_play(track_index)
    update_play_button_style()

  def update_play_button_style():
    """Update the play button style based on the player's state."""
    if player.is_playing:
      play_button.config(text="Stop", bg="red", fg="white")
    else:
      play_button.config(text="Play", bg="green", fg="white")

  # Button for loading a folder
  load_button = tk.Button(root, text="Load Folder", command=load_folder, width=15, font=("Helvetica", 12, "bold"), bd=3)
  load_button.pack(pady=5)

  # Button for adding a file
  add_button = tk.Button(root, text="Add File", command=add_file, width=15, font=("Helvetica", 12, "bold"), bd=3)
  add_button.pack(pady=5)

  # Repeat button
  repeat_button = tk.Button(root, text="Repeat", command=toggle_repeat, width=15, font=("Helvetica", 12, "bold"), bd=3)
  repeat_button.pack(pady=5)

  # Play button
  play_button = tk.Button(root, text="Play", command=toggle_play, bg="green", fg="white", width=15, font=("Helvetica", 12, "bold"), bd=3)
  play_button.pack(pady=5)

  # Initial playlist update
  if not player.playlist:
    messagebox.showwarning("No Playlist", "No music files found! Please load a folder or add files.")
  else:
    update_playlist()

  def check_repeat():
    """Check if repeat is enabled and handle it."""
    if player.is_playing and player.repeat:
      player.handle_repeat()
    root.after(100, check_repeat)  # Check every 100ms

  check_repeat()
