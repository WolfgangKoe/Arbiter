from dataclasses import dataclass, field

PHASES: list[tuple[str, str]] = [
    ("Setup", "setup"),
    ("Befehlsphase", "command"),
    ("Bewegungsphase", "movement"),
    ("Psiphase", "psychic"),
    ("Fernkampfphase", "shooting"),
    ("Angriffsphase", "charge"),
    ("Nahkampfphase", "fight"),
    ("Moralphase", "morale"),
]


@dataclass
class Weapon:
    name: str
    attacks: str  # "1", "D6", "2D6", …
    skill: int  # Trefferwert (z.B. 3 = trifft auf 3+)
    strength: int
    ap: int  # 0, -1, -2, … (negativ = rüstungsbrechend)
    damage: str  # "1", "D3", "D6", …
    abilities: str = ""
    is_melee: bool = False


@dataclass
class Unit:
    uid: str
    name: str
    count: int  # Anzahl Modelle
    move: str
    toughness: int
    save: int  # z.B. 3 = Rüstungswurf 3+
    invuln: int | None  # Unverwundbarkeitsrettung oder None
    fnp: int | None  # Feel No Pain oder None
    wounds: int  # Lebenspunkte pro Modell
    leadership: int
    oc: int  # Objective Control
    weapons: list[Weapon]
    faction_keywords: list[str] = field(default_factory=list)
    other_keywords: list[str] = field(default_factory=list)
    abilities: str = ""


# ---------------------------------------------------------------------------
# Zarekhan'Sol – Patrol Detachment (Necrons, Nephrekh, 25PL / 485pts / 3CP)
# ---------------------------------------------------------------------------
NECRON_UNITS: list[Unit] = [
    Unit(
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
            Weapon(
                "Gauntlet of the Conflagrator",
                "1",
                1,
                5,
                0,
                "1",
                "Auto-trifft! Kein Wundwurf: 1W6 pro Modell im Ziel, jede 6 = 1 MV (Rettungswürfe ignoriert)",
            ),
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
        faction_keywords=["Necrons", "Nephrekh"],
        other_keywords=["Infantry", "Character", "Noble", "Overlord", "Warlord"],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Phase Shifter: 4+ Invuln | "
            "Warlord-Trait: Skin of Living Gold (-1 auf Trefferwürfe gegen diesen) | "
            'My Will Be Done: 1 befreundete CORE-Einheit in 9" +1 auf Trefferwürfe | '
            'Relentless March (Aura): befreundete CORE in 6" +1" Bewegung | '
            'Resurrection Orb: 1×/Spiel Reanimation-Protokoll für befreundete Einheit in 6"'
        ),
    ),
    Unit(
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
        faction_keywords=["Necrons", "Nephrekh"],
        other_keywords=["Infantry", "Core", "Necron Warriors"],
        abilities=(
            "Reanimation Protocols | Their Number Is Legion: RP-Würfe von 1 wiederholen | "
            "Objective Secured | Nephrekh: 6+ Invuln"
        ),
    ),
    Unit(
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
        faction_keywords=["Necrons", "Nephrekh"],
        other_keywords=["Infantry", "Core", "Destroyer Cult", "Skorpekh Destroyers"],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Reanimation Protocols | "
            "Hardwired for Destruction: Trefferwürfe von 1 wiederholen | "
            "Nephrekh: 6+ Invuln"
        ),
    ),
    Unit(
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
                "Heat Ray (Focused)", "2", 3, 8, -4, "D6", 'Heavy 2, 24"; halbe Reichweite: D+D6+2'
            ),
            Weapon("Stalker's Forelimbs", "3", 3, 7, -2, "3", is_melee=True),
        ],
        faction_keywords=["Necrons"],
        other_keywords=["Vehicle", "Dynastic Agent", "Triarch", "Quantum Shielding", "Core"],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Quantum Shielding: 5+ Invuln + unmodif. Wundwürfe 1–3 scheitern | "
            "Targeting Relay: nach Treffer → befreundete NECRONS wiederholen Trefferwürfe von 1 vs. dasselbe Ziel | "
            'Degradiert: 4–6W: M8"/WS4+/BS4+ | 1–3W: M6"/WS5+/BS5+'
        ),
    ),
    Unit(
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
        faction_keywords=["Necrons", "Nephrekh"],
        other_keywords=["Swarm", "Canoptek", "Fly"],
        abilities="Living Metal (+1W/Befehlsphase) | Reanimation Protocols | Fly | Nephrekh: 6+ Invuln",
    ),
]

# ---------------------------------------------------------------------------
# Ork-Armee – Patrol Detachment (Orks, Bad Moons, 25PL / 470pts / 1CP)
# ---------------------------------------------------------------------------
ORK_UNITS: list[Unit] = [
    Unit(
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
        faction_keywords=["Orks", "Bad Moons"],
        other_keywords=["Infantry", "Character", "Mega Armour", "Big Mek"],
        abilities=(
            "Super Cybork Body: 4+ Invuln | "
            "Grot Oiler: 1×/Spiel einen fehlgeschlagenen Treffer- oder Wundwurf wiederholen | "
            "Stratagem: Big Boss | Stratagem: Extra Gubbinz"
        ),
    ),
    Unit(
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
            Weapon("Kustom Shoota", "4", 5, 4, 0, "1", 'Assault 4, 18"'),
            Weapon("Boss Klaw", "4", 2, 10, -3, "3", "S×2 (Profil 5 → 10)", is_melee=True),
        ],
        faction_keywords=["Orks", "Bad Moons"],
        other_keywords=["Infantry", "Character", "Mega Armour", "Warboss", "Warlord"],
        abilities=(
            "Warlord-Trait: Might is Right (tötet Modell → +1A bis Ende Phase) | "
            "Da Krushin' Armour (Relikt) | "
            'Waaagh! (1×/Spiel: befreundete ORK in 6" +1 Angriff im Nahkampf)'
        ),
    ),
    Unit(
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
        faction_keywords=["Orks", "Bad Moons"],
        other_keywords=["Infantry", "Core", "Ork Boyz"],
        abilities=(
            "Mob Rule: statt Moraltest W6, bei 1 stirbt 1 Modell zusätzlich, sonst bestanden | "
            "Besetzung: Boss Nob (W2, A3) + 1×Big Shoota + 3×Shoota + 5×Slugga&Choppa | "
            'Stikkbombs: Handgranate 1, 6", S3, AP0, D1'
        ),
    ),
    Unit(
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
        faction_keywords=["Orks"],
        other_keywords=["Infantry", "Gretchin"],
        abilities=(
            "Objective Secured (wenn Runtherd in Reichweite) | "
            'Cowardly (keine befreundete Einheit in 6" → Moraltest automatisch fehlgeschlagen)'
        ),
    ),
    Unit(
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
        faction_keywords=["Orks", "Bad Moons"],
        other_keywords=["Biker", "Core", "Warbikers"],
        abilities=(
            "Turbo-Boost: kann Vorstoßen und trotzdem schießen | " "Boss Nob: WS3+, A3, Big Choppa"
        ),
    ),
    Unit(
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
        faction_keywords=["Orks", "Bad Moons"],
        other_keywords=["Vehicle", "Artillery", "Mek Gun"],
        abilities=(
            'Artillery | Grot-Crew: Gretchin in 3" → +1 auf Trefferwürfe | '
            "Schwerfällig: kann nicht Vorstoßen"
        ),
    ),
]
