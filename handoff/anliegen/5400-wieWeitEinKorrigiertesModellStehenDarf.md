# Wie weit ein korrigiertes Modell stehen darf

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zu deiner Rückfrage in [5180](5180-annahmenZurBewegungsphase.md) F5 („Was ist
denn die Frage?“): Ohne den Knopf „Bewegung der Einheit beenden“ fehlte der Moment, in dem
Arbiter prüft, ob eine gezogene *Einheit* in *Kohärenz* steht. Deine Beschreibung entscheidet
das, wir bauen es so: Du ziehst in der *Bewegungsphase* deine *Einheiten* in beliebiger
Reihenfolge und korrigierst jede, so oft du willst. Erst „Phase beenden“ sperrt mit ‚keine
Kohärenz‘, solange eine deiner *Einheiten* nicht beisammensteht; diese *Sperre* kann niemand
übergehen (Ziel). Offen bleibt eine Folge: Bisher zählt Arbiter jede Strecke zusammen, die
ein *Modell* in der Phase zieht (*Distanz*). Ziehst du den Warboss 4″ vor und korrigierst
ihn dann 2″ zur Seite, sind das 6″. Bei *B* 5″ hält er also nach 1″ an und kommt nicht an
seinen Platz.

**Kosten.** Bei A ändert der Anforderungsautor eine Zeile (*Distanz* im Glossar). Im Code
ist A einfacher, Arbiter rechnet dann exakt ohne Wurzel. Nachteil von A: Einen Umweg um eine
fremde *Base* zählt Arbiter nicht. B kostet nichts Neues, verhindert aber Korrekturen,
sobald das *B* aufgebraucht ist.

**F1 · Wie weit darf ein Modell am Ende der Bewegungsphase stehen?** A: höchstens *B* in
gerader Linie von seiner *Stelle* zu Beginn der Phase. Wie oft du es dazwischen ziehst,
zählt nicht (Anliegen 5180). B: alle Strecken der Phase zusammen höchstens *B* (Glossar,
Anliegen 4402). Empfehlung: A. So entsteht ein Stand, der regelkonform entstanden sein
könnte, und du kannst korrigieren.
Annahme: A. Der [Vertrag der Bewegung](../../technik/architektur/vertrag/bewegung.md)
rechnet so, Anforderungsautor und Testautor arbeiten damit.
Antwort: A

**Gegenvorschlag.** F1 beantworten; „.“ heißt, die Empfehlung gilt.

**Stellungnahme.**
