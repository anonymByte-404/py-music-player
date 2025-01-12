import pygame
import json
import os

# Initialize the pygame mixer for audio playback
pygame.mixer.init()

class Player:
    def __init__(self):
        self.is_playing = False
        self.playlist = self.load_playlist()  # Load playlist from JSON
        self.last_folder = self.load_last_folder()  # Load last folder from JSON

    def load_playlist(self):
        """Load the list of MP3 files from playlist.json"""
        try:
            with open('playlist.json', 'r') as file:
                data = json.load(file)
                # Ensure there is a valid 'music_files' list, default to empty if not
                return data.get("music_files", [])
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file is missing or corrupted, initialize a default playlist
            return []

    def load_last_folder(self):
        """Load the last opened folder from playlist.json"""
        try:
            with open('playlist.json', 'r') as file:
                data = json.load(file)
                return data.get("last_folder", "")
        except (FileNotFoundError, json.JSONDecodeError):
            return ""

    def save_playlist(self):
        """Save the current playlist to playlist.json"""
        data = {
            "music_files": self.playlist,
            "last_folder": self.last_folder
        }
        with open('playlist.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_folder(self, folder):
        """Load all MP3 files from a selected folder"""
        self.last_folder = folder
        self.playlist = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
        self.save_playlist()

    def add_file(self, file):
        """Add a single MP3 file to the playlist"""
        self.playlist.append(file)
        self.save_playlist()

    def toggle_play(self):
        """Start/stop playing the music"""
        if self.is_playing:
            pygame.mixer.music.stop()
        else:
            if self.playlist:
                pygame.mixer.music.load(self.playlist[0])  # Load the first track
                pygame.mixer.music.play()
        self.is_playing = not self.is_playing
