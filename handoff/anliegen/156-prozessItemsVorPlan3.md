# Prozess-Items vor Plan 3 auf das Nötige begrenzen

156 · Kritik · von Planer (Domäne) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund.** [Retro 2](../retro.md) misst eine Prozesslast von 52 % gegen die Schwelle ein
Drittel (Befund 2) und beauftragt danach acht Läufe des Regelumsetzers: P1 bis P6, dann
[114](114-pruefskripteOrdnenUndLesbarMachen.md) und
[139](139-bashSandboxStattHeuristik.md), je Lauf eins, jeder mit Kritik am Code. Nach dem
[Ablauf](../../prozess/ablauf.md#prozessphase) liegen sie alle vor der Freigabe der Retro
und damit vor Plan 3. Plan 3 bringt das, was der Stakeholder sehen will: die erste
Oberfläche ([145](145-ersteOberflaecheImBrowser.md)). Ob 114 und 139 vor oder nach der
Freigabe laufen, sagt die Retro nicht; 139 braucht erst die Antwort aus der Freigabe.

Nur ein Teil davon wirkt auf Plan 3:
- P1 (Abdeckung, toter Code) ändert die DoD, an der die Items von Plan 3 gemessen werden,
  und geht wie P2 auf das Anliegen des Stakeholders zurück
  ([150](150-sonarlintAbdeckungUndToterCode.md)).
- P4 ist die Löschung, die die Kennzahl verlangt, und klein.
- P3 (Höchstmaße, vorher drei Dateien teilen), P5 (Dashboard), P6 (`kennzahlen.py`), 114
  und 139 betreffen nur Prüfskripte und Werkzeuge; kein Item von Plan 3 hängt an ihnen.

**Kosten.** Bleibt es so, wartet das erste sichtbare Inkrement auf acht Läufe an den
Prüfskripten, nachdem Zyklus 2 dort schon zwölfmal so viel geändert hat wie am Produkt
(Befund 2). Die Retro reagiert auf die Prozesslast, indem sie sie im nächsten Abschnitt
weiter erhöht; die Kennzahl selbst verlangt nur eine Löschung und begrenzt den Rest nicht.

**Gegenvorschlag.** Die Retro nennt, welche Prozess-Items vor der Freigabe laufen, und
begründet jedes mit seiner Wirkung auf den nächsten Zyklus:
1. Vor der Freigabe: P1, P2, P4.
2. P3, P6, 114 und 139 warten auf die Prozessphase von Zyklus 3 (Ablauf, Anliegen: „Anliegen
   an eine Perspektive, deren Phase nicht läuft, warten, außer sie blockieren das
   Inkrement“).
3. P5 ist ein Wunsch des Stakeholders (Anliegen 90); ob das Dashboard vor Plan 3 kommt,
   entscheidet er in der Freigabe, Empfehlung danach.

Erledigt, wenn die Retro die Läufe vor der Freigabe nennt und keiner davon ohne Wirkung auf
Plan 3 oder ohne Wunsch des Stakeholders ist.
