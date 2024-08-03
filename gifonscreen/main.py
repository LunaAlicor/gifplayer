import tkinter as tk
from PIL import Image, ImageTk, ImageSequence


class AnimatedGif(tk.Label):
    def __init__(self, master=None, gif_path=None, **kwargs):
        super().__init__(master, **kwargs)
        self.gif_path = gif_path
        self.frames = []
        self.current_frame = 0
        self.load_gif()
        self.update_animation()

    def load_gif(self):
        with Image.open(self.gif_path) as img:
            for frame in ImageSequence.Iterator(img):
                self.frames.append(ImageTk.PhotoImage(frame))

    def update_animation(self):
        if self.frames:
            self.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.after(50, self.update_animation)


class DraggableWindow(tk.Tk):
    def __init__(self, gif_path):
        super().__init__()
        self.title("gifplayer")
        self.attributes('-topmost', True)
        self.overrideredirect(True)

        self.gif_widget = AnimatedGif(self, gif_path=gif_path)
        self.gif_widget.pack()
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.bind("<Button-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)

    def on_start_drag(self, event):
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

    def on_drag(self, event):
        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.geometry(f"+{new_x}+{new_y}")
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root


if __name__ == "__main__":
    gif_path = r'C:\Users\wowbg\PycharmProjects\pythonProject3\gifonscreen\gif\3.gif'
    app = DraggableWindow(gif_path)
    app.mainloop()
