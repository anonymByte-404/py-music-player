import tkinter as tk
from tkinter import filedialog, messagebox
import os
from player import Player

def create_gui(root, player):
    """Create the GUI for the music player"""
    root.title("Desktop Music Player")
    root.geometry("400x350")

    # Playlist Listbox
    track_listbox = tk.Listbox(root, width=40, height=10)
    track_listbox.pack(pady=10)

    # Display initial playlist or show a warning if empty
    if not player.playlist:
        messagebox.showwarning("No Playlist", "No music files found! Please load a folder or add files.")
    else:
        for track in player.playlist:
            track_listbox.insert(tk.END, os.path.basename(track))
        track_listbox.select_set(0)  # Select the first item

    # Load folder button
    def load_folder():
        folder = filedialog.askdirectory()
        if folder:
            player.load_folder(folder)
            track_listbox.delete(0, tk.END)  # Clear existing playlist display
            for track in player.playlist:
                track_listbox.insert(tk.END, os.path.basename(track))
            track_listbox.select_set(0)  # Select the first item

    load_button = tk.Button(root, text="Load Folder", command=load_folder, width=15)
    load_button.pack(pady=5)

    # Add file button
    def add_file():
        file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file:
            player.add_file(file)
            track_listbox.insert(tk.END, os.path.basename(file))
            track_listbox.select_set(0)  # Select the first item

    add_button = tk.Button(root, text="Add File", command=add_file, width=15)
    add_button.pack(pady=5)

    # Repeat button
    def toggle_repeat():
        player.toggle_repeat()
        if player.repeat:
            repeat_button.config(bg="red", fg="white")
        else:
            repeat_button.config(bg="white", fg="black")

    repeat_button = tk.Button(root, text="Repeat", command=toggle_repeat, width=15)
    repeat_button.pack(pady=5)

    # Play/Stop button
    def toggle_play():
        selected_track_index = track_listbox.curselection()
        track_index = selected_track_index[0] if selected_track_index else 0
        player.toggle_play(track_index)
        if player.is_playing:
            play_button.config(text="Stop", bg="red", fg="white")
        else:
            play_button.config(text="Play", bg="green", fg="white")

    play_button = tk.Button(root, text="Play", command=toggle_play, bg="green", fg="white", width=15)
    play_button.pack(pady=5)

    # Update playlist display
    def update_playlist():
        track_listbox.delete(0, tk.END)
        for track in player.playlist:
            track_listbox.insert(tk.END, os.path.basename(track))
        track_listbox.select_set(0)  # Select the first item

    update_playlist()

    # Periodic check for repeating songs
    def check_repeat():
        if player.is_playing and player.repeat:
            player.handle_repeat()
        root.after(100, check_repeat)  # Check every 100ms

    check_repeat()
