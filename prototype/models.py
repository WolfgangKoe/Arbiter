from dataclasses import dataclass

PHASES: list[tuple[str, str]] = [
    ("Befehlsphase", "command"),
    ("Bewegungsphase", "movement"),
    ("Psiphase", "psychic"),
    ("Schussphase", "shooting"),
    ("Sturmphase", "charge"),
    ("Kampfphase", "fight"),
    ("Moralphase", "morale"),
]


@dataclass
class Weapon:
    name: str
    attacks: str  # "1", "D6", "2D6", etc.
    skill: int  # target number (e.g. 3 means hits on 3+)
    strength: int
    ap: int  # 0, -1, -2, … (negative = armour-piercing)
    damage: str  # "1", "D3", "D6", etc.
    abilities: str = ""
    is_melee: bool = False


@dataclass
class UnitData:
    uid: str
    name: str
    count: int  # number of models
    move: str
    toughness: int
    save: int  # e.g. 3 means 3+
    invuln: int | None  # invulnerable save value or None
    fnp: int | None  # feel-no-pain value or None
    wounds: int  # wounds per model
    leadership: int
    oc: int
    weapons: list[Weapon]
    abilities: str = ""
    keywords: str = ""


# ---------------------------------------------------------------------------
# Zarekhan'Sol – Patrol Detachment (Necrons, Nephrekh, 25PL / 485pts / 3CP)
# Dynastic Code: Translocation Beams → alle Einheiten mit Dynastiecode: 6+ Invuln
# ---------------------------------------------------------------------------
NECRON_UNITS: list[UnitData] = [
    UnitData(
        uid="overlord",
        name="Overlord (Warlord)",
        count=1,
        move='6"',
        toughness=5,
        save=3,
        invuln=4,
        fnp=None,
        wounds=5,
        leadership=10,
        oc=1,
        weapons=[
            # Gauntlet: auto-hits (skill=1); statt Wund-Roll → D6 pro Modell, 6er = 1 MV
            Weapon(
                "Gauntlet of the Conflagrator",
                "1",
                1,
                5,
                0,
                "1",
                "Auto-trifft! Kein Wundwurf: 1W6 pro Modell im Ziel, jede 6 = 1 MV (Rettungswürfe ignoriert)",
            ),
            # Voidscythe: S×2=10, AP-4, D3; -1 zum Treffen bereits eingerechnet (WS2+→3+)
            Weapon(
                "Voidscythe",
                "4",
                3,
                10,
                -4,
                "3",
                "-1 zum Trefferwurf (bereits eingerechnet: WS2+ → 3+)",
                is_melee=True,
            ),
        ],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Phase Shifter: 4+ Invuln | "
            "Warlord-Trait: Skin of Living Gold (-1 auf Trefferwürfe gegen diesen) | "
            'My Will Be Done: 1 befreundete CORE-Einheit in 9" +1 auf Trefferwürfe | '
            'Relentless March (Aura): befreundete CORE in 6" +1" Bewegung | '
            'Resurrection Orb: 1×/Spiel Reanimation-Protokoll für befreundete Einheit in 6"'
        ),
        keywords="Infantry, Character, Noble, Overlord, Warlord",
    ),
    UnitData(
        uid="warriors",
        name="Necron Warriors ×10",
        count=10,
        move='5"',
        toughness=4,
        save=4,
        invuln=6,
        fnp=None,
        wounds=1,
        leadership=10,
        oc=2,
        weapons=[
            Weapon("Gauss Reaper", "2", 3, 5, -2, "1", 'Assault 2, 12"'),
            Weapon("Nahkampfwaffe", "1", 3, 4, 0, "1", is_melee=True),
        ],
        abilities=(
            "Reanimation Protocols | Their Number Is Legion: RP-Würfe von 1 wiederholen | "
            "Objective Secured | Nephrekh: 6+ Invuln"
        ),
        keywords="Infantry, Core, Necron Warriors",
    ),
    UnitData(
        uid="skorpekh",
        name="Skorpekh Destroyers ×3",
        count=3,
        move='8"',
        toughness=5,
        save=3,
        invuln=6,
        fnp=None,
        wounds=3,
        leadership=10,
        oc=2,
        weapons=[
            Weapon(
                "Hyperphase Reap-Blade",
                "3",
                3,
                7,
                -4,
                "3",
                "1 Modell (S: Profil+2=7)",
                is_melee=True,
            ),
            Weapon(
                "Hyperphase Threshers",
                "4",
                3,
                5,
                -3,
                "2",
                "2 Modelle; +1 Angriff des Trägers pro Kampf",
                is_melee=True,
            ),
        ],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Reanimation Protocols | "
            "Hardwired for Destruction: Trefferwürfe von 1 wiederholen | "
            "Nephrekh: 6+ Invuln"
        ),
        keywords="Infantry, Core, Destroyer Cult, Skorpekh Destroyers",
    ),
    UnitData(
        uid="triarch_stalker",
        name="Triarch Stalker",
        count=1,
        move='10"',
        toughness=6,
        save=3,
        invuln=5,
        fnp=None,
        wounds=12,
        leadership=10,
        oc=3,
        weapons=[
            Weapon("Heat Ray (Dispersed)", "2D6", 1, 5, -1, "1", 'Auto-trifft! Heavy 2D6, 12"'),
            Weapon(
                "Heat Ray (Focused)",
                "2",
                3,
                8,
                -4,
                "D6",
                'Heavy 2, 24"; innerhalb halbe Reichweite: D+D6+2',
            ),
            Weapon(
                "Stalker's Forelimbs",
                "3",
                3,
                7,
                -2,
                "3",
                is_melee=True,
            ),
        ],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Quantum Shielding: 5+ Invuln + unmodif. Wundwürfe 1–3 scheitern immer | "
            "Targeting Relay: nach Treffer → befreundete NECRONS-Modelle wiederholen Trefferwürfe von 1 vs. dasselbe Ziel | "
            "DYNASTIC AGENT (kein Dynastiecode) | "
            'Degradiert: 4–6W: M8"/WS4+/BS4+ | 1–3W: M6"/WS5+/BS5+'
        ),
        keywords="Vehicle, Dynastic Agent, Triarch, Quantum Shielding, Core, Elites",
    ),
    UnitData(
        uid="scarabs",
        name="Canoptek Scarab Swarms ×3",
        count=3,
        move='10"',
        toughness=3,
        save=6,
        invuln=6,
        fnp=None,
        wounds=4,
        leadership=10,
        oc=0,
        weapons=[
            Weapon(
                "Feeder Mandibles",
                "4",
                4,
                3,
                0,
                "1",
                "Unmodif. 6 zum Treffen = automatisch verwundet",
                is_melee=True,
            ),
        ],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Reanimation Protocols | Fly | Nephrekh: 6+ Invuln"
        ),
        keywords="Swarm, Canoptek, Fly, Fast Attack",
    ),
]

