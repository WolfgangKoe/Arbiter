# Vertrag: Schlacht · Tür

Abschnitt der *Schlacht* nach der *Aufstellung* (QUE-9, QUE-10), die anderen:
[Architektur](../../../architektur.md#schichten); was alle Phasen teilen:
[Querschnitt](../querschnitt/).

- **V11** Die Tür der Domäne nach der *Aufstellung* ist `Schlacht(aufstellung)` in
  `arbiter/domaene/querschnitt/schlachtrunden.py`, mit `Phase` (Wert: Name aus dem Glossar,
  `Phase.kommandophase.value == "Kommandophase"`, wie `Grund`). Sie übernimmt beim Bau die
  *Stellen* der beendeten *Aufstellung* (AUF-1.7); danach gehören sie ihr, gelesen mit
  `schlacht.stelle(modell)`. Die *Aufstellung* ändert sich nicht mehr; Zonen und Ausgangslage
  liest `web/` weiter an ihr (W2). Abfragen: `ausgangslage` (wie `Aufstellung`), `ersterZug`,
  `amZug`, `schlachtrunde`, `phase`, `beendet`, `inKohärenz(einheit)` (QUE-4), dazu die der
  *Auswahl* wie `Aufstellung` ([V3](../aufstellen/auswahl.md)). Die Regeln der
  *Bewegungsphase* liegen in `phasen/bewegung/` ([Grundschnitt](../../domaene.md));
  `Schlacht` gibt ihnen Ziehen und Beenden weiter, außerhalb der *Bewegungsphase* ändert
  Loslassen nichts, ohne `Sperre` (QUE-10.5). `Schlacht` unterscheidet die *Phase* per `if`
  (Es 9); hat eine zweite eigenes Verhalten, wird jede ein Typ, an den `Schlacht` übergibt
  (Es, O). Prüft: nur Text; Auslöser: Item dieser zweiten *Phase*.
- `web/` hält die *Aufstellung* und, sobald sie beendet ist, genau eine `Schlacht` aus ihr;
  `anwendungFür(aufstellung, schlacht=None)`, `serverStarten(aufstellung, port=0, *,
  schlacht=None)`. Fehlt `schlacht` bei beendeter *Aufstellung*, baut `web/` sie beim ersten
  Bedarf. Danach gehen V5, V10, V14 und `karteAnklicken` an die `Schlacht`, nicht mehr an die
  *Aufstellung*. Vor dem Ende der *Aufstellung*: V12
  und V13 404. Warum in `web/`: Es steckt nur zusammen wie `__main__.py`; mit dem Umbau
  ([Anwendung](../../anwendung.md)) zieht es in den Dienst.
