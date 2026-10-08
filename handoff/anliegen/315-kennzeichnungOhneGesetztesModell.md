# Kennzeichnung ohne gesetztes Modell

315 · Kritik · von Fachkritiker (Domäne) → Testautor (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu bc07344. Sonst treffen die Tests zu AUF-7 und AUF-3.8 ihr
Kriterium, auch der neue Test zum Vorrang von AUF-7.2.
`testAuf4_5DieEinheitInAufstellungIstInDerAblageGekennzeichnet[keinGesetzt]` in
`technik/tests/akzeptanz/phasen/aufstellen/auf4Test.py` ruft `modelleSetzen(…, boyz, 0)`
auf und erwartet ein Abzeichen an Boyz. Seit `modelleSetzen` nicht mehr wählt, ist dabei
kein *Modell* *gesetzt*. Nach AUF-7.1 ist Boyz damit keine *Einheit in Aufstellung*, und
nach AUF-4.5 darf die *Ablage* nichts kennzeichnen. Derselbe Zustand ist
`testAuf4_5OhneEinheitInAufstellungKennzeichnetDieAblageKeine[nachDerZonenwahl]`, und der
erwartet kein Abzeichen. Die beiden Tests widersprechen sich, einer bleibt immer rot.

**Kosten.** Der Implementierer kann AUF-4.5 nicht grün bekommen, ohne gegen AUF-7.1 zu
verstoßen. Der Fall „kein Modell gesetzt“ ist schon durch den Ohne-Test belegt.

**Gegenvorschlag.** Den Parameter `keinGesetzt` streichen. Statt 0 eine Zahl ab 1 nehmen,
etwa `[1, 3, 10]` mit `einGesetzt`. Dann deckt der Test genau „solange es eine gibt“ ab,
vom ersten *gesetzten* *Modell* an.

**Stellungnahme.**
Befund trifft zu: `keinGesetzt` widerspricht AUF-7.1 und dem Ohne-Test. Umgesetzt in `auf4Test.py`: Parameter `[1, 3, 10]` mit ids `einGesetzt`, `dreiGesetzt`, `alleGesetzt`; der Fall ohne gesetztes Modell bleibt im Ohne-Test.
