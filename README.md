# The Arcanum
Jeffrey Seathrún Sardina

## The Arcanum
The Arcanum is a set of hands-off, automated TTRPG tools for music and display management. Right now it's just want I want to use, but I'll try to make it modular so others can adapt it to their setups.

The idea is this:
- a camera that looks at the GM and reads orders as QR codes
- a projector projecting on a table (or a screen built into that table, if you are fancy) for showing maps
- a speaker system
- a core module that manages everything

This can be done, for example, with:
- qr codes printed in a fancy notebook
- a Raspberry Pi for the core module
- HDMI connection to the projector
- Bluetooth or Aux connection to a speaker system
- a cheap webcam connected by USB to the Raspberry Pi

In all cases, default I/O is used -- so any of the above can we swapped out as long as your default webcam / sound / display is what you want the Arcanum to use.

I'm using Python 3.7 for legacy use (my RaspBerry Pi is way out of date) -- but this code should run on basically any Python 3. I'm trying to keep OS-specific stuff out as well, so hopefully your OS of choice will not matter.

## Requirements
You'll need to run `pip install -r requirements.txt'`.

On top of that, you'll need to install VLC: `sudo apt-get install vlc` as this package uses VLC for music.

## Useful References
1. https://stackoverflow.com/questions/47316266/can-i-display-image-in-full-screen-mode-with-pil
2. https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
3. https://www.geeksforgeeks.org/webcam-qr-code-scanner-using-opencv/
