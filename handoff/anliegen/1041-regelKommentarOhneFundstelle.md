# Regel-Kommentar zum Knopf ohne Fundstelle

1041 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu [830](830-knopfInDerEinheitenkarteBekommtKeinenKlick.md) in
[seite.js](../../technik/frontend/seite.js), `ziehenBeginnen`:
`// Regel: Ein Druck auf einen Knopf beginnt keinen Zug` nennt keine Fundstelle.
[Es 8](../../prozess/praemissen/es.md) lässt Kommentare nur als `Regel: <Fundstelle>` oder
`Warum: …` zu; die Nachbarn halten es so (`// Regel: V8, ein Zug beginnt erst …`). V8 nennt
den Satz noch nicht, der Architekt trägt ihn erst ein (830). `formregeln/kommentare.py` prüft
nur Python, darum ist keine Prüfung rot.

**Kosten.** Wer die Zeile liest, sucht eine Regel, die es nirgends gibt; als `Regel:` gibt
sie eine Entscheidung der Technik als Spielregel aus.

**Gegenvorschlag.** Bis V8 den Satz hat: `// Warum: Sonst fängt die Karte den Zeiger und der
Knopf bekommt keinen Mausklick`; steht er in V8, dann
`// Regel: V8, ein Druck auf einen Knopf beginnt keinen Zug`. Erledigt, wenn die Zeile eine
der beiden Formen hat.

**Stellungnahme.** Angenommen; erledigt, indem Wächter und Kommentar entfallen
([1090](1090-knopfWaechterOhneFallUndZiehenDerKarte.md), Punkt 1): Der Fall hat keine
Anforderung mehr.
