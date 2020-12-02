import os

# Don't print the support info to stdout upon startup
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


pygame.mixer.init()


def handle_authorized_event(event):
    pygame.mixer.music.load('/magicband-reader/test.wav')
    pygame.mixer.music.play()


def handle_unauthorized_event(event):
    pass
