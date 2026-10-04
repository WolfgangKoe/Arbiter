# Aufstellung entflechten: Gründe als Tabelle, Verhalten an den Begriff

154 · Kritik · von Architekt → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Aus [152](152-solidUndVieleIf.md): Drei Stellen in
`technik/arbiter/domaene/phasen/aufstellen.py` fragen mit `if`, was Daten oder ein Begriff
beantworten sollten.
1. `_gründeGegenDieStelle` prüft die Sperren beim Setzen (QUE-1.2, AUF-3.2, AUF-3.4) als
   Kette `if … gründe.add(…)`, dazu eine Schleife mit `continue`. Ein neuer Grund, etwa die
   Kohärenz in Etappe 1, ändert die Funktion.
2. `aufstellungszone(spieler)` leitet die Zone mit drei `if` und `next(…)` aus dem Gewinner
   ab.
3. `_modelleVon(spieler)` ist eine Frage an die `Armee`, `_grenzenInX` eine an die
   Aufstellungszone; beide stehen in der Klasse `Aufstellung`, die damit Geometrie trägt.

Die Wächter am Anfang der Handlungen (`if … raise Sperre(…)`) bleiben: Je einer steht für
ein Kriterium (`prozess/praemissen/wir.md` 9).

**Kosten.** Ab Zyklus 3 ruft die Oberfläche `Aufstellung` auf, und jeder weitere Grund folgt
dem vorhandenen Muster. Umbau jetzt: ein Lauf, keine neuen Tests.

**Gegenvorschlag.** Refactoring zu Beginn der Technikphase von Zyklus 3, vor neuen Tests.
Vorbild: `ArbiterMap/backend/app/domain/rule_checks.py`, je Regel eine Funktion,
`check_rules` sammelt nur ein.

Erledigt, wenn
- die Akzeptanztests unverändert grün sind (`python3 -m pytest technik/tests`), ebenso
  `python3 -m pytest prozess/pruefungen` (Verhalten unverändert);
- je Grund beim Setzen eine Funktion besteht, die nur ihn prüft, und `_gründeGegenDieStelle`
  die Gründe aus einer Tabelle Grund → Funktion sammelt, ohne `if`;
- die Aufstellung bei der Zonenwahl eine Zuordnung Spieler → Aufstellungszone anlegt und
  `aufstellungszone(spieler)` sie nur nachschlägt;
- `_modelleVon` als `modelle` an der `Armee` in `spielobjekte.py` steht und die Grenzen
  einer Zone außerhalb der Klasse `Aufstellung` berechnet werden;
- keine neue Klasse und kein neuer Enum-Wert entsteht; braucht es doch einen Begriff, geht
  vorher ein Anliegen an den Anforderungsautor (Glossar).

**Stellungnahme (Implementierer).** Angenommen und umgesetzt, alle fünf Bedingungen:
- `_gründeGegenDieStelle` sammelt aus der Klassentabelle `_prüfungen` (Grund → Prüfung) ohne
  `if`; je Grund eine Methode: `_nichtGanzInDerZone`, `_baseÜberdeckt`,
  `_inNahkampfreichweiteVonGegnern`. Ein neuer Grund ist eine Methode und eine Zeile.
- `aufstellungszoneWählen` legt `_zonen` (Spieler → Aufstellungszone) an,
  `aufstellungszone(spieler)` schlägt nur nach; `_zoneDesGewinners` entfällt.
- `modelle` steht an `Armee` (`spielobjekte.py`), `_modelleVon` entfällt;
  `grenzenInXDerZone` ist eine Funktion des Moduls außerhalb der Klasse.
- Keine neue Klasse, kein neuer Enum-Wert, Akzeptanztests unverändert.
- `python3 -m pytest technik/tests` (153) und `python3 -m pytest prozess/pruefungen` (441)
  grün, ruff sauber.

Zu 152: D4 nach `architektur.md` ist Sache des Architekten (155).
