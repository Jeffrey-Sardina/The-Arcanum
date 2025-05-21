from spell import *

'''
The Spellbook (mapping of text read from QR codes to actions)
You should modify this with your own music / image references
'''
SPELLBOOK = SPELLBOOK_BASE | {
    # Illusion spells -- modify at will
    # '1': Spell([
    #     'images/black.png'
    # ], ILLUSION_SPELL),

    # Music spells -- modify at will. A list will play songs in order.
    ## Ambiance
    '2': Spell([
        "music/ambiance.mp3"
    ], BARDIC_SPELL),

    '3': Spell([
        "music/limgrave.mp3"
    ], BARDIC_SPELL),

    '4': Spell([
        "music/giants-mountaintop.mp3"
    ], BARDIC_SPELL),

    '5': Spell([
        "music/witcher-night.mp3"
    ], BARDIC_SPELL),

    # Battle
    '6': Spell([
        "music/drums.mp3"
    ], BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED

    '7': Spell([
        "music/skyrim.mp3"
    ], BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED

    '8': Spell([
        "music/eldenring.mp3"
    ], BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED

    '9': Spell([
        "music/witcher-banana-tiger.mp3"
    ], BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED

    '9': Spell([
        "music/Baldurs-Gate/07 Baldur's Gate 3 OST - Lead Your Fights (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/05 Baldur's Gate 3 OST - Nine Blades (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/03  Baldur's Gate 3 OST - Mind Flayer Theme (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/10 Baldur's Gate 3 OST - Cunning Cruel Crits (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/12 Baldur's Gate 3 OST - Sixteen Strikes (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/14 Baldur's Gate 3 OST - Twisted Force (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/23 Baldur's Gate 3 OST - A Threat From Nether Years (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/32 Baldur's Gate 3 OST - The Legacy Of Bhaal (2023_10_28 11_55_15 UTC).mp3",
        "music/Baldurs-Gate/33 Baldur's Gate 3 OST - Elder Brain (2023_10_28 11_55_15 UTC).mp3"

    ], BARDIC_SPELL), #tag=TAG_MUSIC_LAYERED
}
