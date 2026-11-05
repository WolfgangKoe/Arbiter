# Fliegen: Übergehen in die Nahkampfreichweite ohne Test

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen

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

**Stellungnahme.**
