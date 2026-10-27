# Ablage der Bewegungsphase im Domänencode, für später

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Kritik am Code zu Item normalMove (`git diff 7684034`). Diese Befunde warten
nach Ich 3 (Ablage, keine Prüfung rot):
1. Die *Bewegungsphase* holt Hilfen aus Modulen von Anforderungen der *Aufstellung*:
   `gesetzteModelle` aus `phasen/aufstellen/beenden.py` (in `phasen/bewegung/beenden.py`
   und `querschnitt/schlachtrunden.py`), `einheitVon` aus `aufstellen/reihenfolge.py`,
   `verschobeneStellen` aus `aufstellen/einheitVerschieben.py`. Nach dem
   [Grundschnitt](../../technik/architektur/domaene.md) liegt, was mehrere Ordner brauchen,
   im gemeinsamen Elternteil; sonst ändert eine Änderung an AUF-24 oder an *Aufstellung
   beenden* unbemerkt die *Normale Bewegung*.
2. QUE-1 hat nun eigene Regeln (`gründeDesSetzens`, `inNahkampfreichweite`,
   `baseÜberdeckt`) in `querschnitt/__init__.py`. Grundschnitt: eine Anforderung mit eigenen
   Regeln wird ein gleichnamiges Modul, hier `querschnitt/setzen.py`.
3. `Schlacht` unterscheidet die *Phase* per `if` (`phaseBeenden`, `stellenBeimLoslassen`).
   Bei einer *Phase* mit eigenem Verhalten ist das nach Es 9 richtig. Kommt die zweite
   (Schuss- oder Chargephase), wird jede ein eigener Typ, an den `Schlacht` übergibt (Es, O).

**Kosten.** Je Punkt ein Umzug ohne neues Verhalten; die Tests bleiben, nur Importe ändern
sich.

**Gegenvorschlag.** 1: `gesetzteModelle`, `einheitVon` und `verschobeneStellen` nach
`phasen/__init__.py` oder `querschnitt/`, wo beide Phasen sie finden. 2: `querschnitt/setzen.py`.
3: erst mit der zweiten *Phase* mit eigenem Verhalten.

**Stellungnahme.**
