# Mockups: englische Namen, Spielerfarbe, vorweggenommene Zonenfarbe

223 · Kritik · von Architekt (Technik) → UX · Runde 1/3 · erledigt

## Runde 1
Geprüft: [que-2.html](../../domaene/mockups/que-2.html), [auf-4.html](../../domaene/mockups/auf-4.html)
und [vorschlag.css](../../domaene/mockups/vorschlag.css) als Komponenten, die die Technikphase
ohne Umschreiben übernimmt ([Plan 3](../plan.md), Anliegen 151 F2). Das Bild prüft
Anliegen 222.

**Befund 1 · Benennung.** Die Klassen `gameHeader…`, `armyCard…`, `unitCard…` und die
Variablen `--arb-bg`, `--arb-surface`, `--arb-accent-lt` sind englisch, `--spieler-1` ist
kebab-case. [wir.md](../../prozess/praemissen/wir.md) gilt auch fürs Frontend: deutsch,
camelCase; ein Begriff der Anforderung steht wörtlich im Code. AUF-4.3 nennt den Ort *Ablage*,
das Mockup `armyCard`. Der Name führt zudem irre: Eine *aufgestellte* *Einheit* verschwindet
aus der *Ablage*, sie zeigt nicht die *Armee*. Die Namen stammen aus Arbiter-old, das der
Stakeholder in Anliegen 145 F1 (git) als Vorbild fürs Design nennt; eine Ausnahme von der
Prämisse ist das nicht ausdrücklich. Keine Prüfung meldet es: `benennung.py` und `glossar.py`
lesen nur `.py`.

Kosten: Jetzt drei Dateien ohne Code. Nach dem Einbau stehen die Namen in HTML, CSS,
JavaScript, Komponentenseite und Bildschirmtests; später umbenennen heißt jede Fundstelle.

Gegenvorschlag: Namen nach Glossar (`ablage…`, `kopfzeile…`), Variablen deutsch und
camelCase (`--hintergrund`, `--akzentHell`, `--spieler1` …).

**F1 · Gilt die Prämisse auch für die Komponenten aus Arbiter-old?**
- A: Ja, deutsche Namen nach Glossar wie oben.
- B: Nein, die Namen aus Arbiter-old (`gameHeader`, `armyCard`, `unitCard` und weitere) sind
  eine Ausnahme; sie wird in wir.md eingetragen.

Empfehlung: A. Der Name trägt die Bedeutung (wir.md): `ablageEinheit` sagt, was der Spieler
dort sieht, `unitCard` nur, wie es aussieht. Das Design aus Arbiter-old bleibt mit beiden
Antworten gleich; es ändern sich nur Bezeichner.

Antwort: armyCard -> armeeKarte, unitCard -> einheitenKarte, armyCardName -> armeeKartenName und entsprechend alles weitere. gameActionArea -> spielAktionsBereich, alles andere dürfte passen

**Befund 2 · Spielerfarbe je Komponente.** `vorschlag.css` setzt die Farbe des Spielers in
vier Komponenten einzeln: `.gameHeaderSpieler.spieler1`, `.armyCard.spieler1 .armyCardName`,
`.aufstellungszone.spieler1`, `.modell.spieler1`, dasselbe für `spieler2`, dazu
`.aufstellungszone.ohneSpieler`: neun Regeln. Jede weitere Komponente in Spielerfarbe
(Auswahl, Reichweite, Sperre) bringt zwei neue.

Kosten: heute gleich viele Zeilen; mit jeder Komponente eine Regel mehr als nötig, und eine
neue Farbe ändert man an vier Stellen.

Gegenvorschlag: Die Klasse des Spielers setzt nur eine Variable,
`.spieler1 { --spielerFarbe: var(--spieler1); }`, ebenso `spieler2` und `ohneSpieler`; jede
Komponente liest `var(--spielerFarbe)`, eine Regel je Komponente.

**Befund 3 · que-2.html zeigt AUF-4.6.** Dort tragen die Zonen `spieler1` und `spieler2`,
also die Farbe ihres Besitzers. Das verlangt AUF-4.6 aus Item 2; QUE-2.3 verlangt nur eine
Fläche. Fällt Item 2 („Reicht der Zyklus nicht, fällt Item 2“), übernimmt Item 1 mit dem
Markup die Besitzerfarbe: Code ohne Kriterium seines Items und ohne Akzeptanztest.

Kosten: zwei Attribute.

Gegenvorschlag: In que-2.html tragen beide Zonen `ohneSpieler`; die Besitzerfarbe zeigt nur
auf-4.html.

**Stellungnahme (UX).**
Befund 2 und 3 angenommen und umgesetzt: Die Klasse des Spielers setzt `--spielerFarbe`,
jede Komponente liest sie einmal; `que-2.html` zeigt beide Zonen `ohneSpieler`. Befund 1:
nach der Antwort umbenannt: `armeeKarte…`, `einheitenKarte…`, `kopfzeile…`, Variablen
deutsch wie vorgeschlagen; die spätere `gameActionsArea` heißt `spielAktionsBereich`.
Alle Mockups und `vorschlag.css` sind umgesetzt.

