# Dashboard: langsam, Architektur unübersichtlich, Ansicht springt zurück

Form: Kritik
Von: Stakeholder
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 9

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Das Dashboard wird mit der Zeit langsam. Ich vermute, das liegt daran, dass es zwischenzeitlich sehr viele Informationen laden muss. Bei den Anliegen ist das okay, aber es muss nicht alle Tokenreports laden. Es würde reichen, wenn eine Seite geladen wird und sollte dann mal weiter geblättert werden, sollte die jeweilige Seite geladen werden. Die Architekturseite im Dashboard hat an sich schon alles, was ich von seiten der Mammutmap erwarten würde, außer dass es übersichtlich ist (s. Screenshot). Das sollte besser werden. Ich habe nur keine Idee wie. So nutzt es nur wenig. Und ich habe beobachtet, dass die automatische Aktualisierung mit Daten, die Ansicht immer wieder zurücksetzt. Das ist so auch nicht gut. Es sollte eher so bleiben, wie es beim letzten Mal eingestellt war.“
Screenshot: Kästen Start, Seite, Web, Anwendung, Speicher, Katalog, darunter Domäne mit Dateien und Unterordnern; viele sich kreuzende Pfeile mit Importzahlen quer über die Fläche.

Ursachen (Code gelesen, nicht gemessen):
1. Tokenbericht: [dashboardServer.py](../../prozess/pruefungen/rollenregeln/dashboardServer.py)
   erzeugt die Seite bei jedem Aufruf neu und liest dazu alle Läufe (`laeufe.jsonl`, 1530 Zeilen, 577 KB, wächst mit jedem Lauf). Alle Sitzungskarten stehen im HTML; das Blättern ([dashboardSeiten.py](../../prozess/pruefungen/rollenregeln/dashboardSeiten.py), Anliegen 246) blendet im Browser nur aus. Geladen wird also alles.
2. Architektur: Jede Importbeziehung ist ein Pfeil mit Zahl, alle zugleich; bei offenen Kästen kreuzen sie sich.
3. Zurücksetzen: [neuladenSkript](../../prozess/pruefungen/rollenregeln/dashboardAnliegenSeiten.py) ruft bei jeder Änderung in `handoff/` `location.reload()`. Es schont nur Formulareingaben; Seite des Blätterns, aufgeklappte Kästen und Scrollstand gehen verloren.

**Kosten.** Je Punkt klein bis mittel, ein Lauf des Regelumsetzers. Ändern sich Tests von Anliegen 246, 360 und 3120 (`dashboardSeitenTest.py`, `dashboardArchitekturTest.py`). Rückweg je Punkt: Commit zurücknehmen.

**Gegenvorschlag.**
1. `/tokens?seite=n`: Der Server rendert nur die sechs Sitzungen der Seite; Seitenschalter als Verweise.
2. Architektur: Pfeile nur der angeklickten Kästen, verbotene (rot) immer; die Zahlen zusätzlich als Liste beim Kasten.
3. Seite, aufgeklappte Kästen und Scrollstand im Browser merken (`sessionStorage`) und nach dem Neuladen wiederherstellen.

**Stellungnahme.**

Annahme: Bis zur Antwort wird nichts umgesetzt; danach gilt die Empfehlung.

**F1 · Tokenbericht seitenweise vom Server laden?**
- Ja, sechs Sitzungen je Seite (Anliegen 246, Wortlaut) · empfohlen
- Nein, wie bisher (neu)

Antwort: .

**F2 · Wie wird die Architektur übersichtlich?**
- Pfeile nur beim angeklickten Kasten, Verbotenes immer (neu; Grund: Ziel Übersicht, Absicht 3) · empfohlen
- Keine Pfeile, nur Liste der Importzahlen (neu)

Antwort: .

**F3 · Ansicht nach der Aktualisierung erhalten?**
- Ja, Seite, Aufklappzustand und Scrollstand merken (Wortlaut) · empfohlen
- Neu laden nur auf Klick (neu)

Antwort: .
