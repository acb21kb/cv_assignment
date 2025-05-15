import os
import numpy as np
import tkinter as tk
from tkinter import filedialog as openfile
from tkinter import ttk
from PIL import Image, ImageTk

import watermark_embed as embed
import watermark_recover as recover
import tamper_detect as detect

dir_path = os.path.dirname(os.path.realpath(__file__))
global current_watermark, current_img

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Watermark Tool")
        self.root.minsize(1200,800)
        self.root.maxsize(1200,800)

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
        # ^^^ use keypoints with watermark! -> LSB

    def run_recover(img:str):
        # ^^^ recover watermark from image
        return

    def check_tamper(img: str):
        # ^^^ check if image was tampered with
        # -> crop, resize, rotate
        return

    def main_page(self):
        ex_img = ImageTk.PhotoImage(Image.open(self.img))
        display_img = tk.Label(self.root, image=ex_img)
        display_img.image = ex_img
        display_img.pack()
        
        ex_watermark = ImageTk.PhotoImage(Image.open(self.watermark).resize((30,30)))
        display_watermark = tk.Label(self.root, image=ex_watermark)
        display_watermark.image = ex_watermark
        display_watermark.pack()

        # ^^^ Set these to update when new images chosen

        open_img = ttk.Button(self.root, text='Select image',
                    command= self.file_select)
        open_watermark = ttk.Button(self.root, text='Select watermark',
                    command=lambda: self.file_select(True))
        open_img.pack()
        open_watermark.pack()

gui = GUI()
gui.main_page()

gui.root.mainloop()