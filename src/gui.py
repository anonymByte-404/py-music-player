import tkinter as tk
from tkinter import filedialog, messagebox
import os

def create_gui(root, player):
  """Create the GUI for the music player."""
  root.title("Desktop Music Player")
  root.geometry("420x600")

  title_label = tk.Label(root, text="Desktop Music Player", font=("Helvetica", 16, "bold"), pady=10)
  title_label.pack()

  track_listbox = tk.Listbox(root, width=53, height=12, font=("Helvetica", 10))  
  track_listbox.pack(pady=5)

  def update_playlist():
    """Update the playlist display and highlight the current track."""
    track_listbox.delete(0, tk.END)
    for index, track in enumerate(player.playlist):
      track_name = os.path.basename(track)
      display_name = f"> {track_name}" if index == player.current_track_index else track_name
      track_listbox.insert(tk.END, display_name)
    highlight_current_track()

  def highlight_current_track():
    """Highlight the currently playing track in the playlist."""
    if player.is_playing and player.current_track_index is not None:
      track_listbox.select_clear(0, tk.END)
      track_listbox.select_set(player.current_track_index)
      track_listbox.see(player.current_track_index)

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

  def remove_selected_track():
    """Remove the selected track from the playlist."""
    selected_track_index = track_listbox.curselection()
    if not selected_track_index:
      messagebox.showwarning("No Track Selected", "Please select a track to remove.")
      return
    track_index = selected_track_index[0]
    player.remove_track(track_index)
    update_playlist()

  def move_track_up():
    """Move the selected track up in the playlist."""
    selected_track_index = track_listbox.curselection()
    if not selected_track_index:
      messagebox.showwarning("No Track Selected", "Please select a track to move.")
      return
    track_index = selected_track_index[0]
    if track_index > 0:
      player.move_track(track_index, track_index - 1)
      update_playlist()

  def move_track_down():
    """Move the selected track down in the playlist."""
    selected_track_index = track_listbox.curselection()
    if not selected_track_index:
      messagebox.showwarning("No Track Selected", "Please select a track to move.")
      return
    track_index = selected_track_index[0]
    if track_index < len(player.playlist) - 1:
      player.move_track(track_index, track_index + 1)
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
    update_playlist()

  def update_play_button_style():
    """Update the play button style based on the player's state."""
    if player.is_playing:
      play_button.config(text="Stop", bg="red", fg="white")
    else:
      play_button.config(text="Play", bg="green", fg="white")

  def set_volume(value):
    """Set the volume of the player."""
    volume = float(value) / 100
    player.set_volume(volume)

  volume_label = tk.Label(root, text="Volume", font=("Helvetica", 12, "bold"))
  volume_label.pack(pady=(5, 0))

  volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, length=350)
  volume_slider.set(50)
  volume_slider.pack(pady=(0, 5), padx=5)

  button_frame_1 = tk.Frame(root)
  button_frame_1.pack(pady=5)

  load_button = tk.Button(button_frame_1, text="Load Folder", command=load_folder, width=18, font=("Helvetica", 12, "bold"), bd=3)
  load_button.grid(row=0, column=0, padx=5)

  add_button = tk.Button(button_frame_1, text="Add File", command=add_file, width=18, font=("Helvetica", 12, "bold"), bd=3)
  add_button.grid(row=0, column=1, padx=5)

  remove_button = tk.Button(root, text="Remove Track", command=remove_selected_track, width=38, font=("Helvetica", 12, "bold"), bd=3)
  remove_button.pack(pady=5)

  button_frame_2 = tk.Frame(root)
  button_frame_2.pack(pady=5)

  move_up_button = tk.Button(button_frame_2, text="Move Up", command=move_track_up, width=18, font=("Helvetica", 12, "bold"), bd=3)
  move_up_button.grid(row=0, column=0, padx=5)

  move_down_button = tk.Button(button_frame_2, text="Move Down", command=move_track_down, width=18, font=("Helvetica", 12, "bold"), bd=3)
  move_down_button.grid(row=0, column=1, padx=5)

  repeat_button = tk.Button(root, text="Repeat", command=toggle_repeat, width=38, font=("Helvetica", 12, "bold"), bd=3)
  repeat_button.pack(pady=5)

  play_button = tk.Button(root, text="Play", command=toggle_play, bg="green", fg="white", width=38, font=("Helvetica", 12, "bold"), bd=3)
  play_button.pack(pady=5)

  if not player.playlist:
    messagebox.showwarning("No Playlist", "No music files found! Please load a folder or add files.")
  else:
    update_playlist()

  def check_repeat():
    """Check if repeat is enabled and handle it."""
    if player.is_playing and player.repeat:
      player.handle_repeat()
    root.after(100, check_repeat)

  check_repeat()
