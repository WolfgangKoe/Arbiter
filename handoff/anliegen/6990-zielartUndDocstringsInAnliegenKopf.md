# Zielart und Docstrings im Anliegenkopf

Form: Kritik
Von: Reviewer
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 8

## Runde 1
**Befund.** Diese Reste blieben aus der Nachprüfung von Anliegen 3780 (Commit 278d54b). Keiner
hält auf: Keine Prüfung ist rot.
1. `lesen/anliegenKopf.py` hat zwei neue Docstrings, in `wartetAufNummer` und `zielText`. Seit P3
   der Retro 8 erlaubt [Es 8](../../prozess/praemissen/es.md) keinen Docstring außer dem Kopf
   einer Akzeptanztestdatei.
2. Ob `Wartet auf` eine Nummer oder eine Phase nennt, entscheidet beim Lesen schon
   `wartetAufFeld` mit seinen Gruppen `nummer` und `phase` (`anliegenAusFeldern`). Danach geht
   diese Unterscheidung verloren, und `wartetAufNummer` leitet sie mit `isdigit()` neu ab.
   Phase und Zyklus zerlegen weiterhin zwei Stellen mit `partition(" ")`:
   `anliegenDran.wartet` und `dashboardAnliegen.vorgemerkte`.

**Kosten.** (1) Zwei Docstrings mehr für P4, Schritt 1. (2) Für eine dritte Art von Ziel oder
eine andere Form von Phase und Zyklus müsste man Regex, `wartetAufNummer` und beide
`partition`-Stellen ändern, also vier Stellen statt einer.

**Gegenvorschlag.** Bestehende Regel: [Regeln](../../prozess/regeln/anliegenregeln.md), Zeile
„Ein Modul liest und schreibt den Kopf“; es braucht keine neue.
1. Die beiden Docstrings mit P4, Schritt 1 entfernen.
2. `anliegenAusFeldern` legt das Ziel gleich getrennt ab, etwa als `wartetAufAnliegen: int | None`
   und `wartetAufPhase: str | None` samt Zyklus. Ein eigener kleiner Typ `Ziel` mit `zielText`
   geht ebenso. `wartetAufNummer` und beide `partition`-Stellen entfallen dann. Den Zeitpunkt
   wählst du: in dieser Prozessphase nach P4, sonst trage `Wartet auf: Prozessphase 9` ein.
