# Der Stand nennt für jedes Prozess-Item den Regelumsetzer

Form: Kritik
Von: Regelumsetzer
An: Regelumsetzer
Runde: 1/3
Status: angenommen
Wartet auf: Prozessphase 8

## Runde 1
**Befund.** Der Stand sagt „Nächster Schritt: Regelumsetzer: Prozess-Item P2 aus Retro 7“,
obwohl [Retro 7](../retro.md) P1 und P2 dem Organisationsentwickler zuweist (und dessen Haken
gesetzt sind). Ursache: `standregeln/phasenfolge.py`, `prozessschritt` (Zeile 70) schreibt
fest „Regelumsetzer“; `standregeln/fortschritt.py` kennt die Rolle je Item bereits
(`itemRollen`, Klammer in der Item-Zeile). Zweitens wählt `offenesProzessItem` das erste Item
ohne Commit `P<k>:`; ein Item, dessen Haken schon gesetzt ist, aber noch nicht committet wurde,
bleibt „offen“ und verdeckt die folgenden.

**Kosten.** Der Koordinator ruft die falsche Rolle auf oder stellt falsche Fragen
([Wir 3](../../prozess/praemissen/wir.md): zwei Quellen für dieselbe Aussage).

**Gegenvorschlag.** Bestehende Regel: [Regeln, Standregeln](../../prozess/regeln/standregeln.md),
Zeile „Fortschritt“. Den Namen aus `itemRollen` in `prozessschritt` einsetzen (die Funktion
dazu nach `lesen/` oder `phasenfolge.py` verlagern, damit kein Kreis entsteht); in
`phasenfolgeTest.py` ein Fall mit Item des Organisationsentwicklers. Ob ein abgehaktes, nicht
committetes Item als offen gilt, entscheidet die DoD der Prozessphase; Vorschlag: Haken
und Commit müssen beide stimmen, der Stand nennt es dann „Commit fehlt“. Wartet nicht auf die
Prozessphase, weil der Stand falsch führt; Umsetzung nach Freigabe in einem späteren
Prozess-Item.

**Stellungnahme.** Umgesetzt: `prozessschritt` nennt die Rolle aus der Klammer; `itemRollen`
liegt dafür in `standregeln/phasenfolge.py`. Test:
`phasenfolgeTest.py` `testDerNächsteSchrittNenntDieRolleAusDerKlammerDesItems`. Regel:
[Standregeln](../../prozess/regeln/standregeln.md). Nicht umgesetzt: „Haken und Commit müssen
beide stimmen“; das verlangt zuerst die DoD der Prozessphase (Organisationsentwickler).
