"""Ordner des Repos, die mehrere Prüfungen kennen."""

from pathlib import Path

wurzel = Path(__file__).resolve().parents[2]

perspektiven = ("domaene", "technik", "prozess")
akzeptanzOrdner = "technik/tests/akzeptanz"
anforderungsOrdner = "domaene/anforderungen"
anliegenOrdner = "handoff/anliegen"
etappenOrdner = "domaene/etappen"
itemsOrdner = "domaene/items"
mockupOrdner = "domaene/mockups"
