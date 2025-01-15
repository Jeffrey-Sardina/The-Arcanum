'''
DEFINE FUNCTIONS NEEDED FOR SPELLS
'''
BARDIC_SPELL = 'BARDIC_SPELL'
COMMAND_SPELL = 'COMMAND_SPELL'
FORBIDDEN_SPELL = 'FORBIDDEN_SPELL'
ILLUSION_SPELL = 'ILLUSION_SPELL'

class Spell:
    def __init__(self, spell_data, spell_type):
        self.spell_data = spell_data
        self.spell_type = spell_type

    def __call__(self):
        if self.spell_type == COMMAND_SPELL:
            self.spell_data()
        else:
            assert False, f"This Spell cannot be called! spell_type: {self.spell_type}; data: {self.spell_data}"

hello_world = Spell(
    spell_data = lambda: print('Hey, this spell worked!'),
    spell_type = COMMAND_SPELL
)

SPELLBOOK = {
    'stop-music': 'stop-music',
    'stop-illusion': 'stop-illusion',
    'exit': 'exit',
    '1': hello_world
}