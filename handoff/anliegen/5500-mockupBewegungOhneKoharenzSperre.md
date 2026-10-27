# Mockups der Bewegungsphase zeigen keine Sperre ‚keine Kohärenz‘

Form: Fragen
Von: Ux
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [5180](5180-annahmenZurBewegungsphase.md) F5 gibt es keinen Knopf „Bewegung der Einheit beenden“ mehr. Die Mockups [bew-1](../../domaene/mockups/bew-1.html) und [bew-2](../../domaene/mockups/bew-2.html) zeigen ihn nicht mehr; bew-2 zeigt nur noch ‚über eine Base‘, denn ein Modell hält am *B* an (F6), das ist keine *Sperre*. Die *Sperre* ‚keine Kohärenz‘ beim Knopf „Phase beenden“ (BEW-1.2) zeigt noch kein Mockup.

**Kosten.** Ein drittes Mockup kostet eine kleine Datei und eine Rückfrage zur Meldung; es ist kein Happy Path.

**Gegenvorschlag.** F1 beantworten.

**F1 · Soll ein Mockup die Sperre ‚keine Kohärenz‘ bei „Phase beenden“ zeigen?** A: nein, die Meldung ist wie in QUE-5.5 und im Mockup [que-5](../../domaene/mockups/que-5.html) bekannt (Anliegen 5180). B: ja, eigenes Mockup `bew-3.html` mit der Meldung unter der Karte (neu). Empfehlung: A, es steht nur da, was verlangt ist (Absicht 3).
Annahme: A; ich zeige keine eigene Darstellung.
Antwort: A

**Stellungnahme.**
Kommentar: So wie ich es verstehe, nutzen wir bereits bestehende Komponenten. Gibt es dazu nicht schon etwas im Frontend? Wozu haben wir das sonst?
Stellungnahme: Ja, die Komponente gibt es: `sperrmeldung` mit `sperrmeldungGrund` steht auf der [Komponentenseite](../../technik/frontend/komponenten.html) mit ‚keine Kohärenz‘, und [que-5](../../domaene/mockups/que-5.html) nutzt sie. Darum braucht „Phase beenden“ kein eigenes Mockup; die Technik setzt dieselbe Komponente ein. Mockups bleiben unverändert; nachgeprüft.
