"""Wer Freigabe oder Kommentare des Stakeholders in Plan, Review oder Retro ändert."""

from collections import Counter

from lesen.artefakt import freigabeJa, freigabeOffen, istStakeholderKommentar
from lesen.plan import zyklusAusText


def geschützteZeilen(text: str) -> list[str]:
    """`Freigabe: ja` und Kommentare des Stakeholders; beide ändert nur er."""
    zeilen = [zeile.strip() for zeile in text.splitlines()]
    return [zeile for zeile in zeilen if zeile == freigabeJa or istStakeholderKommentar(zeile)]


def freigabeVerstoß(bisher: str, danach: str) -> str | None:
    """Warum eine Rolle Freigabe oder Kommentare nicht so ändern darf, sonst `None`."""
    alteZeilen = [zeile.strip() for zeile in bisher.splitlines()]
    neueZeilen = [zeile.strip() for zeile in danach.splitlines()]
    alt, neu = zyklusAusText(bisher), zyklusAusText(danach)
    if alt is None or (neu is not None and neu > alt):
        # Warum: Die Datei des nächsten Zyklus beginnt neu, aber nie schon freigegeben.
        return (
            "beginnt mit `Freigabe: ja`; das setzt nur der Stakeholder."
            if (freigabeJa in neueZeilen)
            else None
        )
    vorher, nachher = Counter(geschützteZeilen(bisher)), Counter(geschützteZeilen(danach))
    if nachher - vorher:
        return f"setzt `{next(iter(nachher - vorher))}`; das tut nur der Stakeholder."
    if vorher - nachher:
        fehlt = next(iter(vorher - nachher))
        return f"ändert oder entfernt `{fehlt}`; das tut nur der Stakeholder."
    if freigabeOffen in alteZeilen and freigabeOffen not in neueZeilen:
        return "ändert `Freigabe: offen`; das tut nur der Stakeholder."
    return None
