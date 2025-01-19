import json
import os
import pygame

# Initialize the pygame mixer for audio playback
try:
  pygame.mixer.init()
except pygame.error as e:
  print(f"Error initializing pygame mixer: {e}")
  raise SystemExit("Failed to initialize pygame mixer")


class Player:
  """Manage the functionality of the music player."""

  PLAYLIST_FILE = "playlist.json"

  def __init__(self):
    """Initialize the player and load the playlist."""
    self.is_playing = False
    self.playlist = []
    self.repeat = False
    self.current_track_index = None
    self.volume = 0.5  # Default volume: 50%
    self.load_playlist()
    pygame.mixer.music.set_volume(self.volume)

  def load_playlist(self):
    """Load the playlist from a JSON file."""
    try:
      if os.path.exists(self.PLAYLIST_FILE):
        with open(self.PLAYLIST_FILE, 'r') as file:
          data = json.load(file)
          self.playlist = data.get("music_files", [])
          if self.playlist:
            self.current_track_index = 0  # Start with the first track
    except (IOError, json.JSONDecodeError) as e:
      print(f"Error loading playlist: {e}")
      self.playlist = []

  def save_playlist(self):
    """Save the playlist to a JSON file."""
    try:
      data = {"music_files": self.playlist}
      with open(self.PLAYLIST_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    except IOError as e:
      print(f"Error saving playlist: {e}")

  def load_folder(self, folder):
    """Load MP3 files from a folder into the playlist."""
    try:
      self.playlist = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
      self.update_and_save_playlist()
    except FileNotFoundError:
      print(f"The folder {folder} does not exist.")
    except Exception as e:
      print(f"Error loading folder: {e}")

  def add_file(self, file):
    """Add an MP3 file to the playlist."""
    try:
      if file.endswith(".mp3"):
        self.playlist.append(file)
        self.update_and_save_playlist()
    except Exception as e:
      print(f"Error adding file: {e}")

  def remove_track(self, track_index):
    """Remove a track from the playlist."""
    try:
      if 0 <= track_index < len(self.playlist):
        self.playlist.pop(track_index)
        self.update_and_save_playlist()
    except Exception as e:
      print(f"Error removing track: {e}")

  def move_track(self, old_index, new_index):
    """Move a track to a new position in the playlist."""
    try:
      if 0 <= old_index < len(self.playlist) and 0 <= new_index < len(self.playlist):
        track = self.playlist.pop(old_index)
        self.playlist.insert(new_index, track)
        self.update_and_save_playlist()
    except Exception as e:
      print(f"Error moving track: {e}")

  def update_and_save_playlist(self):
    """Update the playlist and save it."""
    self.save_playlist()
    if self.current_track_index is None:
      self.current_track_index = 0  # If no track is playing, start from the first track

  def toggle_play(self, track_index):
    """Start or stop the music playback."""
    if self.is_playing:
      pygame.mixer.music.stop()
      self.is_playing = False
    else:
      self.current_track_index = track_index
      self.play_music(track_index)

  def play_music(self, track_index):
    """Play the selected music track."""
    if self.playlist:
      try:
        track_path = self.playlist[track_index]
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True
        self.current_track_index = track_index
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        print(f"Playing track: {track_path}")
      except pygame.error as e:
        print(f"Error playing music: {e}")

  def handle_repeat(self):
    """Handle the repeat functionality for the music."""
    if self.is_playing and self.repeat:
      if not pygame.mixer.music.get_busy():
        self.play_music(self.current_track_index)

  def toggle_repeat(self):
    """Toggle the repeat functionality on/off."""
    self.repeat = not self.repeat

  def set_volume(self, volume):
    """Set the playback volume (0.0 to 1.0)."""
    self.volume = max(0.0, min(1.0, volume))  # Clamp volume between 0.0 and 1.0
    pygame.mixer.music.set_volume(self.volume)
