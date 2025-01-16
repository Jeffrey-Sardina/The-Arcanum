'''
conda activate arcanum
sudo apt-get install vlc
'''

'''
===============================
IMPORTS, CONSTANTS, AND GLOBALS
===============================
'''
# external imports
import cv2 
import sys
import vlc
import tkinter
from PIL import Image, ImageOps, ImageTk

# constants (that you don't need to change)
from spellbook import SPELLBOOK
from spellbook import BARDIC_SPELL, COMMAND_SPELL, FORBIDDEN_SPELL, ILLUSION_SPELL
QR_LOCATOR = None
ILLUSION_ROOT = None
ILLUSION_CANVAS = None
CANVAS_W = None
CANVAS_H = None

# global vars
bard = None
current_music = None
current_image = None


'''
=============
MUSIC CONTROL
=============
'''
def stop_music():
    global current_music
    if bard:
        bard.stop()
        current_music = None

def play_music(music_file):
    global bard, current_music
    if music_file == current_music:
        return # dont replay what we already started playing
    stop_music()
    bard = vlc.MediaPlayer(music_file)
    bard.play()
    current_music = music_file


'''
========================
IMAGE (ILLUSION) CONTROL
========================
'''
def prep_image(image_file):
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
    ILLUSION_ROOT.im = image # to avoid GC issues; see: https://stackoverflow.com/questions/57049722/unable-to-update-image-in-tkinter-using-a-function
    return image

def stop_illusion(image_file):
    global current_image
    image = prep_image(image_file)
    show_illusion(image)
    current_image = None

def show_illusion(image_file):
    global current_image, ILLUSION_CONTAINER
    if image_file == current_image:
        return # dont redraw what we already are showing
    # https://www.tutorialspoint.com/how-to-update-an-image-in-a-tkinter-canvas
    image = prep_image(image_file)
    ILLUSION_CANVAS.itemconfig(ILLUSION_CONTAINER, image=image)
    current_image = image_file


'''
======================
ARCANUM CORE FUNCTIONS
======================
'''
def exit_arcanum():
    if SCRYING_EYE:
        try:
            SCRYING_EYE.release()
        except:
            pass
    if ILLUSION_ROOT:
        try:
            ILLUSION_ROOT.destroy()
        except:
            pass
    exit(0)

def arcanum_loop():
    _, img = SCRYING_EYE.read()
    qr_value, _, _ = QR_LOCATOR.detectAndDecode(img) 
    if qr_value and qr_value in SPELLBOOK: 
        spell = SPELLBOOK[qr_value]
        spell_data = spell.spell_data
        spell_type = spell.spell_type
        print(spell_data)

        if spell_type == BARDIC_SPELL:
            play_music(spell_data)
        elif spell_type == COMMAND_SPELL:
            spell()
        elif spell_type == FORBIDDEN_SPELL:
            if spell_data == 'stop-illusion':
                stop_illusion()
            elif spell_data == 'stop-music':
                stop_music()
            elif spell_data == 'exit':
                exit_arcanum()
        elif spell_type == ILLUSION_SPELL:
            show_illusion(spell_data)
        else:
            assert False, f"unknown spell type: {spell_type}; data: {spell_data}"
    ILLUSION_ROOT.after(int(SAMPLING_FREQ_SECONDS * 1000), arcanum_loop)

def enter_arcanum(camera_id):
    global QR_LOCATOR, ILLUSION_ROOT, ILLUSION_CANVAS, CANVAS_W, CANVAS_H, ILLUSION_CONTAINER

    # for vision
    QR_LOCATOR = cv2.QRCodeDetector()

    # for images; ref: https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
    ILLUSION_ROOT = tkinter.Tk()
    ILLUSION_ROOT.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    CANVAS_W = ILLUSION_ROOT.winfo_screenwidth()
    CANVAS_H = ILLUSION_ROOT.winfo_screenheight()
    ILLUSION_ROOT.attributes("-fullscreen", True) 
    ILLUSION_ROOT.geometry("%dx%d+0+0" % (CANVAS_W, CANVAS_H))
    ILLUSION_ROOT.focus_set()    
    ILLUSION_CANVAS = tkinter.Canvas(
        ILLUSION_ROOT,
        width=CANVAS_W,
        height=CANVAS_H,
        bg='green'
    )
    ILLUSION_CANVAS.pack(anchor=tkinter.CENTER)

    # display default null image
    image = prep_image('images/black.png')
    ILLUSION_CONTAINER = ILLUSION_CANVAS.create_image(
        (CANVAS_W // 2, CANVAS_H // 2),
        image=image
    )
    ILLUSION_ROOT.after(int(SAMPLING_FREQ_SECONDS * 1000), arcanum_loop)
    ILLUSION_ROOT.mainloop()

def process_args():
    enter_arcanum()

if __name__ == '__main__':
    # things the user may want to change
    SCRYING_EYE = cv2.VideoCapture(2) # cannot be in func for some reason
    SAMPLING_FREQ_SECONDS = 0.25

    # start program
    process_args()
