BARDIC_SPELL = 'BARDIC_SPELL'
FORBIDDEN_SPELL = 'FORBIDDEN_SPELL'
ILLUSION_SPELL = 'ILLUSION_SPELL'

'''
Bardic (music) spell tags.

These have the following meanings:
- STANDARD: the standard type if for a single music / sound filre you want to play at once. Only one standard sound can play at a time, so new ones cancel out previous ones, even if they are playing. If nothign is specified, standard is assumed.
- LAYERED: the layered type means the sound should layer over eixsting sound as a sound effect -- not replace it. Note: this is NOT recommended for muxing music streams -- do that in advance, as Arcanum does not allow relative volume changes. This is means for relatively short sounds effects, such as a crash.
'''
TAG_STANDARD = "STANDARD"
TAG_MUSIC_LAYERED = "LAYERED"

class Spell:
    def __init__(self, spell_data, spell_type, tag=TAG_STANDARD):
        if type(spell_data) == str:
            self.spell_data = [spell_data]
        else:
            self.spell_data = spell_data
        self.spell_type = spell_type
        self.tag = tag

SPELLBOOK_BASE = {
    # Forbidden spells -- not not modify
    'stop-music': Spell('stop-music', FORBIDDEN_SPELL),
    'stop-illusion': Spell('stop-illusion', FORBIDDEN_SPELL),
    'exit': Spell('exit', FORBIDDEN_SPELL),
}
