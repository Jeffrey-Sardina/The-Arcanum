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
    'stop-music': Spell('stop-music', FORBIDDEN_SPELL),
    'stop-illusion': Spell('stop-illusion', FORBIDDEN_SPELL),
    'exit': Spell('exit', FORBIDDEN_SPELL),
    'hello': hello_world,

    '0': Spell('images/elden.webp', ILLUSION_SPELL),
    '1': Spell('images/bg3.webp', ILLUSION_SPELL),
    '2': Spell('music/bg3.mp3', BARDIC_SPELL)
}
