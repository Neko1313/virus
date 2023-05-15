import pygame
from pygame import mixer
from pynput import mouse
import threading
import os

def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        play_sound(os.path.dirname(os.path.realpath("__file__"))+"\media\\click.wav")

def play_music():
    mixer.init()
    mixer.music.load(os.path.dirname(os.path.realpath("__file__"))+"\media\\Nevermind.mp3")
    mixer.music.play(-1)

def click_mouse():
    pygame.mixer.init()
    threading.Thread(target=play_music).start()

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()
