"""
A simple music player application using Pygame.
"""

import pygame
import os
from collections import deque
from rainbow import colors
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:
    """
    A class representing a music player.
    """

    def __init__(self):
        """
        Initializes the MusicPlayer object.
        """
        pygame.init()
        pygame.mixer.init()
        self.queue = deque()
        self.current_song = None
        self.paused = False

    def enqueue(self, song):
        """
        Adds a song to the queue.
        """
        self.queue.append(song)

    def skip(self):
        """
        Skips the current song and plays the next song in the queue.
        """
        if self.queue:
            pygame.mixer.music.stop()
            self.queue.popleft()
            self.play()
        else:
            self.current_song = None

    def play(self):
        """
        Plays the next song in the queue.
        """
        if self.queue and not pygame.mixer.music.get_busy():
            if self.current_song:
                pygame.mixer.music.stop()
            song = self.queue[0]
            self.current_song = song
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()

    def pause(self):
        """
        Pauses or resumes the currently playing song.
        """
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True


def draw_button_and_center_text(x, y, width, height, color, text, text_color):
    """
    Draws a button with centered text.
    """
    button = pygame.draw.rect(win, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2-2)
    win.blit(text_surface, text_rect)
    return button


def draw_song_list(selected, queue):
    """
    Draws the list of songs and songs in queue if any.
    """
    y = 32
    songs = 0
    queued = 0
    song_choice = os.path.basename(selected) if selected else None
    draw_button_and_center_text((WIDTH // 4) - 80, 7, 200, 25, BLUE, 'Song List:', WHITE)
    for song_path in music_files:
        songs += 1
        song_name = os.path.basename(song_path)
        if song_choice == song_name:
            draw_button_and_center_text(WIDTH // 4 - 80, y, 200, 30, BLUE, song_name, WHITE)
        else:
            draw_button_and_center_text(WIDTH // 4 - 80, y, 200, 30, GRAY, song_name, BLACK)
        y += 25
        if songs == 10:
            break
        
    y2 = 32
    draw_button_and_center_text((WIDTH // 4) * 3 - 100, 7, 200, 25, BLUE, 'Queued Songs:', WHITE)
    for i, song_path in enumerate(queue):
        queued += 1
        song_name = os.path.basename(song_path)
        if i == 0:
            draw_button_and_center_text((WIDTH // 4) * 3 - 100, y2, 200, 30, WHITE, song_name, GREEN)
        else:
            draw_button_and_center_text((WIDTH // 4) * 3 - 100, y2, 200, 30, WHITE, song_name, RED)
        y2 += 25
        if queued == 10:
            break
        


# Pygame setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)

# Window dimensions
WIDTH, HEIGHT = 500, 400

# Fonts
font = pygame.font.SysFont('Arial', 18)

# Create a Tkinter window to prompt the user for the music folder
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select the music folder
music_folder = filedialog.askdirectory(title="Select Music Folder")

# Create the window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# Check if music folder is selected
if music_folder:
    music_player = MusicPlayer()
    music_extensions = ('.mp3', '.wav', '.mwa', '.m4a', '.aac')
    music_files = [os.path.join(music_folder, filename)
                   for filename in os.listdir(music_folder)
                   if filename.endswith(music_extensions)]

    selected_song = None
    playing = True

    button_width = 50
    r = 255
    g = 0
    b = 0

    while playing and music_files:
        win.fill(WHITE)
        draw_song_list(selected_song, music_player.queue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music_player.pause()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                if play_button.collidepoint(mouse_pos):
                    music_player.play()
                if pause_button.collidepoint(mouse_pos):
                    music_player.pause()
                if skip_button.collidepoint(mouse_pos):
                    music_player.skip()
                if add_to_queue_button.collidepoint(mouse_pos):
                    music_player.enqueue(selected_song)

                if  WIDTH // 4 - 80 <= event.pos[0] <= (WIDTH // 4 - 80) + 200:
                    for i, song_path in enumerate(music_files):
                        if 32 + i * 25 <= event.pos[1] <= 62 + i * 25:
                            if selected_song == song_path:
                                selected_song = None
                            else:
                                selected_song = song_path

        if not pygame.mixer.music.get_busy() and music_player.current_song and not music_player.paused:
            music_player.skip()

        # buttons
        play_button = draw_button_and_center_text(70, 300, button_width, 30, BLUE, 'Play', WHITE)
        pause_button = draw_button_and_center_text(70 + (button_width * 2), 300, button_width, 30, RED, 'Pause', WHITE)
        skip_button = draw_button_and_center_text(70 + (button_width * 4) + 10, 300, button_width, 30, GREEN, 'Skip', WHITE)
        add_to_queue_button = draw_button_and_center_text(70 + (button_width * 6) + 10, 300, button_width, 30, YELLOW, 'Add', WHITE)

        if music_player.current_song:
            now_playing = f'Now Playing: {os.path.basename(music_player.current_song)}'
            now_playing_button = draw_button_and_center_text(100, 350, 300, 32, GRAY, now_playing, colors(r,g,b))

        r, g, b = colors(r, g, b)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
else:
    print("No music folder selected.")
