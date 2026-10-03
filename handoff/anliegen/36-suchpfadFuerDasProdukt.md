# Suchpfad: das Produkt fehlt, die Prüfskripte sind zu viel

36 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** `pyproject.toml` setzt `pythonpath = ["prozess/pruefungen"]`.
1. Das Produkt fehlt: `python3 -m pytest technik/tests` bricht beim Sammeln ab
   (`No module named 'arbiter'`). Nach [Anliegen 27](27-auf1-tests-ort-und-importpfade.md)
   sollte der Implementierer `pythonpath = ["technik"]` eintragen; seit `pyproject.toml`
   dir gehört, darf er das nicht mehr (`implementierer.md`: per Anliegen an dich). Er ist
   der nächste Schritt und fände den Code nur über den `sys.path`-Eingriff in
   `technik/tests/akzeptanz/conftest.py`, den 27 gerade streichen will.
2. `prozess/pruefungen` ist überflüssig: Ohne den Eintrag laufen alle 278 Prüfungen grün
   (geprüft mit `-o pythonpath=`), weil pytest den Ordner einer Testdatei ohne
   `__init__.py` ohnehin vorne in den Suchpfad stellt. Der Eintrag gilt aber für jeden
   Lauf, auch `python3 -m pytest technik/tests`: Dort ist dann `import benennung` oder
   `import stand` möglich. Das Produkt könnte so vom Prozess abhängen, und ein späteres
   Produktmodul mit gleichem Namen wie ein Prüfskript (`stand`, `belegung`) würde still
   verdeckt.

**Kosten.** Zu 1: Ohne den Eintrag kann der Implementierer die Tests nicht grün machen,
oder der Hack bleibt und wandert in jede künftige `conftest.py`. Zu 2: eine Abhängigkeit
gegen die Richtung (Prozess prüft Technik, nie umgekehrt), die kein Test bemerkt.

**Gegenvorschlag.** `pythonpath = ["technik"]`. Das passt unabhängig davon, wie der
Testautor 27 entscheidet: Der Implementierer darf nur in `technik/arbiter/` schreiben
(`schreibgrenze.py`), also liegt das Paket `arbiter` dort. Scheiter-Test in
`konfigurationTest.py`: `prozess/pruefungen` steht nicht im Suchpfad, `technik` schon.

**Stellungnahme.**
