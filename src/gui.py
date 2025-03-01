import logging
import os
import random
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from mutagen.mp3 import MP3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("player.log"),  # Log to a file
        logging.StreamHandler()             # Log to the console
    ]
)

def create_gui(root, player):
    """Initialize the GUI for the Desktop Music Player."""
    try:
        configure_root_window(root)
        title_label = create_title_label(root)
        track_listbox, scrollbar = create_playlist_section(root, player)
        create_volume_controls(root, player)
        create_buttons(root, player, track_listbox)
        status_bar = create_status_bar(root, player)

        # Bind drag-and-drop functionality
        configure_drag_and_drop(root, player, track_listbox)

        # Update playlist and status bar periodically
        update_playlist_display(player, track_listbox)
        update_status_bar(player, status_bar, root)
        monitor_repeat_mode(player, root)

        root.protocol("WM_DELETE_WINDOW", lambda: handle_close(root))
    except Exception as e:
        logging.error(f"Failed to create GUI: {e}", exc_info=True)
        raise

def configure_root_window(root):
    """Configure the main application window."""
    root.title("Desktop Music Player")
    root.geometry("420x640")
    root.resizable(False, False)
    root.config(bg="#262323")

def create_title_label(root):
    """Create the title label for the application."""
    title_label = tk.Label(
        root,
        text="Desktop Music Player",
        font=("Helvetica", 16, "bold"),
        pady=10,
        bg="#262323",
        fg="#DFD7D7"
    )
    title_label.pack()
    return title_label

def create_playlist_section(root, player):
    """Create the playlist display area with scrollbar."""
    playlist_frame = tk.Frame(root, bg="#262323")
    playlist_frame.pack(pady=5)

    track_listbox = tk.Listbox(
        playlist_frame,
        width=53,
        height=12,
        font=("Helvetica", 10),
        bg="#262323",
        fg="#DFD7D7",
        selectbackground="#a7a7a7",
        selectforeground="#262323"
    )
    track_listbox.grid(row=0, column=0)

    scrollbar = tk.Scrollbar(
        playlist_frame,
        orient=tk.VERTICAL,
        command=track_listbox.yview,
        bg="#423F3F"
    )
    scrollbar.grid(row=0, column=1, sticky="ns")
    track_listbox.config(yscrollcommand=scrollbar.set)

    return track_listbox, scrollbar

def create_volume_controls(root, player):
    """Create the volume slider controls."""
    volume_label = tk.Label(
        root,
        text="Volume",
        font=("Helvetica", 12, "bold"),
        bg="#262323",
        fg="#DFD7D7"
    )
    volume_label.pack(pady=(5, 0))

    volume_slider = tk.Scale(
        root,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        command=lambda value: set_volume(player, value),
        length=350,
        bg="#262323",
        fg="#DFD7D7",
        sliderlength=20
    )
    volume_slider.set(50)
    volume_slider.pack(pady=(0, 5), padx=5)

def create_buttons(root, player, track_listbox):
    """Create the control buttons."""
    button_frame_1 = tk.Frame(root, bg="#262323")
    button_frame_1.pack(pady=5)

    tk.Button(
        button_frame_1,
        text="Load Folder",
        command=lambda: load_folder(player, track_listbox),
        width=18,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame_1,
        text="Add File",
        command=lambda: add_file(player, track_listbox),
        width=18,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        root,
        text="Remove Track",
        command=lambda: remove_selected_track(player, track_listbox),
        width=38,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    ).pack(pady=5)

    button_frame_2 = tk.Frame(root, bg="#262323")
    button_frame_2.pack(pady=5)

    tk.Button(
        button_frame_2,
        text="Move Up",
        command=lambda: move_track(player, track_listbox, up=True),
        width=18,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame_2,
        text="Move Down",
        command=lambda: move_track(player, track_listbox, up=False),
        width=18,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        root,
        text="Shuffle",
        command=lambda: shuffle_playlist(player, track_listbox),
        width=38,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    ).pack(pady=5)

    repeat_button = tk.Button(
        root,
        text="Repeat",
        command=lambda: toggle_repeat(player, repeat_button),
        width=38,
        font=("Helvetica", 12, "bold"),
        bd=3,
        bg="#262323",
        fg="#DFD7D7"
    )
    repeat_button.pack(pady=5)

    play_button = tk.Button(
        root,
        text="Play",
        command=lambda: toggle_play(player, track_listbox, play_button),
        bg="green",
        fg="white",
        width=38,
        font=("Helvetica", 12, "bold"),
        bd=3
    )
    play_button.pack(pady=5)

def create_status_bar(root, player):
    """Create the status bar to display current track info."""
    status_bar = tk.Label(
        root,
        text="No track playing",
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W,
        font=("Helvetica", 10, "italic"),
        bg="#262323",
        fg="#DFD7D7"
    )
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    return status_bar

