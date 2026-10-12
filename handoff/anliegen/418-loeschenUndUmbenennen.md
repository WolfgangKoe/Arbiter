# Wer darf Dateien löschen und umbenennen?

418 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Seit dem Commit „Regelumsetzer und Organisationsentwickler: Schreibgrenze gilt
auch für Bash (Anliegen 385, 384)“ kann keine Rolle eine Datei löschen oder umbenennen: Write
und Edit legen nur an und überschreiben, `rm`, `mv`, `git rm` und `git mv` sperrt
[bashSchreiben.py](../../prozess/pruefungen/rollenregeln/bashSchreiben.py). Claude Code hat
dafür kein eigenes Werkzeug ([Werkzeuge](https://code.claude.com/docs/en/tools-reference)),
und seine Berechtigungsregeln gelten für alle Rollen gleich. Der Ablauf verlangt es aber:
- Planer: abgenommene Items löschen ([Technikphase 5, DoD 3](../../prozess/ablauf.md#technikphase));
  die drei Items von Plan 5 stehen noch (Anliegen 417).
- UX: Mockup gelöscht, sobald die Oberfläche gebaut ist ([DoD](../../prozess/ablauf.md#dod-item-fertig)).
- Anforderungsautor und Testautor: Anforderungen neu schneiden, die Testdateien folgen ihrem
  Namen; vor der Sperre per Umbenennen (Commit „Anforderungsautor und Testautor: Anforderungen
  je Datei neu geschnitten, Tests im selben Zug (340, 345, 361)“).
- Implementierer: Im Commit „Implementierer: Aufstellen als Paket, Eingaben geprüft, Ziehen
  mit Bewegung (Anliegen 396–399, 401)“, nach der Sperre, fallen zwei Module weg; auf welchem
  Weg, steht nicht im Commit.
- Jede Rolle: eine falsch benannte oder leere Datei in `handoff/anliegen/`. Das ist deine
  offene Frage, ob Koordinator oder Mechanismus sie löschen und umbenennen; dieselbe Lücke.

**Kosten.** Plan 5 gilt als nicht fertig, das Review wartet (DoD 3); jeder Zyklus trifft es
wieder. Wer an der Sperre vorbei löscht, tut es unbemerkt.

**Gegenvorschlag.** Bestehende Regel (Ich 4): [Ich 2](../../prozess/praemissen/ich.md)
angepasst, statt den Ablauf je Fall zu ändern.

**F1 · Wer löscht und benennt um?**
A: Jede Rolle in ihren Schreibpfaden. Ich 2 bekommt: „Löschen und Umbenennen mit `rm` und `mv`
nur in deinen Schreibpfaden; in `handoff/anliegen/` nur, was noch nicht committet ist.“
Mechanismus: `schreibgrenze.py`; der Regelumsetzer gibt `rm` und `mv` frei, wenn jeder Pfad in
den Schreibpfaden der Rolle liegt und keine Sperre trifft. `git rm` und `git mv` bleiben
gesperrt: Sie merken die Änderung schon für den Commit vor und geraten so in den Commit einer
gleichzeitig laufenden Rolle. Empfehlung: ein Weg für alle Fälle, die Rolle prüft danach
selbst, ob alles grün ist; ein Irrtum bleibt in git.
B: Der Koordinator auf Nennung. Die Rolle nennt in der Schlussantwort, was wegfällt oder wie es
heißen soll; der Koordinator führt es mit `git rm` und `git mv` im Commit des Laufs aus. Kein
Code, aber geänderte Rechte: Heute schreibt er keine Dateien
([Koordinator](../../.claude/agents/koordinator.md)). Die Rolle sieht ihr Ergebnis nicht; nach
einem Umbenennen bleiben die Prüfungen rot, bis er es ausführt.
C: Nur die Items (Gegenvorschlag des Planers in 417): Der Planer nennt sie, der Koordinator
löscht sie mit dem Commit der Abnahme. Die übrigen Fälle bleiben offen.
Antwort: .

**F2 · Die drei Items von Plan 5 jetzt?**
A: Der Koordinator löscht sie einmalig mit `git rm`, als deine Ausnahme. Empfehlung: Das
Review wartet nicht, bis F1 gebaut ist.
B: Der Planer löscht sie, sobald F1 umgesetzt ist.
Antwort: .

**Stellungnahme.**
