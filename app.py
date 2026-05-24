import streamlit as st
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

st.set_page_config(
    page_title="WH40k 9th Ed. – Battle Tracker",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .stProgress > div > div { border-radius: 4px; }
    div[data-testid="metric-container"] { background: #1e1e2e; border-radius: 8px; padding: 8px; }
    .phase-box { background: #12122a; border: 2px solid #4444aa; border-radius: 10px; padding: 16px; margin-bottom: 10px; }
    .log-area { font-family: monospace; font-size: 12px; }
    h2 { margin-top: 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Weapon:
    name: str
    attacks: str       # "1", "D6", "2D6", etc.
    skill: int         # target number (e.g. 3 means hits on 3+)
    strength: int
    ap: int            # 0, -1, -2, … (negative = armour-piercing)
    damage: str        # "1", "D3", "D6", etc.
    abilities: str = ""
    is_melee: bool = False


@dataclass
class UnitData:
    uid: str
    name: str
    count: int         # number of models
    move: str
    toughness: int
    save: int          # e.g. 3 means 3+
    invuln: Optional[int]   # invulnerable save value or None
    fnp: Optional[int]      # feel-no-pain value or None
    wounds: int        # wounds per model
    leadership: int
    oc: int
    weapons: List[Weapon]
    abilities: str = ""
    keywords: str = ""


# ---------------------------------------------------------------------------
# Army lists
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Zarekhan'Sol – Patrol Detachment (Necrons, Nephrekh, 25PL / 485pts / 3CP)
# Dynastic Code: Translocation Beams → alle Einheiten mit Dynastiecode: 6+ Invuln
# ---------------------------------------------------------------------------
NECRON_UNITS: List[UnitData] = [
    UnitData(
        uid="overlord",
        name="Overlord (Warlord)",
        count=1, move='6"', toughness=5, save=3, invuln=4, fnp=None,
        wounds=5, leadership=10, oc=1,
        weapons=[
            # Gauntlet: auto-hits (skill=1); statt Wund-Roll → D6 pro Modell, 6er = 1 MV
            Weapon(
                "Gauntlet of the Conflagrator", "1", 1, 5, 0, "1",
                "Auto-trifft! Kein Wundwurf: 1W6 pro Modell im Ziel, jede 6 = 1 MV (Rettungswürfe ignoriert)",
            ),
            # Voidscythe: S×2=10, AP-4, D3; -1 zum Treffen bereits eingerechnet (WS2+→3+)
            Weapon(
                "Voidscythe", "4", 3, 10, -4, "3",
                "-1 zum Trefferwurf (bereits eingerechnet: WS2+ → 3+)",
                is_melee=True,
            ),
        ],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Phase Shifter: 4+ Invuln | "
            "Warlord-Trait: Skin of Living Gold (-1 auf Trefferwürfe gegen diesen) | "
            "My Will Be Done: 1 befreundete CORE-Einheit in 9\" +1 auf Trefferwürfe | "
            "Relentless March (Aura): befreundete CORE in 6\" +1\" Bewegung | "
            "Resurrection Orb: 1×/Spiel Reanimation-Protokoll für befreundete Einheit in 6\""
        ),
        keywords="Infantry, Character, Noble, Overlord, Warlord",
    ),
    UnitData(
        uid="warriors",
        name="Necron Warriors ×10",
        count=10, move='5"', toughness=4, save=4, invuln=6, fnp=None,
        wounds=1, leadership=10, oc=2,
        weapons=[
            Weapon("Gauss Reaper", "2", 3, 5, -2, "1", "Assault 2, 12\""),
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
        count=3, move='8"', toughness=5, save=3, invuln=6, fnp=None,
        wounds=3, leadership=10, oc=2,
        weapons=[
            # 1 Modell: Reap-Blade; 2 Modelle: Threshers (beide wählbar)
            Weapon(
                "Hyperphase Reap-Blade", "3", 3, 7, -4, "3",
                "1 Modell (S: Profil+2=7)", is_melee=True,
            ),
            Weapon(
                "Hyperphase Threshers", "4", 3, 5, -3, "2",
                "2 Modelle; +1 Angriff des Trägers pro Kampf", is_melee=True,
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
        count=1, move='10"', toughness=6, save=3, invuln=5, fnp=None,
        wounds=12, leadership=10, oc=3,
        weapons=[
            # Auto-trifft → skill=1
            Weapon(
                "Heat Ray (Dispersed)", "2D6", 1, 5, -1, "1",
                "Auto-trifft! Heavy 2D6, 12\""
            ),
            Weapon(
                "Heat Ray (Focused)", "2", 3, 8, -4, "D6",
                "Heavy 2, 24\"; innerhalb halbe Reichweite: D+D6+2"
            ),
            Weapon(
                "Stalker's Forelimbs", "3", 3, 7, -2, "3",
                is_melee=True,
            ),
        ],
        abilities=(
            "Living Metal (+1W/Befehlsphase) | Quantum Shielding: 5+ Invuln + unmodif. Wundwürfe 1–3 scheitern immer | "
            "Targeting Relay: nach Treffer → befreundete NECRONS-Modelle wiederholen Trefferwürfe von 1 vs. dasselbe Ziel | "
            "DYNASTIC AGENT (kein Dynastiecode) | "
            "Degradiert: 4–6W: M8\"/WS4+/BS4+ | 1–3W: M6\"/WS5+/BS5+"
        ),
        keywords="Vehicle, Dynastic Agent, Triarch, Quantum Shielding, Core, Elites",
    ),
    UnitData(
        uid="scarabs",
        name="Canoptek Scarab Swarms ×3",
        count=3, move='10"', toughness=3, save=6, invuln=6, fnp=None,
        wounds=4, leadership=10, oc=0,
        weapons=[
            Weapon(
                "Feeder Mandibles", "4", 4, 3, 0, "1",
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
ORK_UNITS: List[UnitData] = [
    UnitData(
        uid="big_mek",
        name="Big Mek in Mega Armour",
        count=1, move='4"', toughness=5, save=2, invuln=4, fnp=None,
        wounds=6, leadership=7, oc=1,
        weapons=[
            Weapon(
                "Kustom Mega-Blasta", "1", 5, 8, -3, "D6",
                "Assault 1, 24\"; unmodif. 1 zum Treffen = 1 MV an eigener Einheit",
            ),
            Weapon(
                "Tellyport Blasta", "D6", 5, 8, -3, "1",
                "Assault D6, 18\"; unmodif. 1 zum Treffen = 1 MV an eigener Einheit",
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
        count=1, move='4"', toughness=5, save=2, invuln=None, fnp=None,
        wounds=7, leadership=8, oc=1,
        weapons=[
            Weapon(
                "Kustom Shoota", "4", 5, 4, 0, "1",
                "Assault 4, 18\"",
            ),
            Weapon(
                "Boss Klaw", "4", 2, 10, -3, "3",
                "S×2 (Profil 5 → 10)", is_melee=True,
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
        count=10, move='5"', toughness=4, save=6, invuln=None, fnp=None,
        wounds=1, leadership=7, oc=2,
        weapons=[
            Weapon("Slugga", "1", 5, 4, 0, "1", "Pistol 1, 12\""),
            Weapon("Shoota", "2", 5, 4, 0, "1", "Assault 2, 18\" (3 Modelle)"),
            Weapon("Big Shoota", "3", 5, 5, 0, "1", "Assault 3, 36\" (1 Modell)"),
            Weapon("Choppa", "2", 3, 4, -1, "1", "S+1 (User→4)", is_melee=True),
            Weapon("Power Klaw (Boss Nob)", "3", 3, 8, -3, "2", "S×2 (4→8)", is_melee=True),
        ],
        abilities=(
            "Mob Rule: statt Moraltest W6 würfeln, bei 1 stirbt 1 Modell zusätzlich, sonst bestanden | "
            "Besetzung: Boss Nob (W2, A3) + 1×Big Shoota + 3×Shoota + 5×Slugga&Choppa | "
            "Stikkbombs: Handgranate 1, 6\", S3, AP0, D1"
        ),
        keywords="Infantry, Core, Ork Boyz, Troops",
    ),
    UnitData(
        uid="gretchin",
        name="Gretchin ×10",
        count=10, move='5"', toughness=2, save=6, invuln=None, fnp=None,
        wounds=1, leadership=4, oc=1,
        weapons=[
            Weapon("Grot Blasta", "1", 5, 3, 0, "1", "Pistol 1, 12\""),
        ],
        abilities=(
            "Objective Secured (wenn Runtherd in Reichweite) | "
            "Cowardly (wenn keine befreundete Einheit in 6\": automatisch Moraltest fehlgeschlagen)"
        ),
        keywords="Infantry, Gretchin, Troops",
    ),
    UnitData(
        uid="warbikers",
        name="Warbikers ×3",
        count=3, move='14"', toughness=5, save=4, invuln=None, fnp=None,
        wounds=2, leadership=7, oc=2,
        weapons=[
            # 2 Dakkaguns pro Modell → 6 Schuss pro Modell
            Weapon(
                "Dakkagun ×2", "6", 5, 5, 0, "1",
                "2× Dakkagun á Assault 3 = 6 Schuss pro Modell, 18\""
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
        count=1, move='3"', toughness=7, save=4, invuln=None, fnp=None,
        wounds=4, leadership=4, oc=3,
        weapons=[
            Weapon(
                "Kustom Mega Kannon", "D6", 5, 8, -3, "D3",
                "Heavy D6, 36\"; Blast (min. 3 Angriffe gegen 6+ Modelle)",
            ),
        ],
        abilities=(
            "Artillery | Grot-Crew: wenn Gretchin-Einheit in 3\", +1 auf Trefferwürfe | "
            "Schwerfällig: kann nicht Vorstoßen"
        ),
        keywords="Vehicle, Artillery, Mek Gun, Heavy Support",
    ),
]

PHASES = [
    ("⚔️  Befehlsphase",    "command"),
    ("🏃  Bewegungsphase",   "movement"),
    ("🔮  Psiphase",         "psychic"),
    ("🎯  Schussphase",      "shooting"),
    ("💨  Sturmphase",       "charge"),
    ("👊  Kampfphase",       "fight"),
    ("😱  Moralphase",       "morale"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_dice(s: str) -> int:
    s = str(s).upper().strip()
    if "D" in s:
        parts = s.split("D")
        mult = int(parts[0]) if parts[0] else 1
        sides = int(parts[1])
        return sum(random.randint(1, sides) for _ in range(mult))
    return int(s)


def wound_threshold(strength: int, toughness: int) -> int:
    if strength >= toughness * 2:
        return 2
    if strength > toughness:
        return 3
    if strength == toughness:
        return 4
    if strength * 2 <= toughness:
        return 6
    return 5


def resolve_attack(
    attacker: UnitData, atk_state: dict,
    weapon: Weapon,
    defender: UnitData, def_state: dict,
    num_models: int,
) -> Tuple[int, List[str]]:
    msgs: List[str] = []
    total_attacks = parse_dice(weapon.attacks) * num_models
    skill_label = "WS" if weapon.is_melee else "BS"
    msgs.append(
        f"**{attacker.name}** → **{weapon.name}** → **{defender.name}** "
        f"({num_models} Modelle, {total_attacks} Angriffe)"
    )

    # Roll to hit
    hit_rolls = [random.randint(1, 6) for _ in range(total_attacks)]
    hits = sum(1 for r in hit_rolls if r >= weapon.skill)
    msgs.append(f"Trefferwürfe ({skill_label}{weapon.skill}+): {hit_rolls} → **{hits} Treffer**")
    if hits == 0:
        msgs.append("Keine Treffer!")
        return 0, msgs

    # Roll to wound
    thresh = wound_threshold(weapon.strength, defender.toughness)
    wound_rolls = [random.randint(1, 6) for _ in range(hits)]
    wounds = sum(1 for r in wound_rolls if r >= thresh)
    msgs.append(f"Verwundungswürfe (S{weapon.strength} vs T{defender.toughness}, brauche {thresh}+): {wound_rolls} → **{wounds} Verwundungen**")
    if wounds == 0:
        msgs.append("Keine Verwundungen!")
        return 0, msgs

    # Saves (armour, then invuln if better)
    armour_save = defender.save + abs(weapon.ap)
    effective_save = armour_save
    if defender.invuln and defender.invuln < effective_save:
        effective_save = defender.invuln
        msgs.append(f"Rüstungswurf durch AP{weapon.ap} auf {armour_save}+, Unverwundbarkeitsrettung {defender.invuln}+ greift")
    else:
        msgs.append(f"Rüstungswurf: {defender.save}+ mit AP{weapon.ap} → effektiv {effective_save}+")

    if effective_save > 6:
        failed = wounds
        msgs.append("Keine Rettung möglich!")
    else:
        save_rolls = [random.randint(1, 6) for _ in range(wounds)]
        failed = sum(1 for r in save_rolls if r < effective_save)
        msgs.append(f"Rettungswürfe ({effective_save}+): {save_rolls} → **{failed} fehlgeschlagen**")

    if failed == 0:
        msgs.append("Alle Rettungswürfe erfolgreich!")
        return 0, msgs

    # Feel No Pain
    if defender.fnp:
        fnp_rolls = [random.randint(1, 6) for _ in range(failed)]
        survived = sum(1 for r in fnp_rolls if r >= defender.fnp)
        failed -= survived
        msgs.append(f"Feel No Pain ({defender.fnp}+): {fnp_rolls} → {survived} gerettet, noch {failed} übrig")

    # Damage
    total_dmg = sum(parse_dice(weapon.damage) for _ in range(failed))
    msgs.append(f"**⚠️ {total_dmg} Schaden verursacht!**")
    return total_dmg, msgs


def apply_damage(uid: str, faction: str, dmg: int, unit: UnitData):
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    state["current_wounds"] = max(0, state["current_wounds"] - dmg)
    # Recalculate models
    if unit.wounds > 0:
        full_models = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.count, full_models + partial)
    if state["current_wounds"] <= 0:
        state["destroyed"] = True
        state["current_wounds"] = 0
        state["models"] = 0


def heal_unit(uid: str, faction: str, hp: int, unit: UnitData):
    key = "necron_units" if faction == "Necrons" else "ork_units"
    state = st.session_state[key][uid]
    max_hp = unit.wounds * unit.count
    state["current_wounds"] = min(max_hp, state["current_wounds"] + hp)
    state["destroyed"] = state["current_wounds"] <= 0
    if unit.wounds > 0:
        full = state["current_wounds"] // unit.wounds
        partial = 1 if state["current_wounds"] % unit.wounds > 0 else 0
        state["models"] = min(unit.count, full + partial)


def add_log(msg: str):
    st.session_state.battle_log.append(msg)
    if len(st.session_state.battle_log) > 60:
        st.session_state.battle_log = st.session_state.battle_log[-60:]


# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------

def init_state():
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.phase_idx = 0
    st.session_state.active = "Necrons"
    st.session_state.battle_log = ["=== Spiel gestartet! ===", "⚔️ Befehlsphase – Necrons Runde 1"]
    st.session_state.cp = {"Necrons": 3, "Orks": 3}
    st.session_state.vp = {"Necrons": 0, "Orks": 0}

    def unit_state(u: UnitData):
        return {
            "current_wounds": u.wounds * u.count,
            "models": u.count,
            "destroyed": False,
        }

    st.session_state.necron_units = {u.uid: unit_state(u) for u in NECRON_UNITS}
    st.session_state.ork_units = {u.uid: unit_state(u) for u in ORK_UNITS}


def reset_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]


# ---------------------------------------------------------------------------
# UI: unit card
# ---------------------------------------------------------------------------

def unit_card(unit: UnitData, state: dict, faction: str):
    destroyed = state["destroyed"]
    cur = state["current_wounds"]
    total = unit.wounds * unit.count
    models = state["models"]
    color = "#00ff88" if faction == "Necrons" else "#aaee00"
    if destroyed:
        color = "#555"

    title = f"~~{unit.name}~~" if destroyed else unit.name
    subtitle = "💀 VERNICHTET" if destroyed else f"❤️ {cur}/{total} LP  ({models}/{unit.count} Modelle)"

    with st.expander(f"{title}  —  {subtitle}", expanded=not destroyed):
        if destroyed:
            return

        # Stats row
        sc = st.columns(7)
        for col, lbl, val in zip(
            sc,
            ["M", "T", "Ret", "W", "FU", "LD", "OC"],
            [
                unit.move,
                unit.toughness,
                f"{unit.save}+",
                unit.wounds,
                f"{unit.invuln}+" if unit.invuln else "–",
                unit.leadership,
                unit.oc,
            ],
        ):
            col.metric(lbl, val)

        # Wound bar
        if total > 0:
            st.progress(cur / total)

        # Adjust wounds
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("−1", key=f"w1_{faction}_{unit.uid}", help="1 Wunde abziehen"):
                apply_damage(unit.uid, faction, 1, unit)
                add_log(f"⚔️ {unit.name} –1 Wunde ({state['current_wounds']-1}/{total})")
                st.rerun()
        with c2:
            if st.button("−D3", key=f"wd3_{faction}_{unit.uid}", help="D3 Wunden abziehen"):
                d = random.randint(1, 3)
                apply_damage(unit.uid, faction, d, unit)
                add_log(f"⚔️ {unit.name} –{d} Wunden")
                st.rerun()
        with c3:
            if st.button("−D6", key=f"wd6_{faction}_{unit.uid}", help="D6 Wunden abziehen"):
                d = random.randint(1, 6)
                apply_damage(unit.uid, faction, d, unit)
                add_log(f"⚔️ {unit.name} –{d} Wunden")
                st.rerun()
        with c4:
            if st.button("+1", key=f"h1_{faction}_{unit.uid}", help="1 Wunde heilen"):
                heal_unit(unit.uid, faction, 1, unit)
                add_log(f"💚 {unit.name} +1 Wunde geheilt")
                st.rerun()

        # Weapons
        st.caption(f"**Waffen:**")
        for w in unit.weapons:
            icon = "⚔️" if w.is_melee else "🎯"
            ap_str = f"AP{w.ap}" if w.ap != 0 else "AP0"
            st.caption(
                f"{icon} **{w.name}** | A{w.attacks} | "
                f"{'WS' if w.is_melee else 'BS'}{w.skill}+ | S{w.strength} | "
                f"{ap_str} | D{w.damage}"
                + (f" | _{w.abilities}_" if w.abilities else "")
            )

        if unit.abilities:
            st.caption(f"*Fähigkeiten: {unit.abilities}*")


# ---------------------------------------------------------------------------
# UI: phases
# ---------------------------------------------------------------------------

def phase_command():
    active = st.session_state.active
    st.info(
        "**Befehlsphase:** Erhalte 1 Befehlspunkt. Aktiviere Fähigkeiten. Nutze Strategeme."
    )
    c1, c2 = st.columns(2)
    with c1:
        st.metric(f"CP {active}", st.session_state.cp[active])
        if st.button("➕ 1 CP erhalten", key="add_cp"):
            st.session_state.cp[active] += 1
            add_log(f"🎖️ {active} erhält 1 CP (jetzt {st.session_state.cp[active]})")
            st.rerun()
    with c2:
        strat = st.text_input("Strategem-Name:", key="strat_name")
        cost = st.number_input("CP-Kosten:", 1, 3, 1, key="strat_cost")
        if st.button("Strategem einsetzen", key="use_strat"):
            if st.session_state.cp[active] >= cost:
                st.session_state.cp[active] -= cost
                add_log(f"🃏 {active} setzt '{strat or 'Strategem'}' ein (–{cost} CP)")
                st.rerun()
            else:
                st.error("Nicht genug CP!")

    st.divider()
    st.subheader("Siegpunkte")
    vc1, vc2, vc3, vc4 = st.columns(4)
    with vc1:
        if st.button("Necrons +1 VP"):
            st.session_state.vp["Necrons"] += 1
            add_log("🔵 Necrons +1 VP")
            st.rerun()
    with vc2:
        st.metric("Necrons VP", st.session_state.vp["Necrons"])
    with vc3:
        st.metric("Orks VP", st.session_state.vp["Orks"])
    with vc4:
        if st.button("Orks +1 VP"):
            st.session_state.vp["Orks"] += 1
            add_log("🟢 Orks +1 VP")
            st.rerun()


def phase_movement():
    active = st.session_state.active
    units = NECRON_UNITS if active == "Necrons" else ORK_UNITS
    states = st.session_state.necron_units if active == "Necrons" else st.session_state.ork_units

    st.info(
        "**Bewegungsphase:** Normal bewegen (bis M\"), Vorstoßen (+D6\", kein Schießen/Sturm), "
        "Zurückweichen (kein Schießen/Sturm)."
    )
    alive = [(u, states[u.uid]) for u in units if not states[u.uid]["destroyed"]]
    if not alive:
        st.warning("Keine Einheiten mehr!")
        return

    sel = st.selectbox("Einheit auswählen:", [u.name for u, _ in alive], key="mv_sel")
    unit, state = next((u, s) for u, s in alive if u.name == sel)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚶 Normal bewegen", key="mv_normal"):
            add_log(f"🏃 {unit.name} bewegt sich normal (bis {unit.move})")
            st.rerun()
    with c2:
        if st.button("💨 Vorstoßen", key="mv_advance"):
            adv = random.randint(1, 6)
            add_log(f"💨 {unit.name} stößt vor: +{adv}\" (kein Schießen/Sturm)")
            st.rerun()
    with c3:
        if st.button("🏃 Zurückweichen", key="mv_fallback"):
            add_log(f"🏳️ {unit.name} weicht zurück! (kein Schießen/Sturm)")
            st.rerun()


def phase_psychic():
    active = st.session_state.active
    if active == "Necrons":
        st.info("Die Necrons in dieser Liste haben keine Psyker. Psiphase überspringen.")
        return
    st.info(
        "**Psiphase:** Würfle 2W6 für den psychischen Test. "
        "Ergebnis muss ≥ Psi-Stärke sein. Gegner kann mit 2W6 abwehren."
    )
    col1, col2 = st.columns(2)
    with col1:
        power = st.text_input("Psikraft:", "Fists of Gork", key="psi_power")
        charge = st.number_input("Psi-Stärke:", 1, 9, 7, key="psi_charge")
        if st.button("🔮 Psikraft einsetzen", key="psi_cast"):
            rolls = [random.randint(1, 6) for _ in range(2)]
            total = sum(rolls)
            ok = total >= charge
            result = "✅ ERFOLG" if ok else "❌ FEHLGESCHLAGEN"
            add_log(f"🔮 {power}: {rolls} = {total} vs {charge} → {result}")
            if ok:
                st.success(f"{power} wirkt! ({total} ≥ {charge})")
            else:
                st.error(f"{power} scheitert! ({total} < {charge})")
    with col2:
        if st.button("🛡️ Abwehren", key="psi_deny"):
            rolls = [random.randint(1, 6) for _ in range(2)]
            total = sum(rolls)
            add_log(f"🛡️ Abwehrversuch: {rolls} = {total}")
            st.info(f"Abwehrwurf: {total}")


def _shooting_ui(label_prefix: str, attacker_faction: str, defender_faction: str,
                 is_melee: bool = False):
    phase_label = "Nahkampf" if is_melee else "Schuss"
    attacker_units = NECRON_UNITS if attacker_faction == "Necrons" else ORK_UNITS
    defender_units = ORK_UNITS if attacker_faction == "Necrons" else NECRON_UNITS
    atk_states = st.session_state.necron_units if attacker_faction == "Necrons" else st.session_state.ork_units
    def_states = st.session_state.ork_units if attacker_faction == "Necrons" else st.session_state.necron_units

    alive_atk = [(u, atk_states[u.uid]) for u in attacker_units if not atk_states[u.uid]["destroyed"]]
    alive_def = [(u, def_states[u.uid]) for u in defender_units if not def_states[u.uid]["destroyed"]]

    if not alive_atk or not alive_def:
        st.warning("Keine gültigen Einheiten für diesen Angriff!")
        return

    # Filter for ranged / melee weapons
    if is_melee:
        viable_atk = [(u, s) for u, s in alive_atk if any(w.is_melee for w in u.weapons)]
    else:
        viable_atk = [(u, s) for u, s in alive_atk if any(not w.is_melee for w in u.weapons)]

    if not viable_atk:
        st.warning(f"Keine Einheiten mit {'Nah-' if is_melee else 'Fern-'}kampfwaffen!")
        return

    col1, col2 = st.columns(2)
    with col1:
        atk_sel = st.selectbox(
            f"Angreifer ({attacker_faction}):",
            [u.name for u, _ in viable_atk],
            key=f"{label_prefix}_atk",
        )
    with col2:
        def_sel = st.selectbox(
            f"Ziel ({defender_faction}):",
            [u.name for u, _ in alive_def],
            key=f"{label_prefix}_def",
        )

    atk_unit = next(u for u, _ in viable_atk if u.name == atk_sel)
    def_unit = next(u for u, _ in alive_def if u.name == def_sel)
    atk_state = atk_states[atk_unit.uid]

    weapons = [w for w in atk_unit.weapons if w.is_melee == is_melee] or atk_unit.weapons
    w_sel = st.selectbox("Waffe:", [w.name for w in weapons], key=f"{label_prefix}_wpn")
    weapon = next(w for w in weapons if w.name == w_sel)

    max_models = max(1, atk_state["models"])
    if max_models > 1:
        num = st.slider("Anzahl angreifender Modelle:", 1, max_models, max_models, key=f"{label_prefix}_num")
    else:
        num = 1
        st.caption("1 Modell verbleibt — greift mit allen Modellen an.")

    btn_label = f"⚔️ ANGREIFEN!" if is_melee else "🎯 SCHIESSEN!"
    if st.button(btn_label, type="primary", key=f"{label_prefix}_go"):
        dmg, msgs = resolve_attack(atk_unit, atk_state, weapon, def_unit,
                                   def_states[def_unit.uid], num)
        for m in msgs:
            add_log(m)
        if dmg > 0:
            apply_damage(def_unit.uid, defender_faction, dmg, def_unit)
            st.success(f"**{dmg} Schaden** an {def_unit.name}!")
        else:
            st.info("Kein Schaden verursacht.")
        st.rerun()


def phase_shooting():
    active = st.session_state.active
    defender = "Orks" if active == "Necrons" else "Necrons"
    st.info(
        "**Schussphase:** Wähle eine Einheit → Waffe → Ziel. "
        "Würfle Treffer (BS), Verwundung (S vs T), Rettung (SV–AP), dann Schaden."
    )
    _shooting_ui("shoot", active, defender, is_melee=False)


def phase_charge():
    active = st.session_state.active
    defender = "Orks" if active == "Necrons" else "Necrons"
    atk_units = NECRON_UNITS if active == "Necrons" else ORK_UNITS
    def_units = ORK_UNITS if active == "Necrons" else NECRON_UNITS
    atk_states = st.session_state.necron_units if active == "Necrons" else st.session_state.ork_units
    def_states = st.session_state.ork_units if active == "Necrons" else st.session_state.necron_units

    st.info(
        "**Sturmphase:** Erkläre Sturm gegen Ziel innerhalb 12\". "
        "Würfle 2W6: Ergebnis muss ≥ Entfernung (in Zoll) sein. "
        "Verteidiger kann Überraschungsfeuer einsetzen (trifft auf 5+)."
    )

    alive_atk = [(u, atk_states[u.uid]) for u in atk_units if not atk_states[u.uid]["destroyed"]]
    alive_def = [(u, def_states[u.uid]) for u in def_units if not def_states[u.uid]["destroyed"]]

    if not alive_atk or not alive_def:
        st.warning("Keine Einheiten für die Sturmphase!")
        return

    col1, col2 = st.columns(2)
    with col1:
        charger_sel = st.selectbox(f"Stürmende Einheit ({active}):",
                                   [u.name for u, _ in alive_atk], key="chg_unit")
    with col2:
        target_sel = st.selectbox(f"Ziel ({defender}):",
                                  [u.name for u, _ in alive_def], key="chg_target")

    dist = st.number_input("Entfernung zum Ziel (Zoll):", 1, 12, 6, key="chg_dist")

    charger = next(u for u, _ in alive_atk if u.name == charger_sel)
    target = next(u for u, _ in alive_def if u.name == target_sel)
    target_state = def_states[target.uid]

    col_ow, col_ch = st.columns(2)
    with col_ow:
        if st.button("⚡ Überraschungsfeuer!", key="overwatch"):
            ranged = [w for w in target.weapons if not w.is_melee]
            if ranged:
                w = ranged[0]
                n = parse_dice(w.attacks) * target_state["models"]
                rolls = [random.randint(1, 6) for _ in range(n)]
                hits = sum(1 for r in rolls if r >= 5)
                add_log(f"⚡ Überraschungsfeuer {target.name} mit {w.name}: {rolls} → {hits} Treffer (trifft auf 5+)")
                if hits:
                    st.warning(f"Überraschungsfeuer: **{hits} Treffer!**")
                else:
                    st.info("Überraschungsfeuer: keine Treffer.")
            else:
                st.info(f"{target.name} hat keine Fernkampfwaffen.")

    with col_ch:
        if st.button("💨 STURM!", type="primary", key="do_charge"):
            rolls = [random.randint(1, 6) for _ in range(2)]
            total = sum(rolls)
            ok = total >= dist
            result = "✅ STURM ERFOLGREICH" if ok else "❌ STURM GESCHEITERT"
            add_log(f"💨 {charger_sel} stürmt: {rolls} = {total} vs {dist}\" → {result}")
            if ok:
                st.success(f"Sturm erfolgreich! ({total} ≥ {dist}\")")
            else:
                st.error(f"Sturm gescheitert! ({total} < {dist}\")")


def phase_fight():
    active = st.session_state.active
    defender = "Orks" if active == "Necrons" else "Necrons"
    st.info(
        "**Kampfphase:** Einheiten die gestürmt haben kämpfen zuerst. "
        "Wähle Waffe und Ziel, würfle WS-Treffer, Verwundung, Rettungswürfe und Schaden."
    )
    _shooting_ui("fight", active, defender, is_melee=True)

    # Defender strikes back
    st.divider()
    st.subheader(f"↩️ Gegenangriff ({defender})")
    _shooting_ui("fight_back", defender, active, is_melee=True)


def phase_morale():
    active = st.session_state.active
    # Defender tests morale (units that took losses)
    defender = "Orks" if active == "Necrons" else "Necrons"
    def_units = ORK_UNITS if active == "Necrons" else NECRON_UNITS
    def_states = st.session_state.ork_units if active == "Necrons" else st.session_state.necron_units

    st.info(
        "**Moralphase:** Einheiten die Modelle verloren haben müssen einen Moraltest bestehen. "
        "Würfle W6, addiere Ergebnis zu verbleibenden Modellen. "
        "Unterschreitet das Ergebnis den Führungswert, verliert die Einheit weitere Modelle."
    )

    alive = [(u, def_states[u.uid]) for u in def_units if not def_states[u.uid]["destroyed"]]
    if not alive:
        st.info("Keine Einheiten für Moraltests.")
        return

    sel = st.selectbox(f"Einheit testen ({defender}):", [u.name for u, _ in alive], key="mor_sel")
    unit, state = next((u, s) for u, s in alive if u.name == sel)
    models = state["models"]
    st.markdown(f"**{unit.name}** — {models} Modelle, Führung {unit.leadership}")

    if st.button("🎲 Moraltest würfeln", key="mor_roll"):
        roll = random.randint(1, 6)
        total = roll + models
        if total >= unit.leadership:
            add_log(
                f"😤 {unit.name} besteht Moraltest! ({roll}+{models}={total} ≥ LD{unit.leadership})"
            )
            st.success(f"Moraltest bestanden! ({roll}+{models}={total} ≥ LD{unit.leadership})")
        else:
            diff = unit.leadership - total
            add_log(
                f"😱 {unit.name} VERSAGT Moraltest! –{diff} Modelle ({roll}+{models}={total} < LD{unit.leadership})"
            )
            apply_damage(unit.uid, defender, diff * unit.wounds, unit)
            st.error(f"Moraltest versagt! {diff} weitere Modelle verloren!")
            st.rerun()


PHASE_RENDERERS = {
    "command":  phase_command,
    "movement": phase_movement,
    "psychic":  phase_psychic,
    "shooting": phase_shooting,
    "charge":   phase_charge,
    "fight":    phase_fight,
    "morale":   phase_morale,
}


def next_phase():
    st.session_state.phase_idx += 1
    if st.session_state.phase_idx >= len(PHASES):
        st.session_state.phase_idx = 0
        if st.session_state.active == "Necrons":
            st.session_state.active = "Orks"
            add_log(f"--- Orks Runde {st.session_state.round} ---")
        else:
            st.session_state.active = "Necrons"
            st.session_state.round += 1
            st.session_state.cp["Necrons"] += 1
            st.session_state.cp["Orks"] += 1
            add_log(f"=== RUNDE {st.session_state.round} beginnt! (je +1 CP) ===")
    phase_name, _ = PHASES[st.session_state.phase_idx]
    add_log(f"📍 {phase_name} – {st.session_state.active}")


# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------

def main():
    init_state()

    st.title("⚔️ Warhammer 40k – 9. Edition Battle Tracker")

    # Header scoreboard
    h1, h2, h3, h4, h5, h6 = st.columns(6)
    h1.metric("Runde", st.session_state.round)
    h2.metric("Necrons VP", st.session_state.vp["Necrons"])
    h3.metric("Necrons CP", st.session_state.cp["Necrons"])
    h4.metric("Orks CP", st.session_state.cp["Orks"])
    h5.metric("Orks VP", st.session_state.vp["Orks"])
    h6.metric("Aktiver Spieler", st.session_state.active)

    st.divider()

    # Three-column layout
    left, center, right = st.columns([1, 2, 1], gap="medium")

    # ── LEFT: Orks ──────────────────────────────────────────────────────────
    with left:
        st.markdown("## 🟢 ORKS")
        for unit in ORK_UNITS:
            unit_card(unit, st.session_state.ork_units[unit.uid], "Orks")

    # ── CENTER: Phases ───────────────────────────────────────────────────────
    with center:
        phase_name, phase_key = PHASES[st.session_state.phase_idx]

        # Phase stepper
        steps_html = ""
        for i, (pn, _) in enumerate(PHASES):
            if i == st.session_state.phase_idx:
                steps_html += f'<span style="background:#3355cc;border-radius:4px;padding:2px 6px;margin:2px;font-size:12px;">{pn}</span>'
            else:
                steps_html += f'<span style="color:#666;font-size:12px;margin:2px;">{pn}</span>'
        st.markdown(steps_html, unsafe_allow_html=True)
        st.divider()

        st.markdown(f"## {phase_name}")
        st.markdown(f"**Aktiver Spieler:** {st.session_state.active}")
        st.markdown("")

        PHASE_RENDERERS[phase_key]()

        st.divider()
        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            if st.button("◀ Vorherige Phase", key="prev_phase"):
                st.session_state.phase_idx = max(0, st.session_state.phase_idx - 1)
                st.rerun()
        with nav2:
            if st.button("🔄 Spiel zurücksetzen", key="reset_game", type="secondary"):
                reset_game()
                st.rerun()
        with nav3:
            if st.button("Nächste Phase ▶", key="next_phase", type="primary"):
                next_phase()
                st.rerun()

        # Battle log
        st.divider()
        st.markdown("### 📜 Kampfprotokoll")
        log_text = "\n".join(reversed(st.session_state.battle_log[-25:]))
        st.text_area("", value=log_text, height=220, disabled=True, key="log_area", label_visibility="collapsed")

    # ── RIGHT: Necrons ───────────────────────────────────────────────────────
    with right:
        st.markdown("## 🔵 NECRONS")
        for unit in NECRON_UNITS:
            unit_card(unit, st.session_state.necron_units[unit.uid], "Necrons")


if __name__ == "__main__":
    main()
