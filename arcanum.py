#!/usr/bin/env python3

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

# internal imports
from spell import *
from spellbook import SPELLBOOK
from find_camera import find_working_ids

# constants (that you don't need to change)
QR_LOCATOR = None
ILLUSION_ROOT = None
ILLUSION_CANVAS = None
CANVAS_W = None
CANVAS_H = None
BARD_LOG = 'logs/music.cur.txt'
ILLUSION_LOG = 'logs/visual.cur.txt'

# global vars
bard = None
bard_layered = None
current_music = None
current_music_layered = None
music_queue = None
current_image = None


'''
=============
MUSIC CONTROL
=============
'''
def write_curr_music(line):
    with open(BARD_LOG, 'w') as out:
        print(line, file=out)

def write_cur_display(line):
    with open(ILLUSION_LOG, 'w') as out:
        print(line, file=out)

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
        write_curr_music(music_file)
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
    write_cur_display(image_file)
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
    global music_queue, current_music, restart_file
    try:
        if bard and bard.get_state() == 6: #ended
            if len(music_queue) > 0:
                next_music = music_queue[0]
                play_music(next_music, tag=TAG_STANDARD)
                music_queue = music_queue[1:]
            else:
                next_music = current_music
                current_music = None
                play_music(next_music, tag=TAG_STANDARD) # repeat
        
        if bard_layered and bard_layered.get_state() == 6: #ended
            stop_music(streams=TAG_MUSIC_LAYERED) #do a reset

        if restart_bard_file:
            print('restarting', restart_bard_file)
            play_music(restart_bard_file)
            restart_bard_file = False
        if restart_illusion_file:
            print('restarting', restart_illusion_file)
            show_illusion(restart_illusion_file)
            restart_illusion_file = False

        _, img = SCRYING_EYE.read()
        try:
            qr_value, _, _ = QR_LOCATOR.detectAndDecode(img) #detectAndDecodeCurved
        except:
            qr_value = False
            if debug:
                raise
            else:
                print('error')
        if qr_value:
            if qr_value in SPELLBOOK: 
                spell = SPELLBOOK[qr_value]
                spell_data = spell.spell_data
                spell_type = spell.spell_type
                spell_tag = spell.tag
                print(spell_data)

                # music
                if spell_type == BARDIC_SPELL:
                    first_music = spell_data[0]
                    play_music(first_music, tag=spell_tag)
                    if spell_tag == TAG_STANDARD:
                        music_queue = spell_data[1:]

                # arcanum commands
                elif spell_type == FORBIDDEN_SPELL:
                    if 'stop-illusion' in spell_data:
                        stop_illusion()
                    elif 'stop-music' in spell_data:
                        stop_music()
                    elif 'exit' in spell_data:
                        exit_arcanum()
            
                # images
                elif spell_type == ILLUSION_SPELL:
                    show_illusion(spell_data)

                # error handling
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
    debug = False
    restart_bard_file = False
    restart_illusion_file = False

    try:
        # command line args
        try:
            cam_id = int(sys.argv[1])
        except:
            print('No camera found. Attempting a scan to find a connected camera')
            working_ids = find_working_ids()
            if len(working_ids) == 1:
                cam_id = working_ids[0]
            else:
                print('More than one camera found, unsure which to use. Please specify.')
                print(f'Working camera ids are: {working_ids}')
                raise
        if "-db" in sys.argv:
            debug = True
        if '-re' in sys.argv:
            try:
                with open(BARD_LOG, 'r') as inp:
                    restart_bard_file = inp.readlines()[0].strip()
            except:
                pass
            try:
                with open(ILLUSION_LOG, 'r') as inp:
                    restart_illusion_file = inp.readlines()[0].strip()
            except:
                pass

        sampling_freq = 0.01
        SCRYING_EYE = cv2.VideoCapture(cam_id) # cannot be in func for some reason
        SAMPLING_FREQ_SECONDS = float(sampling_freq)
    except:
        print('Error: invalid usage')
        print('Usage:')
        print('python arcanum.py CAMERA_ID')
        print('If you do not know the ID of your camera, the built-in (or only) webcame is 0.')
        print('To find the IDs of other webcams (which may not be sequential), use find_camera.py or see the details printed above')
        exit(1)

    # start program
    enter_arcanum()
