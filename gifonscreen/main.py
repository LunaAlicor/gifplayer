import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk, ImageSequence
import os


def exit_program():
    global app
    app.destroy()


class AnimatedGif(tk.Label):
    def __init__(self, master=None, gif_path=None, **kwargs):
        super().__init__(master, **kwargs)
        self.gif_path = gif_path
        self.frames = []
        self.current_frame = 0
        self.update_id = None
        self.load_gif()
        self.update_animation()

    def load_gif(self):
        if self.update_id:
            self.after_cancel(self.update_id)

        self.frames = []
        try:
            with Image.open(self.gif_path) as img:
                for frame in ImageSequence.Iterator(img):
                    self.frames.append(ImageTk.PhotoImage(frame.copy()))
        except Exception as e:
            print(f"Error loading GIF {self.gif_path}: {e}")

        if self.frames:
            self.current_frame = 0
            self.update_animation()

    def update_animation(self):
        if not self.frames:
            print("No frames to display")
            return

        try:
            num_frames = len(self.frames)
            delay = max(100, 1000 // num_frames)

            self.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % num_frames

            self.update_id = self.after(delay-25, self.update_animation)
        except Exception as e:
            print(f"Error during animation update: {e}")


class DraggableWindow(tk.Tk):
    def __init__(self, gif_path):
        super().__init__()
        self.title("GIF Player")
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.geometry("800x600")
        self.configure(bg='black')

        self.gif_widget = AnimatedGif(self, gif_path=gif_path, bg='black')
        self.gif_widget.pack(fill=tk.BOTH, expand=True)
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.bind("<Button-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Button-2>", self.show_context_menu)

        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Open GIF", command=self.open_gif_menu)

        self.gif_directory = os.path.join(os.getcwd(), 'gif')
        self.gif_files = self.load_gif_files()


        self.attributes('-transparentcolor', 'black')

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

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def load_gif_files(self):
        try:
            gif_files = [f for f in os.listdir(self.gif_directory) if f.endswith('.gif')]
            if not gif_files:
                print("No GIF files found in the directory.")
            return gif_files
        except Exception as e:
            print(f"Error accessing GIF directory {self.gif_directory}: {e}")
            return []

    def open_gif_menu(self):
        menu = tk.Menu(self.context_menu, tearoff=0)
        for gif_file in self.gif_files:
            menu.add_command(label=gif_file, command=lambda f=gif_file: self.change_gif(f))
        menu.add_command(label="Exit", command=exit_program)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def change_gif(self, gif_file):
        gif_path = os.path.join(self.gif_directory, gif_file)
        print(f"Changing GIF to {gif_path}")
        self.gif_widget.gif_path = gif_path
        self.gif_widget.load_gif()


if __name__ == "__main__":
    initial_gif_path = os.path.join(os.getcwd(), 'gif', '2.gif')
    app = DraggableWindow(initial_gif_path)
    app.mainloop()
