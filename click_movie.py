from pynput import mouse
import pygame
import os

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.dirname(os.path.realpath("__file__"))+"\media\\click.wav")  # Замените "sound_file.wav" на путь к вашему звуковому файлу
    pygame.mixer.music.play()

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        play_sound()

def click_mouse():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

