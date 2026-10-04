"""Jeder sichtbare Ordner auf oberster Ebene ist Perspektive, `handoff` oder Altbestand."""

from pathlib import Path

from agenten import altbestandOrdner
from pfade import perspektiven

bekannteOrdner = {*perspektiven, "handoff", *altbestandOrdner}


def unbekannteOrdner(wurzel: Path) -> list[str]:
    """Namen sichtbarer Ordner der Wurzel, die weder Perspektive noch Altbestand sind."""
    return sorted(
        ordner.name
        for ordner in wurzel.iterdir()
        if ordner.is_dir() and not ordner.name.startswith(".") and ordner.name not in bekannteOrdner
    )
