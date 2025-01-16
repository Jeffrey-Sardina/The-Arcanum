'''
DEFINE FUNCTIONS NEEDED FOR SPELLS
'''
BARDIC_SPELL = 'BARDIC_SPELL'
FORBIDDEN_SPELL = 'FORBIDDEN_SPELL'
ILLUSION_SPELL = 'ILLUSION_SPELL'

class Spell:
    def __init__(self, spell_data, spell_type):
        self.spell_data = spell_data
        self.spell_type = spell_type

SPELLBOOK = {
    'stop-music': Spell('stop-music', FORBIDDEN_SPELL),
    'stop-illusion': Spell('stop-illusion', FORBIDDEN_SPELL),
    'exit': Spell('exit', FORBIDDEN_SPELL),

    '1': Spell('images/blue.png', ILLUSION_SPELL),
    '2': Spell('music/bg3.mp3', BARDIC_SPELL)
}
