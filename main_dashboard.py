import os
import numpy as np
import tkinter as tk
from tkinter import filedialog as openfile
from tkinter import ttk
from PIL import Image, ImageTk

import watermark_embed as embed
import watermark_recover as recover
import tamper_detect as detect

PATH = os.path.dirname(os.path.realpath(__file__))

class GUI:
    def __init__(self):
        """
        Initialise class
        """
        self.root = tk.Tk()
        self.root.title("Watermark Tool")
        self.root.minsize(1200,800)
        self.root.maxsize(1200,800)

        self.img = 'cv_assignment/images/dashboard.png'
        self.watermark = 'cv_assignment/watermarks/watermark_3x3.png'
        
    def file_select(self, update_img: tk.Label, is_watermark: bool = False):
        """
        Allow user to select image files to be used
        """
        ftypes = (('PNG files', '*.png',),
                  ('JPEG files', '*.jpg'))
        path = PATH + '/images'
        if is_watermark:
            path = PATH + '/watermarks'

        file = openfile.askopenfilename(title='Select an image',
                        initialdir=path, filetypes=ftypes)
        
        img = Image.open(file)
        if is_watermark:
            img = ImageTk.PhotoImage(img.resize((30,30)))
            self.watermark = file
        else:
            w, h = img.size
            w = int((w/h) * 400)
            img = ImageTk.PhotoImage(img.resize((w,400)))
            self.img = file

        # update_img.configure(image=img)
        # update_img.image = img

    def run_embed(self, result_frame):
        """
        Embed watermark into image
        """
        new_img = embed.embed_watermark(self.watermark, self.img)
        res_img = Image.open(new_img)
        w, h = res_img.size
        w = int((w/h) * 400)
        res_img = ImageTk.PhotoImage(res_img.resize((w,400)))
        display_res = tk.Label(result_frame, image=res_img)
        display_res.image = res_img
        display_res.pack()

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
        main_frame = tk.Frame(self.root)

        # Left frame for displaying current image and watermark
        frame_l = tk.Label(main_frame, bg='gray')
        frame_l.grid(row=0, column=0)

        ex_img = Image.open(self.img)
        w, h = ex_img.size
        w = int((w/h) * 400)
        ex_img = ImageTk.PhotoImage(ex_img.resize((w,400)))
        display_img = tk.Label(frame_l, image=ex_img)
        display_img.image = ex_img
        
        ex_watermark = ImageTk.PhotoImage(Image.open(self.watermark).resize((30,30)))
        display_watermark = tk.Label(frame_l, image=ex_watermark)
        display_watermark.image = ex_watermark
        # ^^^ Set these to update when new images chosen!

        # Middle frame for image selection buttons
        frame_m = tk.Label(main_frame)
        frame_m.grid(row=0, column=1)
        open_img = ttk.Button(frame_m, text='Select image',
                    command=lambda: self.file_select(display_img))  
        open_watermark = ttk.Button(frame_m, text='Select watermark',
                    command=lambda: self.file_select(display_watermark, True))
        embed_watermark = ttk.Button(frame_m, text='Run embed watermark',
                    command=lambda: self.run_embed(frame_r))
    
        # Right frame for displaying results
        frame_r = tk.Label(main_frame, bg='red')
        frame_r.grid(row=0, column=2)

        # Set up grid layout of frame
        for row in range(1):
            main_frame.grid_rowconfigure(row, weight=1)
        for col in range(3):
            main_frame.grid_columnconfigure(col, weight=1)
        
        display_img.pack()
        display_watermark.pack()
        open_img.pack()
        open_watermark.pack()
        embed_watermark.pack()
        main_frame.pack()

if __name__ == "__main__":
    gui = GUI()
    gui.main_page()

    gui.root.mainloop()