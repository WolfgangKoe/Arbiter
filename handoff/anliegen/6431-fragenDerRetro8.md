# Fragen der Retro 8: Docstrings, Testautor, Prämissen

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Zu deinen Aufträgen 6430 und 6380 und zu
[Rollen mit Auslöser](../../prozess/ablauf/rollenMitAusloeser.md). Am Bildschirm ändert keine
Frage etwas.

**Kosten.** Je Frage.

**Gegenvorschlag.** Beantworte F1 bis F3 vor der Freigabe der Retro 8; „.“ heißt, die
Empfehlung gilt. Umgesetzt in P1, P3 und P4 der [Retro 8](../retro.md).

**F1 · Welche Docstrings bleiben?** Docstring: der Satz in `"""…"""` am Kopf einer Datei
oder Funktion; heute rund 500, davon 71 im Produkt.
A: Nur der Spiegel nach deiner Sicht: Die Testdatei beginnt mit der Überschrift ihrer
Anforderung samt Kürzel (`"""OBJ-1 · Armeen und Spielfeld."""`); Kriterium und Satz trägt der
Name des Tests (`testObj1_1JederSpielerFührt…`). Sonst keiner (Anliegen 6430,
[T1](../../technik/architektur/tests.md)).
B: Dazu einer je Produktmodul mit seiner Aufgabe, ohne Kennungen (Es S).
C: Wie heute (Es 8).
Bei A löschen die Rollen die übrigen einmal, die Prüfung lässt nur den Spiegel zu; Es S:
„sein Name nennt sie“.
Empfehlung: A; so arbeitet T1 schon. Mein früheres A „ohne Kennungen“ widersprach T1.
Antwort: .

**F2 · Testautor auf Opus?** Der Testautor schreibt aus deinen Kriterien die Tests, bevor der
Code entsteht; er läuft auf Sonnet, dem günstigeren Modell. In Technikphase 8 prüften seine
Tests oft nur einen Fall (nur Spieler 1, nur Schlachtrunde 1): Die Mutationsprüfung verfälscht
den Code absichtlich, 16 % davon bemerkte zuerst kein Test. 6 der 12 Rückläufe gingen darum an
ihn; für diesen Fall gilt Opus.
A: Opus (Rollen mit Auslöser). Code: Tests prüfen eher gleich jeden Fall. Arbeit: Jeder Lauf
kostet je Token doppelt so viel; billiger erst, wenn kaum noch Rückläufe nötig sind.
B: Sonnet bleibt; seine Anleitung (Skill `akzeptanztest-schreiben`) bekommt das
Gegenbeispiel „nur Spieler 1“ (neu). Ob das reicht, zeigt erst Zyklus 9.
Empfehlung: A und das Gegenbeispiel; sinken die Rückläufe bis Retro 9 nicht, zurück auf Sonnet.
Antwort: .

**F3 · Verschiebe ich diese Stellen der Prämissen?** Prämissen: deine Texte Absicht, Ich, Wir,
Es; die ersten drei liest jede Rolle in jedem Lauf. Sechs Stellen sind Ablauf, der anderswo
steht, oder gelten nur für wenige Rollen:
1. Ich 1, „die Moderation listet … zuoberst“: steht im Moderator; streichen.
2. Ich 2, die Skripte der Schreibgrenze und ihre Lücken: stehen in den Rollenregeln; der Link
   bleibt.
3. Ich 3, die Einordnung „Hält auf, Wartet, Entfällt“: braucht nur, wer kritisiert; nach
   [Kritik](../../prozess/ablauf/kritik.md).
4. Ich 5, „Fragen … als Datei in `handoff/`“: Review 8 fragte dich ohne Antwortfeld. Neu in
   Ich 1: Fragen an dich nur in einem Anliegen.
5. Root-CLAUDE.md, „Akzeptanztests entstehen vor dem Code“: Handwerk, nach Es; Testautor und
   Technikphase haben es.
6. Es L und I, „Noch ohne Anlass“: ein Stand, keine Regel (Wir 4); streichen.
A: Alle sechs (Anliegen 6380, Wir 3). B: Nur 1, 2, 3, 6, die keine Regel ändern (Anliegen
6380). C: Keine (Anliegen 2590).
Code: nichts. Arbeit: Ich wird 1.000 Zeichen kürzer.
Empfehlung: A.
Antwort: .

**Stellungnahme.**
Kommentar: F2 und F3 verstehe ich nicht. Bitte ausführen. Bei F1 habe ich zumindest eine Art Meinung, die ggf. durch den aktuellen Stand gedeckt ist. Wir verwenden Docstrings vor allem und einen Spiegel zwischen Akzeptanztests und den Akzeptanzkriterien herzustellen, korrekt? ALso QUE-1.1 würde einen entsprechenden Test in der Technik haben, wo genau diese Abkürzung in der Datei steht, zusätzlich noch ein Satz, was das für ein TEst ist. Bei allen anderen Codezeilen sollte das an sich nicht nötig sein. Der Code selbst sollte lesbar sein und der Docstring daher unnötig. Ist hingegen der Inhalt des Docstrings nicht im Code zu lesen, dann wird auch ein zusätzlicher Docstring nicht zu einem besseren Verständnis beitragen. Wie machen wir es nun?

**Klärung.** Oben ausgeführt; F1 nach deiner Sicht neu.
