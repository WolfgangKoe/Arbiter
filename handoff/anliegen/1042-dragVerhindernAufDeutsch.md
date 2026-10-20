# Funktion dragVerhindern ist halb englisch

1042 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu [680](680-markierterTextSperrtDasZiehen.md) in
[seite.js](../../technik/frontend/seite.js): Die neue Funktion `dragVerhindern` trägt das
englische „drag“. [Wir 1](../../prozess/praemissen/wir.md) und
[Es, Lesbarkeit](../../prozess/praemissen/es.md): Bezeichner deutsch. Das Ereignis
`dragstart` gibt der Browser vor, den Namen der Funktion nicht. Nach
[Ich 3](../../prozess/praemissen/ich.md) wartet der Befund (Name einer Hilfsfunktion, keine
Prüfung rot).

**Kosten.** Neben `ziehenBeginnen` und `ziehenAbbrechen` liest sich `dragVerhindern` wie ein
anderer Vorgang; dass es um das Ziehen des Browsers geht, sagt der Name nicht.

**Gegenvorschlag.** Umbenennen in `browserZiehenVerhindern`, der Aufruf
`document.addEventListener("dragstart", …)` bleibt. Erledigt, wenn `grep -n dragVerhindern
technik/frontend` nichts mehr findet.

**Stellungnahme.** Angenommen und umgesetzt: `browserZiehenVerhindern`; `grep -n
dragVerhindern technik/frontend` findet nichts mehr.
