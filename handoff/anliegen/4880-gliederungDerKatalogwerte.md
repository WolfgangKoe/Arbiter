# Gliederung der Katalogwerte als Regel

Form: Kritik
Von: Architekt
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder hat in [4800](4800-ablageDerKatalogwerte.md) entschieden: YAML in
`domaene/daten/` (F1 A), nur Werte, je Datenblatt seine Modellarten mit eigenem Profil (F2 B),
Werte je Etappe nach Bedarf (F3 A), mit Auflage: „eine Struktur anlegen, die wir jederzeit
passend ergänzen oder bei Bedarf beliebig füllen können, ohne dass die Systematik bricht“.
[Katalog](../../technik/architektur/katalog.md) hat dazu nur A3. Eine Probe zeigt ein Loch:
`yaml.safe_load("Boyz: {b: 5}\nBoyz: {b: 6}")` ergibt `{'Boyz': {'b': 6}}`, ein doppelt
eingetragenes Datenblatt überschreibt still das erste.

**Kosten.** Die Regeln der Architektur ändern sich nur in der Technikphase. Fehlen sie nach
Zyklus 8, schreibt der Anforderungsautor in der Domänenphase 9 die Datenblätter ohne Vorgabe
([4881](4881-datenblaetterImGlossarUndInDenDaten.md)), oder er wartet einen Zyklus.

**Gegenvorschlag.** In `technik/architektur/katalog.md` unter A3, je mit Prüfung:
- **K1** Katalog und Ausgangslage getrennt: `domaene/daten/katalog/<fraktion>/datenblaetter.yaml`
  hält die Datenblätter, später daneben `waffen.yaml` und `faehigkeiten.yaml`; die
  Ausgangslage nennt je *Einheit* nur Datenblatt und je Modellart die Anzahl. Ein Name, den
  der Katalog nicht kennt, bricht den Start ab. Prüft: Einheitstest in `tests/einheit/katalog/`.
- **K2** Die Gliederung ist fest: Fraktion, Datenblatt, Modellart, Wert. Ergänzt wird nur
  durch einen neuen Schlüssel, eine neue Datei je Art oder einen neuen Fraktionsordner, nie
  durch Umgliedern. Prüft: nur Text, Urteil des Reviewers.
- **K3** `katalog/` führt je Schlüssel eine Zeile: Code-Bezeichner aus dem Glossar, Prüfung
  des Werts (O aus [Es](../../prozess/praemissen/es.md)). Ein unbekannter Schlüssel ist ein
  Fehler (so kommt kein `oc` hinein), ein fehlender auch: Jede Modellart hat jeden Schlüssel
  der Tabelle. Wer einen Wert einführt, trägt ihn für alle vorhandenen Datenblätter ein.
  Prüft: Einheitstests je Fall.
- **K4** Werte sind Zahlen in der Einheit des Glossars, ohne Zeichen (`bewegungsweite: 5`).
  Sonderwerte wie *B* „-“ (`core_rules.txt:565`) bekommen ihre Form mit der ersten
  Anforderung, die sie liest. Prüft: Tabelle aus K3.
- **K5** Datenblätter und Modellarten stehen als Liste mit `name`; ein doppelter Name ist ein
  Fehler (Probe oben). Prüft: Einheitstest.
- **K6** Jeder Wert trägt seine Fundstelle als Kommentar am Zeilenende, die Quelle steht im
  Kopf der Datei; Verhalten einer Fähigkeit steht nie im YAML, sondern im Code ihrer
  Anforderung (4800 F2 B, D4). Prüft: nur Text, Urteil des Reviewers.
- Die Domäne bleibt: `katalog/` baut daraus *Modelle* mit ihren Werten; ein Typ
  *Datenblatt* entsteht in der Domäne erst, wenn ein Kriterium ihn braucht.
- Auslöser für K1, K3, K5: das Item aus [4882](4882-itemKatalogwerteGliedern.md). Bis dahin
  bleibt `ausgangslage.yaml` wie sie ist; Item normalMove liest `bewegungsweite` dort.

Wann: jetzt in der Technikphase 8, nach den Verträgen zu den Items 2 und 3 (sie halten den
Testautor auf), vor der Domänenphase 9. Kosten rund 2.000 Zeichen in `katalog.md`; das
Höchstmaß je Datei steht in den [Kennzahlen](../../prozess/kennzahlen.md#höchstmaße).

**Stellungnahme.** Umgesetzt in [Katalog](../../technik/architektur/katalog.md), K1 bis K6,
A3 darauf abgestimmt. Abweichend vom Gegenvorschlag: Datenblätter und Modellarten sind
Abbildungen statt Listen mit `name`; eine Prüfung der Knoten aus `yaml.compose` (K5, Probe in
`/tmp`) fängt doppelte Schlüssel auf jeder Ebene, auch doppelte Werte einer Modellart.
`fraktion` steht je *Einheit* (K1). K3 lässt eine Zeile vor ihrem Kriterium zu: So lässt sich
der Katalog füllen, bevor ein Kriterium den Wert liest.
