import tkinter as tk
from tkinter import filedialog, messagebox
import os

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

        # Highlight the first song
        track_listbox.select_set(0)  # Select the first item

    # Load folder button
    def load_folder():
        folder = filedialog.askdirectory()
        if folder:
            player.load_folder(folder)
            track_listbox.delete(0, tk.END)  # Clear existing playlist display
            for track in player.playlist:
                track_listbox.insert(tk.END, os.path.basename(track))

            # Highlight the first song after loading new folder
            track_listbox.select_set(0)  # Select the first item

    load_button = tk.Button(root, text="Load Folder", command=load_folder, width=15)
    load_button.pack(pady=5)

    # Add file button
    def add_file():
        file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file:
            player.add_file(file)
            track_listbox.insert(tk.END, os.path.basename(file))

            # Highlight the newly added song if it is the first one
            track_listbox.select_set(0)  # Select the first item

    add_button = tk.Button(root, text="Add File", command=add_file, width=15)
    add_button.pack(pady=5)

    # Remove file button
    def remove_file():
        selected = track_listbox.curselection()
        if selected:
            track_to_remove = track_listbox.get(selected[0])  # Get the file name
            track_to_remove_path = None

            # Find the file path of the selected song
            for track in player.playlist:
                if os.path.basename(track) == track_to_remove:
                    track_to_remove_path = track
                    break

            if track_to_remove_path:
                player.playlist.remove(track_to_remove_path)  # Remove from playlist
                player.save_playlist()  # Save the updated playlist
                track_listbox.delete(selected)  # Remove from listbox
            else:
                messagebox.showerror("Error", "Could not find the selected song.")
        else:
            messagebox.showwarning("No Selection", "Please select a song to remove.")

    remove_button = tk.Button(root, text="Remove", command=remove_file, width=15)
    remove_button.pack(pady=5)

    # Play/Stop button
    def toggle_play():
        player.toggle_play()
        if player.is_playing:
            # Change button color to red when playing
            play_button.config(text="Stop", bg="red", fg="white")
        else:
            # Change button color to green when stopped
            play_button.config(text="Play", bg="green", fg="white")

    # Initially set the Play button color to green and white text
    play_button = tk.Button(root, text="Play", command=toggle_play, bg="green", fg="white", width=15)
    play_button.pack(pady=5)

    # Update GUI to show the initial state of the player
    def update_playlist():
        track_listbox.delete(0, tk.END)
        for track in player.playlist:
            track_listbox.insert(tk.END, os.path.basename(track))

        # Highlight the first song after playlist is updated
        track_listbox.select_set(0)  # Select the first item

    update_playlist()
