import html
from pathlib import Path

from anliegenregeln.anliegenDran import dran
from lesen.anliegenKopf import stakeholder

adresse = "127.0.0.1"
lokalesSchema = "http"
vorgabePort = 8765
öffnenBefehl = "python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer"
öffnenAdresse = f"{lokalesSchema}://{adresse}:{vorgabePort}/"

hinweisStil = """
.befehl{background:var(--panel);border:1px solid var(--border);border-radius:8px;
padding:8px 12px;margin:8px 0;font-size:.86rem}
.befehl code{color:var(--accent-text);overflow-wrap:anywhere}
.offene-frage{background:#fbbf24;color:#1c1a14;border-radius:8px;padding:8px 12px;margin:8px 0;
font-weight:600}
.offene-frage a{color:#1c1a14}
"""


def befehlHinweis() -> str:
    return (
        '<p class="befehl">Anliegen und Antworten gibt es nur auf dem Server. Im Projektordner '
        f"starten: <code>{html.escape(öffnenBefehl)}</code>, dann im Browser "
        f"<code>{html.escape(öffnenAdresse)}</code> öffnen (beenden mit Strg+C).</p>"
    )


def offeneFragen(ordner: Path) -> list[int]:
    return dran(ordner).get(stakeholder, [])


def frageHinweis(ordner: Path) -> str:
    nummern = offeneFragen(ordner)
    if not nummern:
        return ""
    liste = ", ".join(str(nummer) for nummer in nummern)
    return (
        f'<p class="offene-frage">Offen für dich: {len(nummern)} Anliegen ({liste}). '
        "Der Hinweis verschwindet, sobald Antwort und Status gesetzt sind.</p>"
    )


def hinweise(ordner: Path) -> str:
    return frageHinweis(ordner) + befehlHinweis()


def retroNenntBefehl(retroText: str) -> bool:
    return öffnenBefehl in retroText
