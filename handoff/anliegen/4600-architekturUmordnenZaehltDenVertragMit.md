# Item architekturUmordnen zählt den Vertrag in die 24.000 Zeichen

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [architekturUmordnen](../../domaene/items/architekturUmordnen.md) sagt „Fertig:
jede Datei unter 6.000 Zeichen, zusammen unter 24.000“. Entschieden hat der Stakeholder in
Anliegen 2570 F2 C anders: die *Regeln* zusammen unter 24.000, der *Vertrag* je Phase eine
Datei zu 6.000, ohne Summe; so steht es auch in den
[Höchstmaßen](../../prozess/kennzahlen.md#höchstmaße). Anliegen 3051, auf das das Item
verweist, sagt „die Regeln zusammen“; im Item fehlt das Wort.

Heute: Regeln 19.851 Zeichen (`architektur.md`, `anwendung.md`, `oberflaeche.md`,
`speicher.md`, `web.md`), Vertrag 12.687 (`handlungen.md`, `vertrag.md`), dazu 4.954 in den
JSON-Beispielen. Nach dem Wortlaut des Items müssten über 8.500 Zeichen weg. Nach 2570 F2 C
wird nur der Vertrag geteilt, gekürzt wird nichts.

Hält auf ([Ich 3](../../prozess/praemissen/ich.md)): Der Fachkritiker nimmt Item 1 nach
seinem „Fertig“ ab. Nach dem Wortlaut nimmt er es entweder nicht ab, oder ich kürze, was der
Stakeholder behalten wollte.

**Kosten.** Ein Satz im Item. Bleibt er so, kürze ich gegen die Entscheidung des
Stakeholders, oder Item 1 bleibt offen, und Item 2 und 3 warten darauf.

**Gegenvorschlag.** Im Item statt „Fertig: jede Datei unter 6.000 Zeichen, zusammen unter
24.000, Prüfungen grün (3051).“:
„Fertig nach den [Höchstmaßen](../../prozess/kennzahlen.md#höchstmaße): Regeln je Datei
unter 6.000 Zeichen, zusammen unter 24.000; der Vertrag je Phase eine Datei in
`technik/architektur/vertrag/` unter 6.000, ohne Summe; Prüfungen grün (2570 F2 C, 3051).“

**Stellungnahme.** Angenommen, in [architekturUmordnen](../../domaene/items/architekturUmordnen.md)
umgesetzt: „Fertig: Regeln je Datei unter 6.000 Zeichen, zusammen unter 24.000; Vertrag je
Datei unter 6.000, ohne Summe ([Höchstmaße](../../prozess/kennzahlen.md#höchstmaße));
Prüfungen grün (3051).“ Kürzer als dein Wortlaut, weil ein Item höchstens 400 Zeichen hat;
„je Phase eine Datei“ steht schon im Umfang, den Ordner nennen die Höchstmaße.
