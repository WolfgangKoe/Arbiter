# Keine Kohärenz an einer Stelle entschieden

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf (Kritik: neuer Code verletzt Architektur, hier den Vertrag
[V18](../../technik/architektur/vertrag/schlacht/uebergehen.md)), Diff `039da85..b14cdf7`,
Item gemeinsamUebergehen. Geprüft auf `b14cdf7` in `/tmp`: Prüfungen grün, SonarLint ohne
Funde, Tests zu BEW-8, QUE-5, QUE-6 grün; rot nur Tests anderer Items.
1. Wie [8261](8261-uebergehenNachVertragUndAuswahl.md) Punkt 1, dort als wartend
   eingeordnet; aus Sicht der Architektur hält er auf. `Schlacht.modellLoslassen` in
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) setzt,
   wenn `gründe <= übergehen`, ohne `übergehbar` zu fragen. Damit steht die Regel
   „‚keine Kohärenz‘ kann nicht übergangen werden“ ([Ziel](../../domaene/ziel.md), QUE-5.5)
   an zwei Stellen: `Sperre` entscheidet, ob der Knopf erscheint, die *Schlacht* entscheidet
   unabhängig davon, ob übergangen wird. Der Dienst nimmt „keine Kohärenz“ in `übergehen`
   heute schon an.
2. `Schlacht.stellenBeimLoslassen` wirft `Sperre(*gründe, übergehbar=True)`; so trägt auch
   die 409 der Abfrage beim Ziehen (V10) `"übergehbar": true`. V18 bietet das Übergehen nur
   bei `modellLoslassen` an: Die Abfrage ist keine Handlung, es gibt nichts zu übergehen.

**Kosten.** Am Bildschirm heute keine: Beim Ziehen entsteht nie ‚keine Kohärenz‘, und die
Seite liest `übergehbar` bei der Abfrage nicht. Bleibt 1, lässt Arbiter fehlende *Kohärenz*
übergehen, sobald eine *Sperre* beim Ziehen sie meldet, ohne dass ein Test rot wird; bleibt
2, zeigt eine Seite, die der Antwort der Abfrage glaubt, einen Knopf ohne Handlung. Je eine
bis drei Zeilen.

**Gegenvorschlag.**
1. Wie 8261 Punkt 1: in `modellLoslassen` die *Sperre* einmal bilden,
   `sperre = Sperre(*gründe, übergehbar=True)`, und sie werfen, wenn
   `not (sperre.übergehbar and gründe <= übergehen)`. Dann entscheidet nur `Sperre`, und
   `sperreTest.py` prüft die Regel schon.
2. In `stellenBeimLoslassen` `raise Sperre(*gründe)` ohne `übergehbar`.

**Stellungnahme.**