def configure_drag_and_drop(root, player, track_listbox):
    """Configure drag-and-drop functionality for the application."""
    def handle_dragged_files(event):
        paths = root.tk.splitlist(event.data)
        for path in paths:
            if os.path.isdir(path):
                player.load_folder(path)
            elif os.path.isfile(path) and path.endswith(".mp3"):
                player.add_file(path)
            else:
                messagebox.showwarning("Unsupported File", f"Cannot add: {os.path.basename(path)}")
        update_playlist_display(player, track_listbox)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", handle_dragged_files)

def load_folder(player, track_listbox):
    """Load all tracks from a folder into the playlist."""
    folder = filedialog.askdirectory()
    if folder:
        try:
            player.load_folder(folder)
            update_playlist_display(player, track_listbox)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load folder: {e}")

def add_file(player, track_listbox):
    """Add a single file to the playlist."""
    file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file:
        try:
            player.add_file(file)
            update_playlist_display(player, track_listbox)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add file: {e}")

def remove_selected_track(player, track_listbox):
    """Remove the selected track from the playlist."""
    selected = track_listbox.curselection()
    if not selected:
        messagebox.showwarning("No Track Selected", "Please select a track to remove.")
        return
    try:
        player.remove_track(selected[0])
        update_playlist_display(player, track_listbox)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove track: {e}")

def move_track(player, track_listbox, up):
    """Move a selected track up or down in the playlist."""
    selected = track_listbox.curselection()
    if not selected:
        messagebox.showwarning("No Track Selected", "Please select a track to move.")
        return
    index = selected[0]
    new_index = index - 1 if up else index + 1
    if 0 <= new_index < len(player.playlist):
        try:
            player.move_track(index, new_index)
            update_playlist_display(player, track_listbox)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move track: {e}")

def shuffle_playlist(player, track_listbox):
    """Shuffle the current playlist."""
    try:
        logging.info("Shuffling playlist")
        random.shuffle(player.playlist)
        update_playlist_display(player, track_listbox)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to shuffle playlist: {e}")

def toggle_repeat(player, button):
    """Toggle the repeat mode for the player."""
    player.toggle_repeat()
    button.config(bg="red" if player.repeat else "#262323", fg="white" if player.repeat else "#DFD7D7")

def toggle_play(player, track_listbox, button):
    """Play or stop the currently selected track."""
    selected = track_listbox.curselection()
    if not selected:
        messagebox.showwarning("No Track Selected", "Please select a track to play.")
        return
    index = selected[0]
    try:
        player.toggle_play(index)
        button.config(text="Stop" if player.is_playing else "Play", bg="red" if player.is_playing else "green", fg="white")
        update_playlist_display(player, track_listbox)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to toggle play: {e}")

def set_volume(player, value):
    """Set the volume level of the player."""
    try:
        player.set_volume(float(value) / 100)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set volume: {e}")

def update_playlist_display(player, track_listbox):
    """Update the playlist display to reflect the current state."""
    track_listbox.delete(0, tk.END)
    for index, track in enumerate(player.playlist):
        try:
            audio = MP3(track)
            duration = int(audio.info.length)
            mins, secs = divmod(duration, 60)
            duration_str = f"{mins}:{secs:02d}"
        except Exception as e:
            logging.error(f"Error reading track duration: {e}")
            duration_str = "Unknown"
        track_name = os.path.basename(track)
        display_name = f"> {track_name} ({duration_str})" if index == player.current_track_index else f"{track_name} ({duration_str})"
        track_listbox.insert(tk.END, display_name)
    highlight_current_track(player, track_listbox)

def highlight_current_track(player, track_listbox):
    """Highlight the currently playing track in the playlist."""
    if player.is_playing and player.current_track_index is not None:
        track_listbox.select_clear(0, tk.END)
        track_listbox.select_set(player.current_track_index)
        track_listbox.see(player.current_track_index)

def update_status_bar(player, status_bar, root):
    """Update the status bar to display the current track or status."""
    if player.is_playing and player.current_track_index is not None:
        current_track = os.path.basename(player.playlist[player.current_track_index])
        status_bar.config(text=f"Playing: {current_track}")
    else:
        status_bar.config(text="No track playing")
    root.after(1000, lambda: update_status_bar(player, status_bar, root))

def monitor_repeat_mode(player, root):
    """Monitor and handle the repeat mode functionality."""
    if player.is_playing and player.repeat:
        player.handle_repeat()
    root.after(100, lambda: monitor_repeat_mode(player, root))

def handle_close(root):
    """Handle the application window close event."""
    logging.info("Application closed.")
    root.destroy()