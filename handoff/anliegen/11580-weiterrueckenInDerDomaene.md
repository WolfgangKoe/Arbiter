# Weiterrücken in der Domäne

Form: Fragen
Von: Testautor
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Vertrag zu Item [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md)
([Aufstellen · Ziehen](../../technik/architektur/vertrag/aufstellen/ziehen.md),
[Bewegung · Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md)) lässt für die
Tests an der Domäne offen:
1. In welchem Modul stehen `Weiterrücken` und `Gezeigt`, und wie heißen ihre Felder beim
   Erzeugen (`Weiterrücken(zuvor=…, angehaltenAufDemWeg=…)`)?
2. Wie lautet `Schlacht.stellenBeimLoslassen` mit `weiter`, und gibt es `Gezeigt` zurück?
   Wie nimmt `Schlacht.modellLoslassen` `weiter` neben `übergehen` an? Die Seite ruft beide
   über `spiel()` gleich auf (`web/anwendung.py`).
3. Ist `weiter` ein Standardargument (`None`)? „so bleiben die bisherigen Aufrufe“ passt nicht
   zu `Gezeigt` als Ergebnis: 7 Aufrufe von `Aufstellung.stellenBeimLoslassen` in
   `loslassenOhneZielTest.py`, `blockAlsGanzesTest.py`, `anhaltenAnEinerBaseTest.py` und 6 von
   `Schlacht.stellenBeimLoslassen` in `normaleBewegungTest.py`, `uebergehenBeimZiehenTest.py`,
   `anhaltenVorDerGrenzeTest.py` lesen das Ergebnis als Zuordnung *Modell* → *Stelle*.

**Kosten.** Bis zur Antwort prüfen die Tests zu AUF-29 und BEW-17 über den Dienst (V10, V5);
an der Domäne nur, was ohne `weiter` gilt. Mit `Gezeigt` werden die 13 Aufrufe rot, ohne dass
der Implementierer sie ändern darf.

**Gegenvorschlag (Empfehlung).** `Weiterrücken` und `Gezeigt` in
`querschnitt/anhaltenAufDemWeg.py` (dort steht das Gleiten), `weiter: Weiterrücken | None =
None` bei `Aufstellung` und `Schlacht` gleich, beide `stellenBeimLoslassen` geben `Gezeigt`
zurück; ich stelle die 13 Aufrufe auf `.stellen` um, sobald die Kritik an den gesperrten
Dateien endet.

**Stellungnahme.** Angenommen wie dein Gegenvorschlag; der Satz „so bleiben die bisherigen
Aufrufe“ war falsch und ist gestrichen. Steht jetzt in
[Aufstellen · Ziehen](../../technik/architektur/vertrag/aufstellen/ziehen.md), die
[Bewegung](../../technik/architektur/vertrag/bewegung/ziehen.md) verweist darauf:
1. `querschnitt/anhaltenAufDemWeg.py`, beide unveränderlich: `Weiterrücken(zuvor: Stelle |
   None, angehaltenAufDemWeg: bool)`, `zuvor=None` heißt die *Stelle* vor dem Ziehen;
   `Gezeigt(stellen: Mapping[Modell, Stelle], angehaltenAufDemWeg: bool)`.
2. `stellenBeimLoslassen(modell, stelle, weiter=None) -> Gezeigt` und
   `modellLoslassen(modell, stelle, weiter=None) -> None`, bei `Aufstellung` und `Schlacht`
   gleich. Einen Parameter `übergehen` gibt es nicht mehr: Er entfällt mit V18
   ([Gemeinsam übergehen](../../technik/architektur/vertrag/schlacht/uebergehen.md)), der
   Implementierer baut ihn gerade aus; übergangen wird nur mit `gemeinsamÜbergehen()`. So
   ruft `web/` beide Methoden über `spiel()` mit denselben drei Argumenten auf.
3. Ja, `weiter: Weiterrücken | None = None`; `None` gilt wie `Weiterrücken(None, False)`,
   `web/` übergibt `None`, wenn die Anfrage keine der Eingaben nennt. Bei *Neben der Karte*
   nach AUF-16.7 gibt `stellenBeimLoslassen` `Gezeigt({}, False)` zurück.

Die 13 Aufrufe stellst du auf `.stellen` um, wie du vorschlägst; bitte vor dem Code, dann
sind sie rot wie jeder Test vor seinem Code und nicht durch den Implementierer. Verworfen:
`Gezeigt` als Untertyp von `Mapping` mit Zusatzfeld hätte die 13 Aufrufe gelassen, hielte
aber den Vertrag von `Mapping` nicht (zwei solche mit gleichen `stellen` wären gleich, obwohl
`angehaltenAufDemWeg` verschieden ist; Es, L).
