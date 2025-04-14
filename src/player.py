import json
import os
import pygame
from dataclasses import dataclass, field
import logging
import time
from typing import Optional
import random

# Configure logging
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  handlers=[
    logging.FileHandler("player.log"),
    logging.StreamHandler()
  ]
)

# Initialize pygame mixer
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
  current_track_index: Optional[int] = None
  volume: float = 0.5

  def __post_init__(self) -> None:
    """Load playlist and set volume."""
    self.load_playlist()
    self.set_volume(self.volume)

  def load_playlist(self) -> None:
    """Load playlist from file."""
    if os.path.exists(self.PLAYLIST_FILE):
      try:
        with open(self.PLAYLIST_FILE, "r") as file:
          data: dict[str, list[str]] = json.load(file)
          self.playlist = data.get("music_files", [])
          self.current_track_index = 0 if self.playlist else None
          logging.info("Playlist loaded successfully.")
      except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error loading playlist: {e}")
        self.playlist = []
    else:
      logging.warning("Playlist file not found; starting with empty playlist.")
      self.save_playlist()

  def save_playlist(self) -> None:
    """Save playlist to file."""
    try:
      data: dict[str, list[str]] = {"music_files": self.playlist}
      with open(self.PLAYLIST_FILE, "w") as file:
        json.dump(data, file, indent=4)
      logging.info("Playlist saved successfully.")
    except IOError as e:
      logging.error(f"Error saving playlist: {e}")

  def load_folder(self, folder: str) -> None:
    """Load MP3 files from folder."""
    if not os.path.exists(folder):
      logging.error(f"The folder '{folder}' does not exist.")
      return
    try:
      new_tracks: list[str] = [
        os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")
      ]
      if new_tracks:
        self.playlist.extend(new_tracks)
        self.update_and_save_playlist()
        logging.info(f"Loaded {len(new_tracks)} tracks from '{folder}'.")
      else:
        logging.warning(f"No MP3 files found in '{folder}'.")
    except Exception as e:
      logging.error(f"Error loading folder: {e}")

  def add_file(self, file: str) -> None:
    """Add MP3 file to playlist."""
    if file.endswith(".mp3"):
      self.playlist.append(file)
      self.update_and_save_playlist()
      logging.info(f"Added file '{file}' to playlist.")
    else:
      logging.warning(f"File '{file}' is not an MP3.")

  def remove_track(self, track_index: int) -> None:
    """Remove track by index."""
    if 0 <= track_index < len(self.playlist):
      removed: str = self.playlist.pop(track_index)
      self.update_and_save_playlist()
      logging.info(f"Removed track '{removed}'.")
    else:
      logging.error(f"Invalid index: {track_index}.")

  def move_track(self, old_index: int, new_index: int) -> None:
    """Move track to new index."""
    if 0 <= old_index < len(self.playlist) and 0 <= new_index < len(self.playlist):
      track: str = self.playlist.pop(old_index)
      self.playlist.insert(new_index, track)
      self.update_and_save_playlist()
      logging.info(f"Moved track '{track}' from {old_index} to {new_index}.")
    else:
      logging.error(f"Invalid indices: {old_index} -> {new_index}.")

  def update_and_save_playlist(self) -> None:
    """Update and save playlist."""
    self.save_playlist()
    self._update_current_track_index()

  def _update_current_track_index(self) -> None:
    """Update current track index."""
    if self.current_track_index is not None and self.current_track_index >= len(self.playlist):
      self.current_track_index = len(self.playlist) - 1
    elif self.current_track_index is None and self.playlist:
      self.current_track_index = 0

  def toggle_play(self, track_index: int) -> None:
    """Toggle music playback."""
    if self.is_playing:
      pygame.mixer.music.stop()
      self.is_playing = False
      logging.info("Playback stopped.")
    elif 0 <= track_index < len(self.playlist):
      self.play_music(track_index)
    else:
      logging.warning(f"Invalid index: {track_index}.")

  def play_music(self, track_index: int) -> None:
    """Play track by index."""
    if track_index < 0 or track_index >= len(self.playlist):
      logging.error(f"Index {track_index} out of bounds.")
      return
    try:
      track_path: str = self.playlist[track_index]
      pygame.mixer.music.load(track_path)
      pygame.mixer.music.play()
      self.is_playing = True
      self.current_track_index = track_index
      logging.info(f"Now playing: {track_path}")
    except pygame.error as e:
      logging.error(f"Pygame error: {e}")
    except Exception as e:
      logging.error(f"Unexpected error: {e}")

  def toggle_repeat(self) -> None:
    """Toggle repeat mode."""
    self.repeat = not self.repeat
    logging.info(f"Repeat {'enabled' if self.repeat else 'disabled'}.")

  def set_volume(self, volume: float) -> None:
    """Set volume (0.0 to 1.0)."""
    self.volume = max(0.0, min(1.0, volume))
    pygame.mixer.music.set_volume(self.volume)
    logging.info(f"Volume set to {self.volume:.2f}.")

  def stop(self) -> None:
    """Stop music playback."""
    if self.is_playing:
      pygame.mixer.music.stop()
      self.is_playing = False
      self.current_track_index = None
      logging.info("Music stopped.")

  def shuffle_playlist(self) -> None:
    """Shuffle the playlist."""
    random.shuffle(self.playlist)
    self.update_and_save_playlist()
    logging.info("Playlist shuffled.")

  def handle_music_end(self) -> None:
    """Handle music end."""
    if self.repeat and self.current_track_index is not None:
      self.play_music(self.current_track_index)
    elif self.current_track_index is not None and self.current_track_index + 1 < len(self.playlist):
      self.play_music(self.current_track_index + 1)
    else:
      self.is_playing = False
      self.current_track_index = None
      logging.info("Playlist completed.")

  def event_loop(self) -> None:
    """Handle pygame events."""
    running: bool = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if not pygame.mixer.music.get_busy():
          self.handle_music_end()
      time.sleep(0.1)
