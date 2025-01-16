import tkinter as tk

def prep_image(image_file):
    from PIL import Image, ImageOps, ImageTk
    image = Image.open(image_file)
    base_w, base_h = image.size
    img_ratio = base_w / base_h
    screen_ratio = CANVAS_W / CANVAS_H
    tolerance = 0.001
    if screen_ratio - img_ratio > tolerance:
        # see which dim needs to scale less (to avoid the other one getting too big)
        change_ratio_w = CANVAS_W / base_w
        change_ratio_h = CANVAS_H / base_h
        scale_ratio = min(change_ratio_w, change_ratio_h)

        # get new dims with that scaling
        new_w = int(base_w * scale_ratio)
        new_h = int(base_h * scale_ratio)
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # pad to desired screen size
        if new_w < CANVAS_W:
            diff_w = CANVAS_W - new_w
            pad_lat = diff_w // 2
        else:
            pad_lat = 0
        if new_h < CANVAS_H:
            diff_h = CANVAS_H - new_h
            pad_top = diff_h // 2
        else:
            pad_top = 0
        padding = (pad_lat, pad_top, pad_lat, pad_top)
        ImageOps.expand(image, padding)
    else:
        # rescale to fix correct pixel size
        image = image.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(image)
    return image

ILLUSION_ROOT = tk.Tk()
ILLUSION_ROOT.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
CANVAS_W = ILLUSION_ROOT.winfo_screenwidth()
CANVAS_H = ILLUSION_ROOT.winfo_screenheight()
ILLUSION_ROOT.attributes("-fullscreen", True) 
ILLUSION_ROOT.geometry("%dx%d+0+0" % (CANVAS_W, CANVAS_H))
ILLUSION_ROOT.focus_set()    
ILLUSION_CANVAS = tk.Canvas(
    ILLUSION_ROOT,
    width=CANVAS_W,
    height=CANVAS_H,
    bg='green'
)
ILLUSION_CANVAS.pack(anchor=tk.CENTER)


python_image = prep_image('images/black.png')
ILLUSION_CANVAS.create_image(
    (CANVAS_W // 2, CANVAS_H // 2),
    image=python_image
)
ILLUSION_ROOT.mainloop()


# root = tk.Tk()
# root.geometry('800x600')
# root.title('Canvas Demo - Image')

# canvas = tk.Canvas(root, width=600, height=400, bg='white')
# canvas.pack(anchor=tk.CENTER, expand=True)

# python_image = tk.PhotoImage(file='images/blue.png')
# canvas.create_image(
#     (100, 100),
#     image=python_image
# )


# root.mainloop()