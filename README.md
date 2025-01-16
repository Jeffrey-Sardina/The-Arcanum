# The Arcanum
Jeffrey Seathrún Sardina


## The Arcanum
The Arcanum is a set of hands-off, automated TTRPG tools for music and display management. Right now it's just want I want to use, but I'll try to make it modular so others can adapt it to their setups.

The idea is to manage visual and auditory ambiance (that is, music and projections) from a single place. This manages all commands from QR codes, meaning that in session you never have to touch a computer to use it.

This can be done, for example, with:
- qr codes printed in a fancy notebook (don't let your players see the codes -- make them think it's magic!)
- a Raspberry Pi for the control module
- HDMI connection from the Pi to a projector or screen (for visual effects / ambiance)
- Bluetooth or Aux connection from the Pi to a speaker (for music / ambient sound)
- a cheap webcam connected by USB to the Raspberry Pi (to see and respond to QR codes)

In all cases, default I/O is used -- so any of the above can we swapped out as long as your default webcam / sound / display is what you want the Arcanum to use.


## Why QR Codes?
Because QR codes can encode any string -- not just URLs. They are also super easy to decode (OpenCV has a system for that in Python) and very easy to generate. They also don't require any fancy / custom machine learning to read -- whereass a handwritten number would require a trained ML model to read. All in all -- they are simple and very effective.

For generating QR codes, you can use `qrgen.py` as so: `python qrgen.py TEXT text.png`. This file is optimised to make high-res QR codes you can easily print for use with The Arcanum, so to start out I recommend you use it. There are several other QR code generation methods; i.e. see https://pypi.org/project/qrcode/ or search `qr TEXT` on DuckDuckGo.


## Finding your Camera ID
If you have multiple webcams and want to choose which one to use, run `python find_camera.py` (and make sure your webcam is connected!)

For more information on loading webcams and possible issues, see here: https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python


## Requirements and Install
You'll need to run `pip install -r requirements.txt'`. It's recommended you do this in a conda environment; i.e. `conda create -n arcanum python=3.7`. You can then use that environment via `conda activate arcanum`. Info on how to set up Miniconda is here: https://docs.anaconda.com/miniconda/install/

On top of that, you'll need to install VLC: `sudo apt-get install vlc` as this package uses VLC for music.

I'm using Python 3.7 for legacy use (my RaspBerry Pi is way out of date) -- but this code should run on basically any Python 3. I'm trying to keep OS-specific stuff out as well, and as far as I know your OS should have no bearing on this package, as long as you can run Python 3.


## Useful References
1. https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
2. https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
3. https://www.geeksforgeeks.org/webcam-qr-code-scanner-using-opencv/
