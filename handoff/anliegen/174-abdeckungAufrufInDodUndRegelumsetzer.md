# Abdeckung: Aufruf und Mechanismus in DoD 1 und Regelumsetzer nachtragen

174 · Kritik · von Regelumsetzer (Prozess) → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** P1 der Retro 2 ist gebaut (Anliegen 170, 171, 172), aber zwei Texte hinken nach:
1. [DoD 1](../../prozess/ablauf.md#dod-item-fertig) nennt die Abdeckung der Prüfskripte noch
   „Mechanismus: nur Text“. Gebaut ist `abdeckung.py` mit `abdeckungTest.py`; `technik/arbiter`
   misst der Lauf von `python3 -m pytest prozess/pruefungen` (mit `technik/tests`), die
   Prüfskripte der Hook `abdeckungPruefskripte` in `.pre-commit-config.yaml`.
   DoD 2 nennt vulture noch „nur Text“; gebaut ist `unbenutzterCode` in `abdeckung.py`.
2. [Regelumsetzer](../../.claude/agents/regelumsetzer.md), „Melde erst fertig“, nennt nur
   `python3 -m pytest prozess/pruefungen` und 95 % Zweigabdeckung. Die Messung der
   Prüfskripte läuft nicht mehr in diesem Lauf, sondern mit
   `python3 prozess/pruefungen/abdeckung.py`; ohne diesen Aufruf bleibt sie ungeprüft.

**Kosten.** Eine Rolle liest „nur Text“ und baut doppelt, oder meldet fertig, ohne die
Abdeckung der Prüfskripte zu messen.

**Gegenvorschlag.** DoD 1 und 2 nennen Mechanismus und Aufruf; der Regelumsetzer meldet
fertig, wenn Pytest grün ist und `python3 prozess/pruefungen/abdeckung.py` mit 0 endet.
Die Einträge stehen in [`prozess/regeln.md`](../../prozess/regeln.md).

**Stellungnahme.** Umgesetzt. [DoD 1](../../prozess/ablauf.md#dod-item-fertig) nennt
`abdeckung.py` mit beiden Aufrufen, DoD 2 `unbenutzterCode` für den toten Code; das Urteil
des Reviewers über Zeilen, die nur Einheitstests erreichen, bleibt. Aus den Werkzeugen für
offene Prüfungen ist vulture gestrichen. Der
[Regelumsetzer](../../.claude/agents/regelumsetzer.md) meldet fertig, wenn Pytest grün ist und
`python3 prozess/pruefungen/abdeckung.py` mit 0 endet.
