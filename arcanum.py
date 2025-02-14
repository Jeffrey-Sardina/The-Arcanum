'''
===============================
IMPORTS, CONSTANTS, AND GLOBALS
===============================
'''
# external imports
import cv2 
import vlc
import tkinter
from PIL import Image, ImageOps, ImageTk
import sys

# constants (that you don't need to change)
from spellbook import SPELLBOOK
from spellbook import BARDIC_SPELL, FORBIDDEN_SPELL, ILLUSION_SPELL
from spellbook import TAG_STANDARD, TAG_MUSIC_LAYERED
QR_LOCATOR = None
ILLUSION_ROOT = None
ILLUSION_CANVAS = None
CANVAS_W = None
CANVAS_H = None

# global vars
bard = None
bard_layered = None
current_music = None
current_music_layered = None
current_image = None


'''
=============
MUSIC CONTROL
=============
'''
def stop_music(streams="All"):
    '''
    If only standard is true, only music being played with the standard tag will be stopped
    '''
    global current_music, current_music_layered

    if TAG_STANDARD in streams or streams == "All":
        current_music = None
        if bard:
            bard.stop()

    if TAG_MUSIC_LAYERED in streams or streams == "All":
        current_music_layered = None
        if bard_layered:
            bard_layered.stop()

def play_music(music_file, tag=TAG_STANDARD):
    global bard, bard_layered, current_music, current_music_layered
    
    if tag == TAG_STANDARD:
        if music_file == current_music:
            return # dont replay what we already started playing
        stop_music(streams=TAG_STANDARD)
        bard = vlc.MediaPlayer(music_file)
        bard.play()
        current_music = music_file
    else:
        if music_file == current_music_layered:
            return # dont replay what we already started playing
        stop_music(streams=TAG_MUSIC_LAYERED)
        bard_layered = vlc.MediaPlayer(music_file)
        bard_layered.play()
        current_music_layered = music_file 


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
    try:
        if bard and bard.get_state() == 6: #ended
            stop_music(streams=TAG_STANDARD) #do a reset
        
        if bard_layered and bard_layered.get_state() == 6: #ended
            stop_music(streams=TAG_MUSIC_LAYERED) #do a reset

        _, img = SCRYING_EYE.read()
        qr_value, _, _ = QR_LOCATOR.detectAndDecode(img)
        if qr_value:
            if qr_value in SPELLBOOK: 
                spell = SPELLBOOK[qr_value]
                spell_data = spell.spell_data
                spell_type = spell.spell_type
                spell_tag = spell.tag
                print(spell_data)

                if spell_type == BARDIC_SPELL:
                    play_music(spell_data, tag=spell_tag)
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
            else:
                print(f'Found QR value {qr_value}, but it is not mapped to a spell')
        ILLUSION_ROOT.after(int(SAMPLING_FREQ_SECONDS * 1000), arcanum_loop)
    except:
        if debug:
            raise
        else:
            print('ERROR')
            exit_arcanum()

def enter_arcanum():
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

if __name__ == '__main__':
    try:
        # command line args
        cam_id = int(sys.argv[1])
        if "-db" in sys.argv:
            debug = True

        sampling_freq = 0.01
        SCRYING_EYE = cv2.VideoCapture(cam_id) # cannot be in func for some reason
        SAMPLING_FREQ_SECONDS = float(sampling_freq)
    except:
        print('Error: invalid usage')
        print('Usage:')
        print('python arcanum.py CAMERA_ID')
        print('If you do not know the ID of your camera, the built-in (or only) webcame is 0.')
        print('To find the IDs of other webcame (which may not be sequential), use find_camera.py')
        exit(1)

    # start program
    enter_arcanum()
