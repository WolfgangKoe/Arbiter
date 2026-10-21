# P5: Deckel für TODOs, Werkzeugkommentare und die bestehenden Kommentare

1860 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · angenommen

## Runde 1
**Befund.** P5 der [Retro 6](../retro.md) setzt deinen Auftrag
[1660](1660-regelkommentareEntbehrlich.md) um: Im Code stehen nur noch TODOs, gedeckelt; ein
TODO, das schon vor der laufenden Technikphase da war (Commit „Freigabe Plan <n>“), macht am
Ende der Technikphase die DoD über das Inkrement rot. Der Architekt fand in
Anliegen 1850, Punkt 6, was der Regelumsetzer dafür noch nicht weiß:
1. Wie hoch der Deckel ist.
2. Welche Kommentare für Werkzeuge bleiben. `# noqa` ohne Regelcode schaltet jede ruff-Regel
   der Zeile ab; heute stehen 8 solcher Kommentare, einer ohne Code.
3. Was mit den bestehenden Kommentaren geschieht: 58 `Regel:` und 100 `Warum:` in Produkt,
   Tests, Frontend und Prüfcode. Sperrt die Prüfung sie sofort, kann kein Item committet
   werden, bis alle weg sind.

**Kosten.** Ohne Antwort rät der Regelumsetzer ([Ich 1](../../prozess/praemissen/ich.md)), oder
P5 macht mit seinem ersten Commit jede Prüfung rot.

**Gegenvorschlag.** Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)):
[Es 8](../../prozess/praemissen/es.md), [Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig).

**F1 · Wie viele TODOs dürfen im Code stehen?**
A: Höchstens drei, eins je Item eines Plans; ein Plan hat höchstens drei.
B: Höchstens fünf.
C: Keins; was zu tun ist, wird ein Anliegen.
Empfehlung: A. Jedes TODO ist Arbeit für die nächste Technikphase, mehr als ein Plan fasst,
schafft sie nicht.
Annahme: P5 baut den Deckel mit drei.
Antwort: .

**F2 · Welche Kommentare für Werkzeuge bleiben erlaubt?**
A: Eine feste Liste, je mit Regelcode: `# noqa: PLR2004` (ruff) und
`// eslint-disable-next-line <Regel>`; ohne Regelcode gesperrt, ebenso `# pragma: no cover`
und `# type: ignore`.
B: Jeder Werkzeugkommentar, wenn er einen Regelcode nennt.
Empfehlung: A. Jeder Eintrag schaltet eine Prüfung ab; die Liste zeigt, welche.
Annahme: P5 baut die Liste nach A.
Antwort: .

**F3 · Wer entfernt die bestehenden Kommentare, und wann?**
A: Im Prüfcode der Regelumsetzer mit P5. In Produkt, Tests und Frontend Implementierer und
Testautor in der Technikphase 7, neben den Items; die Prüfung meldet sie erst in der DoD über
das Inkrement von Zyklus 7 als rot.
B: Sie gelten als TODOs von vor der Technikphase 7, ohne Deckel.
Empfehlung: A. Die Items bleiben committbar, und am Ende der Technikphase 7 ist der Code frei.
Annahme: P5 baut die Prüfung nach A.
Antwort: .

**Stellungnahme.**
Kommentar: Ich folge deinen Empfehlungen. Setze sie so um. Lass uns von Zeit zu Zeit darauf achten, dass die Agenten nicht auf anderen Wegen Kommentare schreiben. Der Code selbst soll erklären, was er tut. Ein Kommentar ist überflüssig. Es würde sich fast lohnen eine Art Whitelist zu führen. Wäre das noch eine sinnvolle Ergänzung an dieser Stelle?

**Klärung.** Ja, und sie steht schon: [Es 8](../../prozess/praemissen/es.md) erlaubt nur
Kommentare aus einer festen Liste (Werkzeugkommentare mit Regelcode, höchstens drei TODOs);
alles andere, auch `# Warum:`, sperrt P5 in `formregeln/kommentare.py` und
`eslintKommentare.mjs`. Darauf achtet der Reviewer im Rundgang Prüfcode. Bitte setze den Status.
