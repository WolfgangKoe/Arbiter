# Offene Anliegen wirksam begrenzen, Schreibbilanz ohne Fehlalarm

306 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · beantwortet

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Deine Kommentare zu Retro 3 und [296](296-prozesslastEindaemmen.md) über den
Koordinator. (1) Offen sind 34, davon 27 an den Regelumsetzer, der Deckel ist 10. Seit
`Freigabe Retro 2` kamen 139 neu, 127 gingen; 82 der neuen gingen an den Regelumsetzer
(Reviewer 44, ich 20, Architekt 14). Seit dem Deckel kamen 300, 301, 302, 304, 305 an ihn,
vier über die Ausnahme „Fehlverhalten“, belegt mit Proben in `/tmp` oder am Code gelesen,
keins in einem echten Lauf beobachtet außer 304. 202 bis 206 und 221
stehen im Backlog und sind trotzdem offen. (2) `rollenregeln/schreibBilanz.py` meldet jede
Änderung ohne Rolle als „unklar, wer … Nicht committen, dem Stakeholder melden“: deine und
die eines gleichzeitigen Laufs (zuletzt `ablauf.md`, `retro.md` beim Reviewer). Auch „kam
ein Commit hinzu“ trifft jeden Commit eines Nachbarn. An der Bilanz hingen seit 278 zwei Runden
Fehlverhalten in 300 und zwei Punkte in 305.

**Kosten.** Der Deckel ist nur Text mit offener Tür; jede Änderung an Prüfskripten erzeugt
mehr Kritik, als abfließt. Fehlalarme lehren den Koordinator, Meldungen zu übergehen.

**Gegenvorschlag.** Geprüft (ich.md 4): Deckel ([Kennzahlen](../../prozess/kennzahlen.md)),
[Kritik am Code](../../prozess/ablauf.md#kritik-am-code), `anliegenregeln/anliegennummer.py`
(prüft schon jede neue Datei) decken es angepasst ab; gelöscht wird zuerst.

**F1 · Bestand abbauen.** Offen an den Regelumsetzer bleiben 215 (Sandbox ersetzt die
Bash-Heuristik), 246 (von dir), 302 (Sammel), 304. Die übrigen 23 schließen die Absender mit
`erledigt` und einer Zeile im [Backlog](../../prozess/backlog.md) samt Auslöser; 305: Punkte
1, 2 deckt 215, 3, 4 entfallen mit F3. 219 schließt der Reviewer mit 220 (Regel bleibt nur
Text), 138 wartet auf 215; offen bleiben 10, davon 4 an den Regelumsetzer.
- A (empfohlen): so, in einem Lauf je Absender.
- B: nur 202 bis 206, 221 (schon im Backlog).

Antwort: A. Wichtig wäre zunächst den Bestand abzubauen, bevor etwas neues geöffnet wird, aber gleichzeitig etwas wirksames zu implementieren, damit der Regelumsetzer nicht immer angefragt wird und die Pipeline voll macht. Ich sehe ehrlich gesagt nicht, ob all diese ANliegen dem Produkt dienen oder ob hier nicht wieder die Organisation das Produkt ist.

**F2 · Zufluss sperren.** Fehlverhalten am Code des Regelumsetzers zählt nur mit Beleg aus
einem echten Lauf (Lauf, Befehl, Meldung); Gelesenes und Nachgestelltes geht ins Sammel.
`anliegennummer.py` sperrt eine neue Datei an eine Rolle mit 10 offenen, außer vom
Stakeholder; ein weiteres Fehlverhalten kommt als neue Runde ins offene Anliegen derselben Datei.
- A (empfohlen): so; Mechanismus angepasst, nach F3.
- B: Beleg-Regel nur als Text, Deckel ohne Sperre.
- C: Kritik am Code der Prüfskripte bis Retro 4 aussetzen.

Antwort: Hmm, wäre ein Beleg ein wirksamer Mechanismus, der den Zulauf sperrt?

**F3 · Mechanismus löschen.** Zuerst gelöscht (Prozesslast-Reaktion): Schreibbilanz am
SubagentStop samt `angefasstePfade.py`, `schreibMeldung.py` und Tests. Write und Edit sperrt
`schreibgrenze.py` vorher, Bash die Heuristik, den Rest später 215. Bleibt: die Nennung der
Schreibpfade beim Start. Was nach den Pfaden aller Läufe uncommittet bleibt, gilt als deins;
der Koordinator committet es nicht und meldet nichts.
- A (empfohlen): so.
- B: behalten, nur „verletzt“ (Rolle nannte den Pfad schreibend); „unklar, wer“ und
  Commit-Meldung entfallen.
- C: behalten, „unklar, wer“ als Hinweis ohne „Nicht committen“.

Antwort: Was hat "Mechanismus löschen" mit committen zu tun? Ich will, dass mein Produkt entwickelt wird und nicht, wie könnne wir jedes zweites Anliegen eine Schraube nach links drehen um sie dazwischen kurz nach rechts zu drehen. Bitte einen wirksamen Vorschlag um das Zustopfen des Regelumsetzers einzudämmen. Ich will sehen, dass Anforderungen geschrieben, in AK-testfälle umgesetzt und diese dann durch Produktivcoe grün gemacht werden. Wo ist das Problem?

Nach deinen Antworten ändere ich Kennzahlen, Ablauf und Backlog und beauftrage den Regelumsetzer.

**Stellungnahme.**
