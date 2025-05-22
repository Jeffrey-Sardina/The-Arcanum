# The Arcanum
Jeffrey Seathrún Sardina<br>
Last updated May 2025


## The Arcanum
The Arcanum is a set of hands-off, automated TTRPG tools for music and display management. Right now it's just want I want to use, but I'll try to make it modular so others can adapt it to their setups.

The idea is to manage visual and auditory ambiance (that is, music and projections) from a single place. This manages all commands from QR codes, meaning that in session you never have to touch a computer to use it.

This can be done, for example, with:
- qr codes printed in a fancy notebook (don't let your players see the codes -- make them think it's magic!)
- a computer or Raspberry Pi for the control module
- HDMI connection from the Pi to a projector or screen (for visual effects / ambiance)
- Bluetooth or Aux connection from the Pi to a speaker (for music / ambient sound)
- a cheap webcam connected by USB to the computer / Raspberry Pi (to see and respond to QR codes)

In all cases, default I/O is used -- so any of the above can we swapped out as long as your default webcam / sound / display is what you want the Arcanum to use.


## Using the Arcanum
The easiest way to use the Arcanum is via the command `./arcanum.sh`, which will begin the Arcanum using your default camera and display device. If this is not what you want, however, then keep reading!

Command-line args for `arcanum.py`. The first is the ID of your webcam (if you only have one webcam, it will be automatically loaded and no ID need be specified). That means you can run this as `python arcanum.py 0` in almost all use cases (on some linux / MacOS versions, you might need to type python3, rather than python). You can further specify `-db` to enter into debug mode and `-re` to ask the Arcanum to resume your last-played music and image/video.

Hard-coded actions in `spellbook.py`. These are called "Spells" and are created using the `Spell` class (examples are given in that file). The Spellbook maps text to some sort of action -- note that the text is the value read off the QR code by the camera! There are three types of spells: 
    - FORBIDDEN_SPELL -- these are ones I use for special purposes (like closing the program). THere should be no need for you to never change them, though you might want to create QR codes for them.
    - BARDIC_SPELL -- contains a path to a music file. That file will be played if this command is given. This file must be on your computer (not, for example, on youtube -- for the moment at least).
    - ILLUSION_SPELL -- contains a path to an image file. That file will be displayed if this command is given. This file must be on your computer, not a link to a file online.

You may also want to tag a spell with TAG_MUSIC_LAYERED to play it as a sound effect. Music played this way
- does not repeat (most music will by default)
- can be played at the same time as "regular" music
- is intended to be mainly used for sound effects (like a door closing), but can be used for anything you'd like!

Define all the mappings you want, run Arcanum, and there you go! Just show it QR codes for each of your spells, and it will "cast" them for you!


## Finding your Camera ID
If you have multiple webcams and want to choose which one to use, run `python find_camera.py` (and make sure your webcam is connected!)

For more information on loading webcams and possible issues, see here: https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python


## Generating QR Codes to Print
For generating QR codes, you can use `qrgen.py` as so: `python qrgen.py TEXT text.png`. This file is optimised to make high-res QR codes you can easily print for use with The Arcanum, so to start out I recommend you use it. There are several other QR code generation methods; i.e. see https://pypi.org/project/qrcode/ or search `qr TEXT` on DuckDuckGo.

### Why QR Codes?
Because QR codes can encode any string -- not just URLs. They are also super easy to decode (OpenCV has a system for that in Python) and very easy to generate. They also don't require any fancy / custom machine learning to read -- whereas#s a handwritten number would require a trained ML model to read. All in all -- they are simple and very effective.


## Requirements and Install
You'll need to run `pip install -r requirements.txt'`. It's recommended you do this in a conda environment; i.e. `conda create -n arcanum python=3.7`. You can then use that environment via `conda activate arcanum`. Info on how to set up Miniconda is here: https://docs.anaconda.com/miniconda/install/

On top of that, you'll need to install VLC: `sudo apt-get install vlc` as this package uses VLC for music.

I'm using Python 3.7 for legacy use -- but this code should run on basically any Python 3.X. Currently I have only tested on Linux, but in theory a python 3.7 environment with all requirements installed, and VLC (https://www.videolan.org/vlc/) downloaded, *should* work on any OS.


## Dealing with Errors
When run via ./arcanum.sh, all logs can be found at:
- logs/arcanum.cmd.log (for commands it was given)
- logs/arcanum.err.log (for errors it had)

If run via python on the terminal, these will be printed to the terminal (to STDOUT and STDERR, in turn).

PLease note that **the #1 cause of error** in my experience is the computer being idle, which leads to the webcam being deactivated / going to sleep etc. I'm still working for a way around this, and will update when I have one!


## Useful References
1. https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
2. https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
3. https://www.geeksforgeeks.org/webcam-qr-code-scanner-using-opencv/
