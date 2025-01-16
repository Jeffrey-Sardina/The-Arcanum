'''
Background constants and Spell class
You should not modify this
'''
BARDIC_SPELL = 'BARDIC_SPELL'
FORBIDDEN_SPELL = 'FORBIDDEN_SPELL'
ILLUSION_SPELL = 'ILLUSION_SPELL'

class Spell:
    def __init__(self, spell_data, spell_type):
        self.spell_data = spell_data
        self.spell_type = spell_type

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
    '1': Spell('images/blue.png', ILLUSION_SPELL),

    # Music spells -- modify at will
    '2': Spell('music/bg3.mp3', BARDIC_SPELL),
}
