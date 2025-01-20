from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
import random
import os

def create_gui(root, player):
  """Create the GUI for the music player."""
  root.title("Desktop Music Player")
  root.geometry("420x640")

  title_label = tk.Label(root, text="Desktop Music Player", font=("Helvetica", 16, "bold"), pady=10)
  title_label.pack()

  playlist_frame = tk.Frame(root)
  playlist_frame.pack(pady=5)

  track_listbox = tk.Listbox(playlist_frame, width=53, height=12, font=("Helvetica", 10))
  track_listbox.grid(row=0, column=0)

  scrollbar = tk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=track_listbox.yview)
  scrollbar.grid(row=0, column=1, sticky="ns")
  track_listbox.config(yscrollcommand=scrollbar.set)

  def update_playlist():
    """Update the playlist display in the GUI."""
    track_listbox.delete(0, tk.END)
    for index, track in enumerate(player.playlist):
      try:
        audio = MP3(track)
        duration = int(audio.info.length)
        mins, secs = divmod(duration, 60)
        duration_str = f"{mins}:{secs:02d}"
      except:
        duration_str = "Unknown"
      track_name = os.path.basename(track)
      display_name = f"> {track_name} ({duration_str})" if index == player.current_track_index else f"{track_name} ({duration_str})"
      track_listbox.insert(tk.END, display_name)
    highlight_current_track()

  def highlight_current_track():
    """Highlight the currently playing track in the playlist."""
    if player.is_playing and player.current_track_index is not None:
      track_listbox.select_clear(0, tk.END)
      track_listbox.select_set(player.current_track_index)
      track_listbox.see(player.current_track_index)

  def load_folder():
    """Prompt the user to load a folder of MP3 files into the playlist."""
    folder = filedialog.askdirectory()
    if folder:
      player.load_folder(folder)
      update_playlist()

  def add_file():
    """Allow the user to add an individual MP3 file to the playlist."""
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
    """Toggle the repeat mode for the music player."""
    player.toggle_repeat()
    update_repeat_button_style()

  def update_repeat_button_style():
    """Update the appearance of the repeat button based on repeat mode."""
    if player.repeat:
      repeat_button.config(bg="red", fg="white")
    else:
      repeat_button.config(bg="white", fg="black")

  def toggle_play():
    """Toggle between play and stop for the selected track."""
    selected_track_index = track_listbox.curselection()
    if not selected_track_index:
      messagebox.showwarning("No Track Selected", "Please select a track to play.")
      return
    track_index = selected_track_index[0]
    player.toggle_play(track_index)
    update_play_button_style()
    update_playlist()

  def update_play_button_style():
    """Update the appearance of the play button based on the playback state."""
    if player.is_playing:
      play_button.config(text="Stop", bg="red", fg="white")
    else:
      play_button.config(text="Play", bg="green", fg="white")

  def set_volume(value):
    """Set the volume of the player based on the slider value."""
    volume = float(value) / 100
    player.set_volume(volume)

  def shuffle_playlist():
    """Shuffle the order of the tracks in the playlist."""
    random.shuffle(player.playlist)
    player.current_track_index = None
    update_playlist()

  def handle_dragged_files(event):
    """Handle files dragged onto the application window."""
    dragged_paths = root.tk.splitlist(event.data)
    for path in dragged_paths:
      if os.path.isdir(path):
        player.load_folder(path)
      elif os.path.isfile(path) and path.endswith(".mp3"):
        player.add_file(path)
      else:
        messagebox.showwarning("Unsupported File", f"Cannot add: {os.path.basename(path)}")
    update_playlist()

  # Register drag-and-drop support for MP3 files and folders
  root.drop_target_register(DND_FILES)
  root.dnd_bind('<<Drop>>', handle_dragged_files)

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

  shuffle_button = tk.Button(root, text="Shuffle", command=shuffle_playlist, width=38, font=("Helvetica", 12, "bold"), bd=3)
  shuffle_button.pack(pady=5)

  repeat_button = tk.Button(root, text="Repeat", command=toggle_repeat, width=38, font=("Helvetica", 12, "bold"), bd=3)
  repeat_button.pack(pady=5)

  play_button = tk.Button(root, text="Play", command=toggle_play, bg="green", fg="white", width=38, font=("Helvetica", 12, "bold"), bd=3)
  play_button.pack(pady=5)

  status_bar = tk.Label(root, text="No track playing", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Helvetica", 10, "italic"))
  status_bar.pack(side=tk.BOTTOM, fill=tk.X)

  def update_status_bar():
    """Update the status bar with the current track information."""
    if player.is_playing and player.current_track_index is not None:
      current_track = os.path.basename(player.playlist[player.current_track_index])
      status_bar.config(text=f"Playing: {current_track}")
    else:
      status_bar.config(text="No track playing")
    root.after(1000, update_status_bar)

  update_status_bar()

  if not player.playlist:
    messagebox.showwarning("No Playlist", "No music files found! Please load a folder or add files.")
  else:
    update_playlist()

  def check_repeat():
    """Check if the repeat mode should be triggered during playback."""
    if player.is_playing and player.repeat:
      player.handle_repeat()
    root.after(100, check_repeat)

  check_repeat()
