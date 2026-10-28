# Fragen der Retro 8: Docstrings, Testautor, Prämissen

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Zu deinen Aufträgen 6430 und 6380 und zum Auslöser „Testautor auf Opus“
([Rollen mit Auslöser](../../prozess/ablauf/rollenMitAusloeser.md)). Gezählt mit grep:
- Im Produkt kein Kommentar mit `#`, aber 71 Docstrings, 38 davon mit Kennungen wie
  „(QUE-10.5)“, also wie die `# Regel:` aus 1660. Tests rund 150, Prüfcode rund 300.
  `pyproject.toml` hat 35 Zeilen `# Warum:`, die Daten-YAML 21; Es 8 erfasst beide nicht.
- 6 der 12 Hindernisse der Technikphase 8 gingen an den Testautor, meist ein Test für nur
  einen Fall (nur Spieler 1, nur Schlachtrunde 1, nur auf den Achsen); die Mutation fing
  zuerst 84 %.
- Prämissen: Falsch ist nichts, am falschen Fleck stehen sechs Stellen (unten, F3).

**Kosten.** Ohne Docstrings trägt allein der Name die Bedeutung (Es, Lesbarkeit). Opus kostet
je Token ein Mehrfaches von Sonnet; der Testautor lief in Zyklus 8 rund zehnmal.

**F1 · Welche Docstrings bleiben?**
A: Nur der des Moduls, ohne Kennungen; er nennt seine Aufgabe (Es S, Architektur T1).
Funktionen und Klassen ohne Docstring, auch in Tests und Prüfcode (Anliegen 1660).
B: Keine; auch die Aufgabe des Moduls trägt sein Name (Anliegen 1660).
C: Wie heute (Es 8).
Empfehlung: A. T1 braucht den Docstring der Testdatei, das Modul seine Aufgabe.
Antwort: .

**F2 · Testautor auf Opus?**
A: Ja, der Auslöser ist eingetreten (Rollen mit Auslöser).
B: Nein, nur ein Gegenbeispiel „nur Spieler 1“ im Skill `akzeptanztest-schreiben` (neu).
Empfehlung: A und dazu das Gegenbeispiel: Fehlende Fälle kosteten sechs Läufe.
Antwort: .

**F3 · Verschiebe ich diese Stellen der Prämissen?**
1. Ich 1, „die Moderation listet … zuoberst“: steht im Moderator; streichen.
2. Ich 2, Liste der Mechanismen und Lücken: steht in den Rollenregeln; nur der Link bleibt.
3. Ich 3, „Hält auf, Wartet, Entfällt“: braucht nur, wer kritisiert; nach
   [Kritik](../../prozess/ablauf/kritik.md).
4. Ich 5, „Fragen … als Datei in `handoff/`“: Review 8 fragte dich im Rundgang („schreib im
   Kommentar …“); neu in Ich 1: Fragen nur in einem Anliegen an dich.
5. Root-CLAUDE.md, „Akzeptanztests entstehen vor dem Code“: nach Es (Handwerk); zweimal in
   Zyklus 8 verletzt (6101, 6241).
6. Es L und I, „Noch ohne Anlass“: streichen.
A: Alle sechs (Anliegen 6380, Wir 3). B: Nur 1, 2, 3, 6, die den Wortlaut nicht ändern
(Anliegen 6380). C: keine (Anliegen 2590).
Empfehlung: A; Ich, das jeder Lauf lädt, wird um rund 1.000 Zeichen kürzer.
Antwort: .

**Gegenvorschlag.** Beantworte F1 bis F3 vor der Freigabe der Retro 8; „.“ heißt, die
Empfehlung gilt. Umgesetzt in P1, P3 und P4 der [Retro 8](../retro.md).

**Stellungnahme.**
Kommentar: F2 und F3 verstehe ich nicht. Bitte ausführen. Bei F1 habe ich zumindest eine Art Meinung, die ggf. durch den aktuellen Stand gedeckt ist. Wir verwenden Docstrings vor allem und einen Spiegel zwischen Akzeptanztests und den Akzeptanzkriterien herzustellen, korrekt? ALso QUE-1.1 würde einen entsprechenden Test in der Technik haben, wo genau diese Abkürzung in der Datei steht, zusätzlich noch ein Satz, was das für ein TEst ist. Bei allen anderen Codezeilen sollte das an sich nicht nötig sein. Der Code selbst sollte lesbar sein und der Docstring daher unnötig. Ist hingegen der Inhalt des Docstrings nicht im Code zu lesen, dann wird auch ein zusätzlicher Docstring nicht zu einem besseren Verständnis beitragen. Wie machen wir es nun?
