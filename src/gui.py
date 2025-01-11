import tkinter as tk
from tkinter import filedialog, messagebox
import os

def create_gui(root, player):
    """Create the GUI for the music player"""
    root.title("Desktop Music Player")
    root.geometry("400x300")

    # Playlist Listbox
    track_listbox = tk.Listbox(root, width=40, height=10)
    track_listbox.pack(pady=10)

    # Check if playlist is empty
    if not player.playlist:
        messagebox.showwarning("No Playlist", "No music files found! Please load a folder or add files.")
    
    for track in player.playlist:
        track_listbox.insert(tk.END, os.path.basename(track))

    # Load folder button
    def load_folder():
        folder = filedialog.askdirectory()
        if folder:
            player.load_folder(folder)
            track_listbox.delete(0, tk.END)
            for track in player.playlist:
                track_listbox.insert(tk.END, os.path.basename(track))

    load_button = tk.Button(root, text="Load Folder", command=load_folder)
    load_button.pack(pady=5)

    # Add file button
    def add_file():
        file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file:
            player.add_file(file)
            track_listbox.insert(tk.END, os.path.basename(file))

    add_button = tk.Button(root, text="Add File", command=add_file)
    add_button.pack(pady=5)

    # Play/Stop button
    def toggle_play():
        player.toggle_play()
        if player.is_playing:
            play_button.config(text="Stop")
        else:
            play_button.config(text="Play")

    play_button = tk.Button(root, text="Play", command=toggle_play)
    play_button.pack(pady=5)
