import tkinter as tk
from itertools import count
import os
import ctypes
import time
import threading

import vlc
from PIL import Image, ImageTk

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

        self.player = vlc.MediaPlayer(os.path.dirname(os.path.realpath("__file__"))+"\media\Nevermind.mp3")
        self.player.play()

        self.lbl = ImageLabel(self)
        self.lbl.pack()
        self.thread_kaun = threading.Thread(target=self.lbl.load, args=(os.path.dirname(os.path.realpath("__file__"))+"\media\gif.gif"),)
        self.thread_kaun.start()

        self.thread_bg = threading.Thread(target=self.bg_new)
        self.thread_bg.start()
        

    def bg_new(self):
        SPI_SETDESKWALLPAPER = 20
        gif_path = os.path.dirname(os.path.realpath("__file__"))+"\media\bg.gif"
        gif_image = Image.open(gif_path)
        frames = gif_image.n_frames
        frame_delay = 0.001
        while True:
            for frame in range(frames):
                gif_image.seek(frame)
                frame_image = gif_image.copy()
                frame_image_path = os.path.dirname(os.path.realpath("__file__"))+f"\media\frame\frame_{frame}.png"
                frame_image.save(frame_image_path)
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, frame_image_path, 3)
                time.sleep(frame_delay)
                os.remove(frame_image_path)        
                time.sleep(frame_delay)


app = App()
app.mainloop()
