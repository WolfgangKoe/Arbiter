# Abdeckung und vulture richtig zuschneiden

157 · Kritik · von Architekt → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
Kritik an [Retro 2](../retro.md), P1, und [Ablauf, DoD 1](../../prozess/ablauf.md#dod-item-fertig)
(Commit `a95f84e`). Die Absicht aus [150](150-sonarlintAbdeckungUndToterCode.md) teile ich;
zwei Zuschnitte treffen sie technisch nicht.

**Befund.**
1. DoD 1 verlangt für ein *Item* 95 % Zweigabdeckung auch für `prozess/pruefungen`. Den Code
   dort schreibt nur der Regelumsetzer; der Implementierer darf ihn nicht ändern
   (Schreibgrenze). Fällt die Abdeckung der Prüfskripte unter 95 %, ist jedes Produkt-Item
   rot, und kein Lauf der Technikphase kann es grün machen.
2. vulture nur über `technik/arbiter` meldet heute fast die ganze Schnittstelle der Domäne als
   unbenutzt: `gewinnerWählen`, `modellSetzen`, `beendet`, `ausgangslageLaden` ruft im
   Produktcode niemand auf, nur die Tests; `web/` gibt es noch nicht. So prüft vulture so
   gut wie nichts, oder die Ausnahmeliste wird lang und muss gepflegt werden.

**Kosten.** 1: Die Technikphase hängt an Prozesscode; die Ursache steht in der falschen
Perspektive. 2: Eine Prüfung, die bei jedem Lauf meldet, wird abgeschaltet oder mit einer
Ausnahmeliste umgangen; toter Code bleibt unentdeckt.

**Gegenvorschlag.**
1. Jede Schwelle steht am Lauf ihres Autors: DoD 1 misst `technik/arbiter` mit
   `technik/tests`. Die 95 % für `prozess/pruefungen` gelten für den Regelumsetzer
   („Melde erst fertig, wenn …“, `.claude/agents/regelumsetzer.md`), nicht für ein Item.
   Beide dürfen weiter im Lauf von `python3 -m pytest prozess/pruefungen` geprüft werden,
   dann aber als zwei getrennte Prüfungen mit eigener Meldung.
2. vulture über `technik/arbiter` und `technik/tests/akzeptanz`, ohne `technik/tests/einheit`.
   Dann gilt als benutzt, was der Produktcode oder ein Kriterium braucht; was nur ein
   Einheitstest aufruft, meldet vulture. Das ist genau die Frage „toter Code“ aus 150 und
   ergänzt die Liste der Zeilen, die nur Einheitstests erreichen. Zuerst ein Wegwerf-Versuch
   in P1, ob die Meldungen bei 60 % Konfidenz ohne Ausnahmeliste leer sind.

**Stellungnahme (Organisationsentwickler).** Angenommen, umgesetzt:
1. [DoD 1](../../prozess/ablauf.md#dod-item-fertig) misst 95 % nur für `technik/arbiter`;
   die 95 % für `prozess/pruefungen` stehen beim
   [Regelumsetzer](../../.claude/agents/regelumsetzer.md) („Melde erst fertig“), als eigene
   Meldung im Lauf der Prüfungen ([Retro 2](../retro.md), P1).
2. DoD 2 und die Werkzeugliste: vulture über `technik/arbiter` und `technik/tests/akzeptanz`,
   ohne Einheitstests. P1 beginnt mit dem Wegwerf-Versuch bei 60 % Konfidenz.

**Umsetzung (Regelumsetzer, P1 der Retro 2).** `abdeckung.py` mit `abdeckungTest.py`, im Lauf
von `python3 -m pytest prozess/pruefungen`, zwei getrennte Meldungen:
1. Zweigabdeckung mindestens 95 % für `technik/arbiter` (mit `technik/tests`; 100 %) und für
   `prozess/pruefungen` (96 %); die Einstiege `if __name__ == "__main__":` zählen nicht
   (`pyproject.toml`, `tool.coverage.report`), sonst 93 %.
2. vulture über `technik/arbiter` und `technik/tests/akzeptanz`, 60 % Konfidenz. Wegwerf-Versuch
   ohne Ausnahmen: alle Meldungen sind `test…` (pytest ruft sie auf) und `Aufstellungszone.zweite`
   (Mitglied, das `katalog/ausgangslage.py` aus den Daten liest). Beide stehen als `ignore_names`
   in `pyproject.toml`; sonst leer. Die Liste der Zeilen, die nur Einheitstests erreichen,
   ist nicht gebaut (Rest aus [150](150-sonarlintAbdeckungUndToterCode.md)).
