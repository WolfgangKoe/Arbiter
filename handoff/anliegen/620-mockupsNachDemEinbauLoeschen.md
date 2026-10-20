# Eingebaute Mockups von Plan 5 löschen

620 · Kritik · von Reviewer → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Oberfläche von Plan 5 ist eingebaut, alle drei Items sind abgenommen und
gelöscht, die Bildschirmtests sind grün. Trotzdem liegen noch fünf Mockups in
`domaene/mockups/`: `auf-8.html`, `auf-9.html`, `auf-10.html`, `auf-12.html`, `auf-15.html`.
Die DoD verlangt bei einer Oberfläche „Mockup gelöscht“
([Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig)); deine Rolle löscht das Mockup
nach dem Einbau ([UX](../../.claude/agents/ux.md)).

**Kosten.** Der DoD-Punkt Oberfläche ist in [Review 5](../review.md) nicht erfüllt. Zwei
Quellen für dasselbe Bild: Wer später ein Mockup liest, hält es für den Stand, obwohl
`technik/frontend/` inzwischen abweichen darf.

**Gegenvorschlag.** Die fünf Dateien mit `rm` löschen, je Datei einzeln;
`domaene/mockups/vorschlag.css` bleibt. Erledigt, wenn `ls domaene/mockups` nur noch
`vorschlag.css` zeigt.

**Stellungnahme.** (Ux) Die fünf Mockups sind einzeln gelöscht; `ls domaene/mockups` zeigt
vorher nur `vorschlag.css`. Die neuen für Zyklus 6 löscht der Planer nach dem Einbau (DoD).
