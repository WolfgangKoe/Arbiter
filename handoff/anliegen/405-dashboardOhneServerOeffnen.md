# Dashboard ohne Server zeigt keine Anliegen

405 · Fragen · von Regelumsetzer (Prozess) → Stakeholder · Runde 1/3 · angenommen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Du siehst keine Anliegen im Dashboard, weil du die Datei `dashboard.html` direkt
öffnest. Sie zeigt nur den Tokenbericht (Läufe, Verteilung, Legende), ohne Reiter. Seit
Anliegen 360 ([Regeln](../../prozess/regeln.md#rollenregeln)) stehen die Anliegen, der Reiter „Anliegen“ und
„Du bist dran: n“ nur auf den Seiten des Mini-Servers. Es ist also kein Fehler im Mechanismus,
sondern die Art des Öffnens. So geht es:

1. Im Projektordner `python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer`
   starten (bleibt offen, beenden mit Strg+C).
2. Im Browser `http://127.0.0.1:8765/` öffnen. Der Tokenbericht ist dort der Reiter
   „Tokenbericht“ (`/tokens`).

Die Tabellen, die aus ihren Boxen ragten (Tokenverteilung je Rolle, Läufe mit Dauer und
Kontextfenster), sind behoben: Sie stehen nun in einer waagerecht scrollbaren Hülle, Zahlen
und Spaltenköpfe brechen nicht mehr um. Scheiter-Test:
[dashboardTest.py](../../prozess/pruefungen/rollenregeln/dashboardTest.py),
`testTabellenSindInScrollbarerHülleUndZahlenBrechenNichtUm`.

**Kosten.** Wer die Datei öffnet, hält das Dashboard für unvollständig und bemerkt es erst spät.

**Gegenvorschlag.** Bestehende Regel: Anliegen 360 (zwei Seiten, Server). Eine Änderung daran
braucht dein Wort.

**F1 · Was soll `dashboard.html` ohne Server zeigen?**
A) Einen Hinweis oben: „Anliegen: Server starten, `…/rollenregeln.dashboardServer`“.
B) Nichts ändern; du startest den Server.
C) Die Datei entfällt, der Server ist der einzige Einstieg.
Empfehlung: A, kleinster Eingriff, der die Verwechslung beendet.
Antwort: B, bitte ergänze diesen Befehl bitte dauerhaft in retro.md, damit ich diesen immer finde. Das Dashboard ohne Server soll den aktuellen Befehl ebenfalls zeigen.

**Stellungnahme.** Es wäre noch gut, wenn im Tokenbericht eine gelber Hinweis erschiene, wenn es eine offene Frage an mich gibt. Sobald ich Antwort und Status zu diesem Anliegen gesetzt habe, soll dieser Hinweis verschwinden. Auf diese Weise bekomme ich an mich gerichtete Anliegen mit, wenn ich mal nicht reinschaue.
Der Fehler in den Tabellen ist immer noch nicht behoben. Diese einfach wegzublenden, statt die Tabellengörße an die Kästen zu hängen, ist keine Lösung.
