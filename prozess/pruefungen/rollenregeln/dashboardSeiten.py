tokensPfad = "/tokens"
sitzungenJeSeite = 6

schalterStil = """
.seitenschalter{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:4px 0 8px}
.seitenschalter a{background:var(--panel-2);color:var(--text);border:1px solid var(--border);
border-radius:5px;padding:5px 11px;font-size:.84rem;text-decoration:none}
.seitenschalter a[aria-current="page"]{background:var(--accent-text);color:var(--bg);
font-weight:700}
.seitenschalter .gesperrt{opacity:.35;border:1px solid var(--border);border-radius:5px;
padding:5px 11px;font-size:.84rem}
.seitenschalter .seiten-stand{color:var(--text-muted);font-size:.82rem;margin-left:6px}
"""


def seitenAnzahl(anzahlSitzungen: int) -> int:
    return max(1, -(-anzahlSitzungen // sitzungenJeSeite))


def seiteBegrenzt(seite: int, anzahlSitzungen: int) -> int:
    return min(max(seite, 1), seitenAnzahl(anzahlSitzungen))


def verweis(text: str, ziel: int, zusatz: str = "") -> str:
    return f'<a href="{tokensPfad}?seite={ziel}"{zusatz}>{text}</a>'


def seitenschalter(anzahlSitzungen: int, seite: int) -> str:
    if anzahlSitzungen <= sitzungenJeSeite:
        return ""
    letzte = seitenAnzahl(anzahlSitzungen)
    zurück = (
        verweis("‹ Zurück", seite - 1) if seite > 1 else '<span class="gesperrt">‹ Zurück</span>'
    )
    weiter = (
        verweis("Weiter ›", seite + 1)
        if seite < letzte
        else '<span class="gesperrt">Weiter ›</span>'
    )
    nummern = "".join(
        verweis(str(nummer), nummer, ' aria-current="page"' if nummer == seite else "")
        for nummer in range(1, letzte + 1)
    )
    von = (seite - 1) * sitzungenJeSeite + 1
    bis = min(anzahlSitzungen, seite * sitzungenJeSeite)
    stand = f"Session {von}–{bis} von {anzahlSitzungen}, neueste zuerst"
    return (
        f'<nav class="seitenschalter" id="seitenschalter" data-pro-seite="{sitzungenJeSeite}" '
        f'aria-label="Seitenauswahl">{zurück}{nummern}{weiter}'
        f'<span class="seiten-stand">{stand}</span></nav>'
    )


def sitzungenDerSeite(sitzungen: list, seite: int) -> list:
    anfang = (seite - 1) * sitzungenJeSeite
    return sitzungen[anfang : anfang + sitzungenJeSeite]
