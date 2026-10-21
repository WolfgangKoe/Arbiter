# QUE-2.1: immer dieselbe Adresse, belegt heißt Abbruch

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder hat in 1650 entschieden: Arbiter startet immer unter
`http://127.0.0.1:8040/` (F1). Ist die Nummer belegt, bricht Arbiter mit einer Meldung ab und
weicht nicht auf eine andere aus (F2). Heute verlangt
[QUE-2.1](../../domaene/anforderungen/querschnitt/karte.md) nur, dass Arbiter „die Adresse
nennt“. Darum wählt der Server bei jedem Start eine freie Nummer
([W5](../../technik/architektur/web.md)), und ein Lesezeichen gilt nur bis zum nächsten Start.

**Kosten.** Ohne Kriterium entsteht kein Item und kein Akzeptanztest, die Entscheidung bleibt
liegen. Ein Kriterium ohne den Fall „belegt“ ließe offen, ob Arbiter ausweicht. Ein Ausweichen
führt das Lesezeichen still zur alten Partie.

**Gegenvorschlag.** Nach deinem Urteil, etwa:
- QUE-2.1 **Wenn** jemand Arbiter mit einem Befehl startet, **dann** nennt Arbiter die
  Adresse `http://127.0.0.1:8040/`, bei jedem Start dieselbe, unter der die *Spieler* die *Karte*
  im Browser öffnen (Anliegen 145 F1 A, 1650).
- QUE-2.x **Gegeben** die Adresse von QUE-2.1 ist schon belegt (etwa weil Arbiter schon läuft),
  **wenn** jemand Arbiter startet, **dann** startet Arbiter nicht und nennt die Adresse als
  belegt (Anliegen 1650 F2).

Technisch prüfbar ohne Zusammenstoß: Die Tests starten den Befehl mit einer freien Nummer und
prüfen die feste Adresse, ohne sie zu belegen (W5 ziehe ich mit dem Item nach).

**Stellungnahme.** Angenommen als eigene Anforderung
[QUE-8](../../domaene/anforderungen/querschnitt/festeAdresse.md) (8.1 Adresse, 8.2 belegt);
QUE-2.1 bleibt mit seinem Test, QUE-2 wäre sonst über dem Höchstmaß.
