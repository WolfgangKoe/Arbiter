# Startprompt erst, wenn nichts mehr läuft

Form: Kritik
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Aus Zyklus 10, weitergegeben vom Koordinator (dein Wortlaut liegt mir nicht vor,
ergänze ihn gern mit `Kommentar:`): Der Koordinator gab Startprompts unvollständig und
reichte Änderungen nach. Dein Vorschlag: Startprompt erst, wenn nichts mehr läuft, und dann
vollständig.
Verwandt: In [14500](14500-punkteFuerDieProzessphase.md) standen Punkte nur im Startprompt,
(a) bis (z) sind verloren; in [14360](14360-parallelArbeitenIstDieRegel.md) stand eine
Annahme nur im Startprompt.
Bestehende Regeln (Ich 4):
- [Koordinator](../../.claude/agents/koordinator.md): „Nach einer Freigabe oder ab 120.000
  Token … empfiehlst du einen neuen Chat mit einem Startprompt zum Kopieren, der den nächsten
  Schritt nennt.“ Sie sagt nicht, wann und was vollständig heißt; angepasst deckt sie den
  Befund.
- Ebenda: „Befunde, Fragen oder Empfehlungen in einer Schlussantwort schickst du nach
  `handoff/`.“ Deckt, dass nichts nur im Startprompt steht.
- [Prozessphase](../../prozess/ablauf/prozessphase.md), letzter Absatz: „den Stand bringt der
  Hook mit“; der Stand zählt auch die uncommitteten Dateien.
- [Budget](../../prozess/ablauf/budget.md): Ab 120.000 Token beginnt die Rolle nichts Neues
  und schließt ab; für den Koordinator fehlt das.

**Kosten.** Heute: Jede nachgereichte Änderung kopierst du erneut, und unklar ist, welcher
Prompt gilt; was nur im Prompt stand, geht verloren. Mit dem Gegenvorschlag: Du wartest, bis
der letzte Lauf fertig und committet ist; die Belegung des Koordinators wächst dabei nur um
die kurzen Schlussantworten. Ein Item, einige hundert Token.

**Gegenvorschlag (Organisationsentwickler).** Nach einer Freigabe oder ab 120.000 Token
startet der Koordinator nichts Neues. Erst wenn keine Rolle mehr läuft und der Stand
„0 uncommittete Dateien“ zeigt, gibt er einmal den Startprompt: nächster Schritt, was frei
ist, das Log eines Befehls, der im Hintergrund weiterläuft (etwa der Mutationslauf). Was der
neue Chat sonst wissen muss, steht vorher in einem Anliegen. Nachgereicht wird nichts; was
danach kommt, nimmt der neue Chat aus dem Stand.
Ändern: die Regel in den Absatz der [Prozessphase](../../prozess/ablauf/prozessphase.md), auch
für 120.000 Token; [Koordinator](../../.claude/agents/koordinator.md) (2.498 von 2.500 Zeichen)
und [Budget](../../prozess/ablauf/budget.md) verlinken nur. Als Prozess-Item der
[Retro 10](../retro.md), mit 15960. Mechanismus: nur Text. Rückweg: Commit `P<k>:`
zurücknehmen.

**Stellungnahme.**

**F1 · Wann und wie gibt der Koordinator den Startprompt?**
A: Wie im Gegenvorschlag, einmal, wenn keine Rolle mehr läuft und alles committet ist; nur Text (Koordinator)
B: Wie A, dazu nennt der Stand die laufenden Rollen, vermerkt beim Start und Ende jedes Laufs; ein Lauf des Regelumsetzers (neu)
C: Wie bisher, gleich nach der Freigabe (Koordinator)
Empfehlung: A, der Koordinator weiß, was er gestartet hat, und erfährt, wenn es endet; es
fehlte nur die Regel, wann. Greift sie nicht, folgt B.
Antwort: A
