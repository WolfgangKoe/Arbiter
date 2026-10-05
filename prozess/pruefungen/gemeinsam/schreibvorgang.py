"""Ziel und Ergebnis eines Write oder Edit, wie ein Hook sie vor dem Schreiben sieht."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe


def schreibZiel(eingabe: HookEingabe, wurzel: Path) -> Path | None:
    """Der aufgelöste Zielpfad eines Write oder Edit; `None` bei anderem Werkzeug oder ohne Pfad."""
    if eingabe.werkzeug not in ("Write", "Edit") or not eingabe.angaben.get("file_path"):
        return None
    ziel = Path(eingabe.angaben["file_path"])
    return (ziel if ziel.is_absolute() else wurzel / ziel).resolve()


def bisherigerInhalt(ziel: Path) -> str | None:
    """Der Text der Datei, `""` wenn sie fehlt, `None` wenn sie kein UTF-8 ist."""
    try:
        return ziel.read_text(encoding="utf-8") if ziel.is_file() else ""
    except UnicodeDecodeError:
        return None


def neuerInhalt(eingabe: HookEingabe, bisher: str) -> str | None:
    """Der Text der Datei nach dem Write oder Edit; `None`, wenn der Aufruf ihn nicht nennt."""
    angaben = eingabe.angaben
    if eingabe.werkzeug == "Write":
        return angaben.get("content")
    alt, neu = angaben.get("old_string"), angaben.get("new_string")
    if alt is None or neu is None:
        return None
    return bisher.replace(alt, neu, -1 if angaben.get("replace_all") else 1)
