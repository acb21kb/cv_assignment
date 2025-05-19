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
        Initialise class.
        """
        self.root = tk.Tk()
        self.root.title("Watermark Tool")
        self.root.minsize(1200,800)
        self.root.maxsize(1200,800)

        self.img = 'cv_assignment/images/dashboard.png'
        self.watermark = 'cv_assignment/watermarks/watermark_3x3.png'
        
    def file_select(self, update_img: tk.Label):
        """
        Allow user to select image files to be used and updates images.
        """
        ftypes = (('PNG files', '*.png',),
                  ('JPEG files', '*.jpg'))
        path = PATH + '/images'

        file = openfile.askopenfilename(title='Select an image',
                    initialdir=path, filetypes=ftypes)
        img = Image.open(file)
        w, h = img.size
        w = int((w/h) * 400)
        img = ImageTk.PhotoImage(img.resize((w,400)))
        self.img = file

        update_img.configure(image=img)
        update_img.image = img
        update_img.update()

    def watermark_select(self, update_img: tk.Label, i: int):
        """
        Update watermark to be used.
        """
        img, file = self.get_watermark(i)
        self.watermark = file

        update_img.configure(image=img)
        update_img.image = img
        update_img.update()

    def get_watermark(self, i: int):
        """
        Return watermark image.
        """
        size = str(i)+'x'+str(i)
        file = PATH + '/watermarks/watermark_'+size+'.png'
        img = Image.open(file)
        img = ImageTk.PhotoImage(img.resize((50,50)))
        return img, file

    def watermark_options(self, frame: tk.Label, update_frame: tk.Label, wm_opt: list[int], i: int):
        """
        Display all watermark options with buttons to select each.
        """
        wm, _ = self.get_watermark(wm_opt[i])
        display_wm = tk.Label(frame, image=wm)
        display_wm.image = wm
        display_wm.grid(row=0, column=i)
        open_wm = ttk.Button(frame, text='Select watermark',
                    command=lambda: self.watermark_select(update_frame, wm_opt[i]))    
        open_wm.grid(row=1, column=i)

    def run_embed(self, display_res: tk.Label, display_recover: tk.Label, drastic: int):
        """
        Embed watermark into image and display resulting image
        (either actual result or with watermarks clearly visible).
        """
        new_img, drastic_img = embed.embed_watermark(self.watermark, self.img, drastic)

        if drastic == 0:
            res_img = Image.open(new_img)
        else:
            res_img = Image.open(drastic_img)

        w, h = res_img.size
        w = int((w/h) * 400)
        res_img = ImageTk.PhotoImage(res_img.resize((w,400)))

        display_recover.configure(image=None)
        display_recover.image = None
        display_recover.update()

        display_res.configure(image=res_img)
        display_res.image = res_img
        display_res.update()

    def select_recover(self, display_res: tk.Label, display_recover: tk.Label, is_auth: tk.Label):
        """
        Select file to recover a watermark from.
        """
        ftypes = (('PNG files', '*.png',),
                  ('JPEG files', '*.jpg'))
        path = PATH + '/embedded'

        file = openfile.askopenfilename(title='Select an image to recover',
                    initialdir=path, filetypes=ftypes)
        self.run_recover(display_res, display_recover, is_auth, file)

    def run_recover(self, display_res: tk.Label, display_recover: tk.Label, is_auth:tk.Label, img:str):
        """
        Recover watermark from image.
        """
        recovered_wm = recover.recover_watermark(img)

        display_res.configure(image=None)
        display_res.image = None
        display_res.update()

        if recovered_wm is None:
            recovered = None
            text = "NO - Watermark could not be authenticated."
        else:
            recovered = ImageTk.PhotoImage(Image.open(recovered_wm).resize((50,50)))
            text = "YES - Consistent watermark found! This image is authenticated."
        
        display_recover.configure(image=recovered)
        display_recover.image = recovered
        display_recover.update()
        is_auth.configure(text=text)
        is_auth.text = text
        is_auth.update()

    def select_tamper(self):
        """
        Select file to detect tampering.
        """
        ftypes = (('PNG files', '*.png',),
                  ('JPEG files', '*.jpg'))
        path = PATH + '/tampered'

        file = openfile.askopenfilename(title='Select an image to recover',
                    initialdir=path, filetypes=ftypes)
        self.check_tamper(file)

    def check_tamper(self, img: str):
        """
        Check if image was tampered with.
        """
        # -> crop, resize, rotate
        detect.detect_tampering(img)
        return

    def main_page(self):
        """
        Set up main page.
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
        display_img.grid(row=0, column=0)

        open_img = ttk.Button(frame_l, text='Select image',
                    command=lambda: self.file_select(display_img))
        open_img.grid(row=1, column=0)
        
        ex_watermark = ImageTk.PhotoImage(Image.open(self.watermark).resize((50,50)))
        display_watermark = tk.Label(frame_l, image=ex_watermark)
        display_watermark.image = ex_watermark
        display_watermark.grid(row=2, column=0)

        # Display the watermark options
        frame_l2 = tk.Label(main_frame)
        frame_l2.grid(row=1, column=0)
        
        wm_options = [3, 5, 7, 9]
        for i in range(len(wm_options)):
            self.watermark_options(frame_l2, display_watermark, wm_options, i)

        # Right frame for displaying results
        frame_r = tk.Label(main_frame)
        frame_r.grid(row=0, column=2)

        display_res = tk.Label(frame_r)
        display_res.grid(row=0, column=0)
        display_recover = tk.Label(frame_r)
        display_recover.grid(row=1, column=0)
        is_auth = tk.Label(frame_r)
        is_auth.grid(row=2, column=0)

        # Middle frame for image selection buttons
        frame_m = tk.Label(main_frame)
        frame_m.grid(row=0, column=1)
        
        embed_watermark = ttk.Button(frame_m, text='Run embed watermark',
                    command=lambda: self.run_embed(display_res, display_recover, do_drastic.get()))
        embed_watermark.grid(row=0, column=0)

        do_drastic = tk.IntVar()
        display_drastic = tk.Checkbutton(frame_m, text='Display with visible changes?',
                    variable=do_drastic)
        display_drastic.grid(row=1, column=0)

        recover_img = ttk.Button(frame_m, text='Run recover watermark',
                    command=lambda: self.select_recover(display_res, display_recover, is_auth))
        recover_img.grid(row=3, column=0)

        check_tamper = ttk.Button(frame_m, text='Run tamper detection',
                    command=self.select_tamper)
        check_tamper.grid(row=4, column=0)
        

        # Set up grid layout of frame
        for row in range(1):
            main_frame.grid_rowconfigure(row, weight=1)
        for col in range(3):
            main_frame.grid_columnconfigure(col, weight=1)
        
        main_frame.pack()

if __name__ == "__main__":
    gui = GUI()
    gui.main_page()

    gui.root.mainloop()