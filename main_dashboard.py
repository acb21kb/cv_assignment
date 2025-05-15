import os
import numpy as np
import tkinter as tk
from tkinter import filedialog as openfile
from tkinter import ttk
import watermark_embed as embed
import watermark_recover as recover
import tamper_detect as detect

dir_path = os.path.dirname(os.path.realpath(__file__))
global current_watermark, current_img


class GUI:
    def __init__(self):
        self.img = 'cv_assignment/images/dashboard.png'
        self.watermark = 'cv_assignment/watermarks/watermark_1.png'

    def file_select(self, is_watermark: bool = False):
        ftypes = (('PNG files', '*.png',),
                    ('JPEG files', '*.jpg'))
        path = dir_path+'/images'
        if is_watermark:
            path = dir_path+'/watermarks'

        file = openfile.askopenfilename(title='Select an image',
                                        initialdir=path,
                                        filetypes=ftypes)
        if is_watermark:
            self.watermark = file
        else:
            self.img = file

    def run_embed(img: str, watermark):
        kp_img = embed.get_kp(img)


def main_page(gui):
    open_img = ttk.Button(root, text='Select image',
                command=gui.file_select)
    open_watermark = ttk.Button(root, text='Select watermark',
                command=lambda: gui.file_select(True))
    open_img.pack()
    open_watermark.pack()

root = tk.Tk()
root.title("Watermark Tool")
root.minsize(1200,800)
root.maxsize(1200,800)
gui = GUI()
main_page(gui)
root.mainloop()