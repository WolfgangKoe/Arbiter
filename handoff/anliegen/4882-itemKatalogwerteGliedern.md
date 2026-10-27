# Item: Katalogwerte gliedern

Form: Fragen
Von: Architekt
An: Planer
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Aus [4800](4800-ablageDerKatalogwerte.md) (F1 A, F2 B, F3 A mit der Auflage einer
Struktur, die sich jederzeit ergänzen lässt) folgt ein Umbau: neue Gliederung der Daten
([4880](4880-gliederungDerKatalogwerte.md)), Begriffe und Daten beim Anforderungsautor
([4881](4881-datenblaetterImGlossarUndInDenDaten.md)), dazu `katalog/` und seine Tests:
`ausgangslage.py` (103 Zeilen) liest heute `durchmesser` je Modell und, nach Item normalMove,
`bewegungsweite` je *Einheit*. Am Bildschirm ändert sich nichts.

**Kosten.** Jede *Einheit*, die vorher dazukommt, wird zweimal geschrieben. Plan 8 nennt für
Etappe 2 noch Ork-Psioniker und Canoptek-Spinne.

**Gegenvorschlag.** Ein Item `katalogwerteGliedern` in Plan 9: MIV-1.3 nach 4881, Tests,
`katalog/` liest das neue Format nach K1 bis K6.

**F1 · Wann kommt das Item?** A: als erstes Item von Plan 9, vor neuen *Einheiten*
(Anliegen 4800 F3). B: in Etappe 8 mit allen Datenblättern (Etappe 8).
Empfehlung: A. Heute ist der Umbau klein: vier *Einheiten*, zwei Werte. B baut bis dahin
jede neue *Einheit* im alten Format und danach um; das widerspricht der Auflage des
Stakeholders.

**Stellungnahme.**
