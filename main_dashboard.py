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
        self.watermark = 'cv_assignment/watermarks/watermark_5x5.png'
        
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

    def run_embed(self):
        """
        Embed watermark into image
        """
        embed.process_watermark(self.watermark, self.img)
        # ^^^ use keypoints with watermark! -> LSB

    def run_recover(self, img:str):
        """
        Recover watermark from image
        """
        return

    def check_tamper(self, img: str):
        """
        Check if image was tampered with
        """
        # -> crop, resize, rotate
        return

    def main_page(self):
        """
        Set up main page
        """
        frame_l = tk.Label(self.root, bg='gray')
        frame_l.grid(row=0, column=0)

        ex_img = ImageTk.PhotoImage(Image.open(self.img))
        display_img = tk.Label(frame_l, image=ex_img)
        display_img.image = ex_img
        display_img.pack()
        
        ex_watermark = ImageTk.PhotoImage(Image.open(self.watermark).resize((30,30)))
        display_watermark = tk.Label(frame_l, image=ex_watermark)
        display_watermark.image = ex_watermark
        display_watermark.pack()

        # ^^^ Set these to update when new images chosen!

        frame_m = tk.Label(self.root)
        frame_m.grid(row=0, column=1)

        open_img = ttk.Button(frame_m, text='Select image',
                    command= self.file_select)
        open_img.pack()

        open_watermark = ttk.Button(frame_m, text='Select watermark',
                    command=lambda: self.file_select(True))
        open_watermark.pack()

        frame_r = tk.Label(self.root, bg='red')
        frame_r.grid(row=0, column=2)

        embed_watermark = ttk.Button(frame_r, text='Run embed watermark',
                    command=self.run_embed)
        embed_watermark.pack()

        for row in range(1):
            self.root.grid_rowconfigure(row, weight=1)
        for col in range(3):
            self.root.grid_columnconfigure(col, weight=1)

if __name__ == "__main__":
    gui = GUI()
    gui.main_page()

    gui.root.mainloop()