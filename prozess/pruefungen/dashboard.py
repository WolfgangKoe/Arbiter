"""Erzeugt `dashboard.html` aus dem Lauf-Log: Tokenstand je Lauf, daneben die Verteilung."""

import html
import sys
from pathlib import Path

from belegung import sperrschwelle, warnschwelle
from laufLog import läufeLesen
from pfade import wurzel

dashboardDatei = "dashboard.html"
sichtbareLäufe = 40
legende = (
    "Balken: Belegung je Lauf",
    "Gelb: ab Warnschwelle",
    "Rot: ab Sperrschwelle",
    "Rechts: Verteilung je Rolle",
    "Hell: Mittel, dunkel: Höchstwert",
)

stil = """
body{font:14px sans-serif;margin:1.5rem;color:#222}
main{display:flex;gap:2rem;flex-wrap:wrap}
section{flex:1;min-width:22rem}
.zeile{display:flex;align-items:center;gap:.5rem;margin:2px 0}
.name{width:11rem;white-space:nowrap;overflow:hidden}
.spur{flex:1;background:#eee;height:14px;position:relative}
.balken{height:14px;background:#4a8;position:absolute;left:0}
.warnung{background:#ca3}.sperre{background:#c44}.mittel{background:#9bd}.hoechst{background:#26a}
.zahl{width:5rem;text-align:right}
ul{padding-left:1.2rem;color:#555}
"""


def punkte(zahl: int) -> str:
    return f"{zahl:,}".replace(",", ".")


def stufe(belegung: float) -> str:
    if belegung >= sperrschwelle:
        return "sperre"
    return "warnung" if belegung >= warnschwelle else ""


def balkenZeile(name: str, belegung: float, klasse: str, beschriftung: str) -> str:
    breite = min(100.0, 100 * belegung / sperrschwelle)
    return (
        f'<div class="zeile"><span class="name">{html.escape(name)}</span>'
        f'<span class="spur"><span class="balken {klasse}" style="width:{breite:.1f}%"></span>'
        f'</span><span class="zahl">{html.escape(beschriftung)}</span></div>'
    )


def laufZeilen(läufe: list[dict]) -> list[str]:
    jüngste = läufe[-sichtbareLäufe:]
    return [
        balkenZeile(
            f"{lauf['zeit'][5:16].replace('T', ' ')} {lauf['rolle']}",
            lauf["belegung"],
            stufe(lauf["belegung"]),
            punkte(lauf["belegung"]),
        )
        for lauf in reversed(jüngste)
    ]


def rollenZeilen(läufe: list[dict]) -> list[str]:
    nachRolle: dict[str, list[int]] = {}
    for lauf in läufe:
        nachRolle.setdefault(lauf["rolle"], []).append(lauf["belegung"])
    zeilen = []
    for rolle in sorted(nachRolle):
        werte = nachRolle[rolle]
        mittel = sum(werte) // len(werte)
        zeilen.append(
            balkenZeile(f"{rolle} ({len(werte)})", max(werte), "hoechst", punkte(max(werte)))
        )
        zeilen.append(balkenZeile("", mittel, "mittel", punkte(mittel)))
    return zeilen


def seiteErzeugen(läufe: list[dict]) -> str:
    if läufe:
        linksZeilen, rechtsZeilen = laufZeilen(läufe), rollenZeilen(läufe)
    else:
        linksZeilen = rechtsZeilen = ["<p>Noch kein Lauf protokolliert.</p>"]
    punktListe = "".join(f"<li>{html.escape(eintrag)}</li>" for eintrag in legende)
    return (
        '<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Arbiter · Läufe</title>'
        f"<style>{stil}</style></head><body><h1>Tokenstand der Läufe</h1><main>"
        f"<section><h2>Belegung je Lauf</h2>{''.join(linksZeilen)}</section>"
        f"<section><h2>Verteilung je Rolle</h2>{''.join(rechtsZeilen)}</section>"
        f"</main><h2>Legende</h2><ul>{punktListe}</ul></body></html>\n"
    )


def dashboardSchreiben(ordner: Path) -> Path:
    ziel = ordner / dashboardDatei
    ziel.write_text(seiteErzeugen(läufeLesen(ordner)), encoding="utf-8")
    return ziel


if __name__ == "__main__":
    print(dashboardSchreiben(wurzel))
    sys.exit(0)
