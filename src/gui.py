import tkinter as tk
from tkinter import filedialog, messagebox
import os
from player import Player

"""
Desktop Music Player - GUI

This file defines the graphical user interface (GUI) for a simple desktop music player using Tkinter.
It allows users to:
- Load MP3 files from a folder or add individual MP3 files to the playlist.
- Play, stop, and toggle repeat functionality for music tracks.
- Display the playlist in a listbox and update it dynamically.

The GUI includes buttons for loading files, adding songs, controlling playback, and enabling repeat.
"""

def create_gui(root, player):
  """Create the GUI for the music player"""
  root.title("Desktop Music Player")
  root.geometry("400x380")

  # Playlist Listbox
  track_listbox = tk.Listbox(root, width=40, height=10)
  track_listbox.pack(pady=10)

  # Display initial playlist or show a warning if empty
  if not player.playlist:
    messagebox.showwarning("No Playlist", "No music files found! Please load a folder or add files.")
  else:
    for track in player.playlist:
      track_listbox.insert(tk.END, os.path.basename(track))

    # Highlight the first song
    track_listbox.select_set(0)  # Select the first item

  def load_folder():
    folder = filedialog.askdirectory()
    if folder:
      player.load_folder(folder)
      track_listbox.delete(0, tk.END)  # Clear existing playlist display
      for track in player.playlist:
        track_listbox.insert(tk.END, os.path.basename(track))

      # Highlight the first song after loading new folder
      track_listbox.select_set(0)  # Select the first item

  load_button = tk.Button(root, text="Load Folder", command=load_folder, width=15, font=("Helvetica", 12, "bold"), bd=3)
  load_button.pack(pady=5)

  def add_file():
    file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file:
      player.add_file(file)
      track_listbox.insert(tk.END, os.path.basename(file))

      # Highlight the newly added song if it is the first one
      track_listbox.select_set(0)  # Select the first item

  add_button = tk.Button(root, text="Add File", command=add_file, width=15, font=("Helvetica", 12, "bold"), bd=3)
  add_button.pack(pady=5)

  def toggle_repeat():
    player.toggle_repeat()
    if player.repeat:
      repeat_button.config(bg="red", fg="white")
    else:
      repeat_button.config(bg="white", fg="black")

  repeat_button = tk.Button(root, text="Repeat", command=toggle_repeat, width=15, font=("Helvetica", 12, "bold"), bd=3)
  repeat_button.pack(pady=5)

  def toggle_play():
    selected_track_index = track_listbox.curselection()
    track_index = selected_track_index[0] if selected_track_index else 0
    player.toggle_play(track_index)
    if player.is_playing:
      play_button.config(text="Stop", bg="red", fg="white")
    else:
      play_button.config(text="Play", bg="green", fg="white")

  play_button = tk.Button(root, text="Play", command=toggle_play, bg="green", fg="white", width=15, font=("Helvetica", 12, "bold"), bd=3)
  play_button.pack(pady=5)

  def update_playlist():
    track_listbox.delete(0, tk.END)
    for track in player.playlist:
      track_listbox.insert(tk.END, os.path.basename(track))

    # Highlight the first song after playlist is updated
    track_listbox.select_set(0)  # Select the first item

  update_playlist()

  def check_repeat():
    if player.is_playing and player.repeat:
      player.handle_repeat()
    root.after(100, check_repeat)  # Check every 100ms

  check_repeat()
