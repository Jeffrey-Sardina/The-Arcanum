'''
Background constants and Spell class
You should not modify this
'''
BARDIC_SPELL = 'BARDIC_SPELL'
FORBIDDEN_SPELL = 'FORBIDDEN_SPELL'
ILLUSION_SPELL = 'ILLUSION_SPELL'

'''
Bardic (music) spell tags.
You should not modify this

These ahve the following meanings:
- STANDARD: the standard type if for a single music / sound filre you want to play at once. Only one standard sound can play at a time, so new ones cancel out previous ones, even if they are playing. If nothign is specified, standard is assumed.
- LAYERED: the layered type means the sound should layer over eixsting sound as a sound effect -- not replace it. Note: this is NOT recommended for muxing music streams -- do that in advance, as Arcanum does not allow relative volume changes. This is means for relatively short sounds effects, such as a crash.
'''
TAG_STANDARD = "STANDARD"
TAG_MUSIC_LAYERED = "LAYERED"


class Spell:
    def __init__(self, spell_data, spell_type, tag=TAG_STANDARD):
        self.spell_data = spell_data
        self.spell_type = spell_type
        self.tag = tag

'''
The Spellbook (mapping of text read from QR codes to actions)
You should modify this with your own music / image references
You should not modify anything to do with forbidden spells
'''
SPELLBOOK = {
    # Forbidden spells -- not not modify
    'stop-music': Spell('stop-music', FORBIDDEN_SPELL),
    'stop-illusion': Spell('stop-illusion', FORBIDDEN_SPELL),
    'exit': Spell('exit', FORBIDDEN_SPELL),

    # Illusion spells -- modify at will
    # '1': Spell('images/blue.png', ILLUSION_SPELL),

    # Music spells -- modify at will
    '2': Spell("music/2.mp3", BARDIC_SPELL),
    '3': Spell("music/3.wav", BARDIC_SPELL, tag=TAG_MUSIC_LAYERED),
}
