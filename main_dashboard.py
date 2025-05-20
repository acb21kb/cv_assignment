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
        self.img = file

        img = Image.open(file)
        img = self.resize(img)
        update_img.configure(image=img)
        update_img.image = img
        update_img.update()

    def watermark_select(self, update_img: tk.Label, i: int):
        """
        Update watermark to be used.
        """
        img, file = self.get_watermark(i)
        self.watermark = file

        img = ImageTk.PhotoImage(img.resize((75,75)))
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
        return img, file

    def watermark_options(self, frame: tk.Label, update_frame: tk.Label, wm_opt: list[int], i: int):
        """
        Display all watermark options with buttons to select each.
        """
        wm, _ = self.get_watermark(wm_opt[i])
        wm = ImageTk.PhotoImage(wm.resize((50,50)))
        display_wm = tk.Label(frame, image=wm)
        display_wm.image = wm
        display_wm.grid(row=0, column=i)
        open_wm = ttk.Button(frame, text='Select '+str(wm_opt[i])+'x'+str(wm_opt[i])+' watermark',
                    command=lambda: self.watermark_select(update_frame, wm_opt[i]))    
        open_wm.grid(row=1, column=i)

    def run_embed(self, display_res: tk.Label, is_auth: tk.Label, drastic: int):
        """
        Embed watermark into image and display resulting image
        (either actual result or with watermarks clearly visible).
        """
        display_res.configure(image=None)
        display_res.image = None
        display_res.update()
        is_auth.configure(text=None)
        is_auth.text = None
        is_auth.update()
        
        new_img, drastic_img = embed.embed_watermark(self.watermark, self.img, drastic)

        if drastic == 0:
            res_img = Image.open(new_img)
        else:
            res_img = Image.open(drastic_img)

        res_img = self.resize(res_img)

        display_res.configure(image=res_img)
        display_res.image = res_img
        display_res.update()

    def select_recover(self, display_res: tk.Label, is_auth: tk.Label):
        """
        Select file to recover a watermark from.
        """
        ftypes = (('PNG files', '*.png',),
                  ('JPEG files', '*.jpg'))
        path = PATH + '/embedded'

        file = openfile.askopenfilename(title='Select an image to recover',
                    initialdir=path, filetypes=ftypes)
        self.run_recover(display_res, is_auth, file)

    def run_recover(self, display_res: tk.Label, is_auth: tk.Label, img:str):
        """
        Recover watermark from image.
        """
        display_res.configure(image=None)
        display_res.image = None
        display_res.update()
        is_auth.configure(text="")
        is_auth.text = ""
        is_auth.update()

        auth, recovered_wm, confidence = recover.recover_watermark(img)

        if not auth:
            text = "NO - Watermark could not be authenticated."
        else:
            recovered = ImageTk.PhotoImage(Image.open(recovered_wm).resize((50,50)))
            if confidence < 0.6:
                extra = " mostly "
            else:
                extra = " "
            confidence = str(np.round(confidence*100, 1))
            text = "YES - Consistent watermark found!\nThis image is"+extra+"authenticated with "+confidence+"% confidence"
            display_res.configure(image=recovered)
            display_res.image = recovered
            display_res.update()

        is_auth.configure(text=text)
        is_auth.text = text
        is_auth.update()

    def select_tamper(self, display_res: tk.Label, is_auth: tk.Label):
        """
        Select file to detect tampering.
        """
        ftypes = (('PNG files', '*.png',),
                  ('JPEG files', '*.jpg'))
        path = PATH + '/tampered'
        path2 = PATH + '/embedded'

        file = openfile.askopenfilename(title='Select an image to recover',
                    initialdir=path, filetypes=ftypes)
        file2 = openfile.askopenfilename(title='Select original of image',
                    initialdir=path2, filetypes=ftypes)
        self.check_tamper(display_res, is_auth, file, file2)

    def check_tamper(self, display_res: tk.Label, is_auth: tk.Label, img: str, og_img:str):
        """
        Check if image was tampered with.
        """
        tampered, result = detect.detect_tampering(img, og_img)

        if tampered and result is not None:
            result = self.resize(Image.open(result))
            display_res.configure(image=result)
            display_res.image = result
            display_res.update()
            text = "YES - Tampering probable. Watermark could not be authenticated."
        else:
            text = "NO - Tampering unlikely. Watermark appears consistent."
            
        is_auth.configure(text=text)
        is_auth.text = text
        is_auth.update()

    def resize(self, img):
        w, h = img.size
        h = int((h/w) * 400)
        return ImageTk.PhotoImage(img.resize((400,h)))

    def main_page(self):
        """
        Set up main page.
        """
        main_frame = tk.Frame(self.root)

        framerows = 1
        framecols = 3

        # Left frame for displaying current image and watermark
        frame_l = tk.Frame(main_frame)
        frame_l.pack_propagate(0)
        frame_l.grid(row=0, column=0, rowspan=framerows)

        embed_title = tk.Label(frame_l, text="Current image to embed:",
                               font=("Helvetica",12,"bold"))
        embed_title.grid(row=0, column=0)
        
        ex_img = Image.open(self.img)
        ex_img = self.resize(ex_img)
        display_img = tk.Label(frame_l, image=ex_img)
        display_img.image = ex_img
        display_img.grid(row=1, column=0, pady=5)

        open_img = ttk.Button(frame_l, text='Select image to watermark',
                    command=lambda: self.file_select(display_img))
        open_img.grid(row=2, column=0, pady=(1,15))
        
        embed_title2 = tk.Label(frame_l, text="Current watermark to embed:",
                                font=("Helvetica",12,"bold"))
        embed_title2.grid(row=3, column=0)
        
        ex_watermark = ImageTk.PhotoImage(Image.open(self.watermark).resize((75,75)))
        display_watermark = tk.Label(frame_l, image=ex_watermark, bg='thistle')
        display_watermark.image = ex_watermark
        display_watermark.grid(row=4, column=0, pady=5)

        # Display the watermark options
        frame_l2 = tk.Frame(frame_l, bg='thistle')
        frame_l2.grid(row=5, column=0, pady=(10,1))
        
        wm_options = [3, 5, 7, 9]
        for i in range(len(wm_options)):
            self.watermark_options(frame_l2, display_watermark, wm_options, i)

        # Right frame for displaying results
        frame_r = tk.Frame(main_frame)
        frame_r.grid(row=0, column=2)

        result_title = tk.Label(frame_r, text="Results from functions:",
                               font=("Helvetica",12,"bold"))
        result_title.grid(row=0, column=0)

        display_result = tk.Label(frame_r)
        display_result.grid(row=1, column=0)
        is_auth = tk.Label(frame_r)
        is_auth.grid(row=2, column=0)

        # Middle frame for image selection buttons
        frame_m = tk.Frame(main_frame)
        frame_m.grid(row=0, column=1)

        function_title = tk.Label(frame_m, text="Run functions:",
                               font=("Helvetica",12,"bold"))
        function_title.grid(row=0, column=0)
        
        embed_watermark = ttk.Button(frame_m, text='Run embed watermark',
                    command=lambda: self.run_embed(display_result, is_auth, do_drastic.get()))
        embed_watermark.grid(row=1, column=0)

        do_drastic = tk.IntVar()
        display_drastic = tk.Checkbutton(frame_m, text='Display with visible changes?',
                    variable=do_drastic)
        display_drastic.grid(row=2, column=0, pady=(1,10))

        recover_img = ttk.Button(frame_m, text='Run recover watermark',
                    command=lambda: self.select_recover(display_result, is_auth))
        recover_img.grid(row=3, column=0)

        check_tamper = ttk.Button(frame_m, text='Run tamper detection',
                    command=lambda: self.select_tamper(display_result, is_auth))
        check_tamper.grid(row=4, column=0, pady=10)
        

        # Set up grid layout of frame
        for row in range(framerows):
            main_frame.grid_rowconfigure(row, weight=1)
        for col in range(framecols):
            main_frame.grid_columnconfigure(col, weight=1)
        
        main_frame.pack()

if __name__ == "__main__":
    gui = GUI()
    gui.main_page()

    gui.root.mainloop()