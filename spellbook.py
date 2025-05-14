from spell import *

'''
The Spellbook (mapping of text read from QR codes to actions)
You should modify this with your own music / image references
'''
SPELLBOOK = SPELLBOOK_BASE | {
    # Illusion spells -- modify at will
    # '1': Spell('images/black.png', ILLUSION_SPELL),

    # Music spells -- modify at will.
    '2': Spell("music/ambiance.mp4", BARDIC_SPELL),
    '3': Spell("music/drums.mp3", BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED
    '4': Spell("music/skyrim.mp3", BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED
}