# ---------------------------------------------------------------------------
# Ork-Armee – Patrol Detachment (Orks, Bad Moons, 25PL / 470pts / 1CP)
# Clan Kultur: Bad Moons → +1 Angriff bei Schusswaffen wenn keine Bewegung
# ---------------------------------------------------------------------------
ORK_UNITS: list[UnitData] = [
    UnitData(
        uid="big_mek",
        name="Big Mek in Mega Armour",
        count=1,
        move='4"',
        toughness=5,
        save=2,
        invuln=4,
        fnp=None,
        wounds=6,
        leadership=7,
        oc=1,
        weapons=[
            Weapon(
                "Kustom Mega-Blasta",
                "1",
                5,
                8,
                -3,
                "D6",
                'Assault 1, 24"; unmodif. 1 zum Treffen = 1 MV an eigener Einheit',
            ),
            Weapon(
                "Tellyport Blasta",
                "D6",
                5,
                8,
                -3,
                "1",
                'Assault D6, 18"; unmodif. 1 zum Treffen = 1 MV an eigener Einheit',
            ),
        ],
        abilities=(
            "Super Cybork Body: 4+ Invuln | "
            "Grot Oiler: 1×/Spiel einen fehlgeschlagenen Treffer- oder Wundwurf wiederholen | "
            "Stratagem: Big Boss | Stratagem: Extra Gubbinz | "
            "Bad Moons Clan Kultur"
        ),
        keywords="Infantry, Character, Mega Armour, Big Mek, HQ",
    ),
    UnitData(
        uid="warboss",
        name="Warboss in Mega Armour (Warlord)",
        count=1,
        move='4"',
        toughness=5,
        save=2,
        invuln=None,
        fnp=None,
        wounds=7,
        leadership=8,
        oc=1,
        weapons=[
            Weapon(
                "Kustom Shoota",
                "4",
                5,
                4,
                0,
                "1",
                'Assault 4, 18"',
            ),
            Weapon(
                "Boss Klaw",
                "4",
                2,
                10,
                -3,
                "3",
                "S×2 (Profil 5 → 10)",
                is_melee=True,
            ),
        ],
        abilities=(
            "Warlord | Warlord-Trait: Might is Right (wenn dieses Modell kämpft und ein Modell tötet, +1A bis Ende der Phase) | "
            "Da Krushin' Armour (Relikt) | Waaagh! (1×/Spiel: befreundete ORK-Einheiten in 6\" +1 Angriff im Nahkampf)"
        ),
        keywords="Infantry, Character, Mega Armour, Warboss, Warlord, HQ",
    ),
    UnitData(
        uid="boyz",
        name="Boyz ×10",
        count=10,
        move='5"',
        toughness=4,
        save=6,
        invuln=None,
        fnp=None,
        wounds=1,
        leadership=7,
        oc=2,
        weapons=[
            Weapon("Slugga", "1", 5, 4, 0, "1", 'Pistol 1, 12"'),
            Weapon("Shoota", "2", 5, 4, 0, "1", 'Assault 2, 18" (3 Modelle)'),
            Weapon("Big Shoota", "3", 5, 5, 0, "1", 'Assault 3, 36" (1 Modell)'),
            Weapon("Choppa", "2", 3, 4, -1, "1", "S+1 (User→4)", is_melee=True),
            Weapon("Power Klaw (Boss Nob)", "3", 3, 8, -3, "2", "S×2 (4→8)", is_melee=True),
        ],
        abilities=(
            "Mob Rule: statt Moraltest W6 würfeln, bei 1 stirbt 1 Modell zusätzlich, sonst bestanden | "
            "Besetzung: Boss Nob (W2, A3) + 1×Big Shoota + 3×Shoota + 5×Slugga&Choppa | "
            'Stikkbombs: Handgranate 1, 6", S3, AP0, D1'
        ),
        keywords="Infantry, Core, Ork Boyz, Troops",
    ),
    UnitData(
        uid="gretchin",
        name="Gretchin ×10",
        count=10,
        move='5"',
        toughness=2,
        save=6,
        invuln=None,
        fnp=None,
        wounds=1,
        leadership=4,
        oc=1,
        weapons=[
            Weapon("Grot Blasta", "1", 5, 3, 0, "1", 'Pistol 1, 12"'),
        ],
        abilities=(
            "Objective Secured (wenn Runtherd in Reichweite) | "
            'Cowardly (wenn keine befreundete Einheit in 6": automatisch Moraltest fehlgeschlagen)'
        ),
        keywords="Infantry, Gretchin, Troops",
    ),
    UnitData(
        uid="warbikers",
        name="Warbikers ×3",
        count=3,
        move='14"',
        toughness=5,
        save=4,
        invuln=None,
        fnp=None,
        wounds=2,
        leadership=7,
        oc=2,
        weapons=[
            Weapon(
                "Dakkagun ×2",
                "6",
                5,
                5,
                0,
                "1",
                '2× Dakkagun á Assault 3 = 6 Schuss pro Modell, 18"',
            ),
            Weapon("Choppa", "2", 3, 4, -1, "1", "S+1", is_melee=True),
            Weapon("Big Choppa (Boss Nob)", "3", 3, 5, -1, "2", "S+2, Boss Nob", is_melee=True),
        ],
        abilities=(
            "Turbo-Boost: kann Vorstoßen und trotzdem schießen | "
            "Klann Kultur: Bad Moons | "
            "Boss Nob: WS3+, A3, Big Choppa"
        ),
        keywords="Biker, Core, Warbikers, Fast Attack",
    ),
    UnitData(
        uid="mek_gun",
        name="Mek Gun (Kustom Mega Kannon)",
        count=1,
        move='3"',
        toughness=7,
        save=4,
        invuln=None,
        fnp=None,
        wounds=4,
        leadership=4,
        oc=3,
        weapons=[
            Weapon(
                "Kustom Mega Kannon",
                "D6",
                5,
                8,
                -3,
                "D3",
                'Heavy D6, 36"; Blast (min. 3 Angriffe gegen 6+ Modelle)',
            ),
        ],
        abilities=(
            'Artillery | Grot-Crew: wenn Gretchin-Einheit in 3", +1 auf Trefferwürfe | '
            "Schwerfällig: kann nicht Vorstoßen"
        ),
        keywords="Vehicle, Artillery, Mek Gun, Heavy Support",
    ),
]
