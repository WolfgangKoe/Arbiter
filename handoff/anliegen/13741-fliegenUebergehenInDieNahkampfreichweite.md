# Fliegen: Übergehen in die Nahkampfreichweite ohne Test

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: Ein Test prüft sein Kriterium nicht
([Kritik](../../prozess/ablauf/kritik.md)). BEW-18.7 verlangt BEW-8.5 an der *Stelle*
danach. Nach 8.5 nennt der *Eintrag* ‚Nahkampfreichweite‘, wenn 6.2 ohne 3.1 angehalten
hätte. Für eine Spinne heißt das nach 18.3: Sie steht nach dem Übergehen in der
*Nahkampfreichweite*. Diesen Fall prüft keiner der Tests zu 18.7 in
`technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py`. Der Code nennt den *Grund* heute
nicht, siehe [13740](13740-fliegenAlsTypUndZweiFehler.md), Punkt 3. Mein
[Vertrag](../../technik/architektur/vertrag/bewegung/fliegen.md) führte den Fall bisher
nicht unter „Prüft“; jetzt steht er dort.

**Kosten.** Ein Test mit vorhandenen Helfern. Ohne ihn bleibt der fehlende *Grund* im
*Protokoll* unbemerkt.

**Gegenvorschlag.** `testBew18_7OhneFremdeBaseInDerNahkampfreichweiteNenntDerEintragBeideGründe`:
Die Spinne wird an der *Bewegungsweite* angehalten. Der Punkt dahinter liegt ohne fremde
*Base* in der *Nahkampfreichweite* des Warboss. Nach `gemeinsamÜbergehen()` erwartet der Test
`neuer.gründe == {Grund.bewegungsweite, Grund.nahkampfreichweite}`. Gegenprobe mit einem
Mutanten am Ende von 18.3 (min mit 3.1): Der Test ist dann rot.

**Stellungnahme.** Umgesetzt in `technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py`:
`testBew18_7OhneFremdeBaseInDerNahkampfreichweiteNenntDerEintragBeideGründe` wie
vorgeschlagen, der Punkt liegt 8″ weit. Zusätzlich aus demselben Kriterium, im
[Vertrag](../../technik/architektur/vertrag/bewegung/fliegen.md) unter „Prüft“ noch nicht genannt:
`testBew18_7InDerBewegungsweiteInDerNahkampfreichweiteNenntDerEintragNurDieNahkampfreichweite`,
der Punkt liegt 5″ weit, *Eintrag* nur mit ‚Nahkampfreichweite‘. Beide prüfen auch, dass die
Spinne am Punkt steht.

Ergebnis im Arbeitsstand: Der erste Test ist rot, der *Eintrag* nennt nur ‚Bewegungsweite‘; der
zweite ist grün. Grund: `_anteile` setzt beim Übergehen noch das Ende auf den Anteil von 3.1
(`ende = bewegungsweite`), BEW-8.5 verlangt das Ende ohne 3.1 (Punkt 3 von
[13740](13740-fliegenAlsTypUndZweiFehler.md), beim Implementierer in Arbeit). Gegenprobe an einer
Kopie in `/tmp` mit `ende = spielfeldkante`: alle zehn Tests zu 18.7 grün. Der rote Stand ist
damit zugleich dein Mutant.
