'''
conda activate arcanum
'''
# external imports
import cv2 
import time
import vlc

# constants
SAMPLING_FREQ_SECONDS = 0.25
from spellbook import SPELLBOOK
from spellbook import BARDIC_SPELL, COMMAND_SPELL, FORBIDDEN_SPELL, ILLUSION_SPELL
SCRYING_EYE = cv2.VideoCapture(0) 
QR_LOCATOR = cv2.QRCodeDetector()

# global vars
bard = None
current_music = None
current_image = None

def stop_music():
    if bard:
        bard.stop()

def play_music(music_file):
    global bard, current_music
    if music_file == current_music:
        return # dont replay what we already started playing
    stop_music()
    bard = vlc.MediaPlayer(music_file)
    bard.play()
    current_music = music_file

def stop_illusion(image_file):
    pass

def show_illusion(image_file):
    global current_image
    if image_file == current_image:
        return # dont replay what we already started playing
    stop_illusion()
    # ...
    current_image = image_file

def exit_arcanum():
    SCRYING_EYE.release() 
    exit(0)

def enter_arcanum():
    while True: 
        _, img = SCRYING_EYE.read()
        qr_value, _, _ = QR_LOCATOR.detectAndDecode(img) 
        if qr_value and qr_value in SPELLBOOK: 
            spell = SPELLBOOK[qr_value]
            spell_data = spell.spell_data
            spell_type = spell.spell_type

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

        time.sleep(SAMPLING_FREQ_SECONDS)
  
if __name__ == '__main__':
    enter_arcanum()
