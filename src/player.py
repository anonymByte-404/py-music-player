import json
import os
import pygame
from dataclasses import dataclass, field
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
  pygame.mixer.init()
  logging.info("Pygame mixer initialized successfully.")
except pygame.error as e:
  logging.critical(f"Error initializing pygame mixer: {e}")
  raise SystemExit("Failed to initialize pygame mixer")

@dataclass
class Player:
  PLAYLIST_FILE: str = "playlist.json"
  is_playing: bool = False
  playlist: list[str] = field(default_factory=list)
  repeat: bool = False
  current_track_index: int | None = None
  volume: float = 0.5

  def __post_init__(self):
    """Post-initialization to load the playlist and set the volume."""
    self.load_playlist()
    self.set_volume(self.volume)

  def load_playlist(self):
    """Load the playlist from a JSON file."""
    if os.path.exists(self.PLAYLIST_FILE):
      try:
        with open(self.PLAYLIST_FILE, 'r') as file:
          data = json.load(file)
          self.playlist = data.get("music_files", [])
          self.current_track_index = 0 if self.playlist else None
          logging.info("Playlist loaded successfully.")
      except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error loading playlist: {e}")
        self.playlist = []
    else:
      logging.warning("Playlist file not found; starting with an empty playlist.")
      self.save_playlist()

  def save_playlist(self):
    """Save the current playlist to a JSON file."""
    try:
      data = {"music_files": self.playlist}
      with open(self.PLAYLIST_FILE, 'w') as file:
        json.dump(data, file, indent=4)
      logging.info("Playlist saved successfully.")
    except IOError as e:
      logging.error(f"Error saving playlist: {e}")

  def load_folder(self, folder: str):
    """Load MP3 files from a folder into the playlist."""
    if not os.path.exists(folder):
      logging.error(f"The folder '{folder}' does not exist.")
      return
    try:
      self.playlist = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
      self.update_and_save_playlist()
      logging.info(f"Loaded {len(self.playlist)} tracks from folder '{folder}'.")
    except Exception as e:
      logging.error(f"Error loading folder: {e}")

  def add_file(self, file: str):
    """Add an MP3 file to the playlist."""
    if not file.endswith(".mp3"):
      logging.warning(f"File '{file}' is not an MP3 and will not be added.")
      return
    self.playlist.append(file)
    self.update_and_save_playlist()
    logging.info(f"Added file '{file}' to playlist.")

  def remove_track(self, track_index: int):
    """Remove a track from the playlist by its index."""
    if 0 <= track_index < len(self.playlist):
      removed = self.playlist.pop(track_index)
      self.update_and_save_playlist()
      logging.info(f"Removed track '{removed}' from playlist.")
    else:
      logging.error(f"Invalid track index: {track_index}. Cannot remove track.")

  def move_track(self, old_index: int, new_index: int):
    """Move a track to a new position in the playlist."""
    if not (0 <= old_index < len(self.playlist)) or not (0 <= new_index < len(self.playlist)):
      logging.error(f"Invalid indices for moving track: {old_index} -> {new_index}.")
      return
    track = self.playlist.pop(old_index)
    self.playlist.insert(new_index, track)
    self.update_and_save_playlist()
    logging.info(f"Moved track '{track}' from position {old_index} to {new_index}.")

  def update_and_save_playlist(self):
    """Update the playlist and save it to the file."""
    self.save_playlist()
    if self.current_track_index is not None and self.current_track_index >= len(self.playlist):
      self.current_track_index = len(self.playlist) - 1
    elif self.current_track_index is None and self.playlist:
      self.current_track_index = 0

  def toggle_play(self, track_index: int):
    """Start or stop music playback."""
    if self.is_playing:
      pygame.mixer.music.stop()
      self.is_playing = False
      logging.info("Playback stopped.")
    elif 0 <= track_index < len(self.playlist):
      self.play_music(track_index)
    else:
      logging.warning(f"Invalid track index: {track_index}. Cannot toggle playback.")

  def play_music(self, track_index: int):
    """Play the selected music track."""
    if track_index < 0 or track_index >= len(self.playlist):
      logging.error(f"Track index {track_index} is out of bounds.")
      return
    try:
      track_path = self.playlist[track_index]
      pygame.mixer.music.load(track_path)
      pygame.mixer.music.play()
      self.is_playing = True
      self.current_track_index = track_index
      logging.info(f"Now playing: {track_path}")
    except pygame.error as e:
      logging.error(f"Error playing music: {e}")
    except Exception as e:
      logging.error(f"Unexpected error: {e}")

  def toggle_repeat(self):
    """Toggle the repeat functionality on/off."""
    self.repeat = not self.repeat
    logging.info(f"Repeat mode {'enabled' if self.repeat else 'disabled'}.")

  def set_volume(self, volume: float):
    """Set the playback volume (0.0 to 1.0)."""
    self.volume = max(0.0, min(1.0, volume))
    pygame.mixer.music.set_volume(self.volume)
    logging.info(f"Volume set to {self.volume:.2f}.")

  def handle_music_end(self):
    """Handle music end event (auto-repeat or next track)."""
    if self.repeat and self.current_track_index is not None:
      # If repeat is enabled, play the same track again
      self.play_music(self.current_track_index)
    elif self.current_track_index + 1 < len(self.playlist):
      # If repeat is disabled and there is a next track, play it
      self.play_music(self.current_track_index + 1)
    else:
      # If no more tracks, stop the music and reset
      self.is_playing = False
      self.current_track_index = None
      logging.info("Playlist playback completed.")

  def event_loop(self):
    """Event loop to handle pygame events."""
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        # Handle music end event here
        if not pygame.mixer.music.get_busy():
          self.handle_music_end()
      time.sleep(0.1)  # Small delay to reduce CPU usage
