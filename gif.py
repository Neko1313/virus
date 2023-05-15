import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import vlc

p = vlc.MediaPlayer("./Nevermind.mp3")
p.play()

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

root = tk.Tk()
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 400
window_height = 400

x = screen_width - window_width - 10
y = screen_height - window_height - 10
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


lbl = ImageLabel(root)
lbl.pack()
lbl.load('ff.gif')
root.mainloop()