import json
import os
import pygame

# Initialize the pygame mixer for audio playback
pygame.mixer.init()

class Player:
    def __init__(self):
        self.is_playing = False
        self.playlist = []  # List of songs
        self.repeat = False  # Repeat functionality
        self.current_track_index = None  # Index of the current track
        self.load_playlist()  # Load the playlist when the player is initialized

    def load_playlist(self):
        """Load the playlist from a JSON file"""
        if os.path.exists('playlist.json'):
            with open('playlist.json', 'r') as file:
                data = json.load(file)
                self.playlist = data.get("music_files", [])
                if self.playlist:
                    self.current_track_index = 0  # Start with the first track

    def save_playlist(self):
        """Save the playlist to a JSON file"""
        data = {
            "music_files": self.playlist
        }
        with open('playlist.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_folder(self, folder):
        """Load all MP3 files from a selected folder"""
        self.playlist = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
        self.save_playlist()  # Save playlist after loading folder
        if self.playlist:
            self.current_track_index = 0  # Start with the first track

    def add_file(self, file):
        """Add a single MP3 file to the playlist"""
        self.playlist.append(file)
        self.save_playlist()  # Save playlist after adding a file
        if self.current_track_index is None:
            self.current_track_index = 0  # If no track is playing, start from the first track

    def toggle_play(self, track_index):
        """Start/stop playing the music"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
        else:
            self.current_track_index = track_index
            self.play_music(track_index)

    def play_music(self, track_index):
        """Play the music track"""
        if self.playlist:
            pygame.mixer.music.load(self.playlist[track_index])
            pygame.mixer.music.play()
            self.is_playing = True
            self.current_track_index = track_index

            # Set up a callback to check when the song ends
            pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def handle_repeat(self):
        """Handle repeat functionality"""
        if self.is_playing and self.repeat:
            # Check if the current track has finished playing, if yes, reload and replay the track
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.playlist[self.current_track_index])
                pygame.mixer.music.play()

    def toggle_repeat(self):
        """Toggle repeat functionality"""
        self.repeat = not self.repeat
