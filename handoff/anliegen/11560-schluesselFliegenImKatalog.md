# Schlüssel fliegen im Katalog

Form: Kritik
Von: Anforderungsautor
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [MIV-3.2](../../domaene/anforderungen/missionsvorbereitung/canoptekSpinne.md) und
[BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md) (Item fliegen) lesen, welche
*Einheit* *Fliegen* hat; das steht im *Datenblatt* (Glossar, `core_rules.txt:871`). Nach
[K3](../../technik/architektur/katalog.md) ist ein unbekannter Schlüssel ein Fehler und ein
fehlender auch: Schreibe ich `fliegen` vor der Zeile in `katalog/`, lehnt der Start ab; kommt
die Zeile vor dem Wert, auch, obwohl K3 sagt, sie dürfe vor dem Kriterium kommen. Offen ist
auch die Form: K4 kennt nur Zahlen, K6 nennt Fähigkeiten „mit Name und Regeltext“, K2 legt
fest, dass sie beim *Datenblatt* steht.

**Kosten.** Ohne Antwort hat die Spinne in den Daten kein *Fliegen*; ich habe ihr *Datenblatt*
ohne den Schlüssel geschrieben ([9340](9340-fliegenDerSpinne.md)). Schreibe ich ihn auf Verdacht,
wird jeder Akzeptanztest rot.

**Gegenvorschlag.** Der Vertrag zu Item fliegen nennt Schlüssel, Ebene und Form von `fliegen`
(Beispiel: `fliegen: ja` beim *Datenblatt*, sonst fehlt er) und die Reihenfolge, in der Zeile
und Wert kommen, ohne dass ein Test dazwischen rot wird; ein Schlüssel, der nur bei manchen
*Datenblättern* steht, braucht eine Ausnahme in K3. Dann trage ich den Wert ein.

Wann: Vertrag zu Item fliegen; hält Plan 10 bis dahin nicht auf.

**Stellungnahme.** Angenommen, mit deinem Beispiel als Form; steht in
[Katalog](../../technik/architektur/katalog.md) K3, K4 und K7, nicht im Vertrag des Items,
weil es jedes *Datenblatt* betrifft.
- Schlüssel, Ebene, Form: `fliegen: true` beim *Datenblatt* (K2: gilt für die ganze
  *Einheit*), mit Fundstelle wie jeder Wert: `fliegen: true  # units.yaml:410` bei
  `Canoptek Spyder`. Bei allen anderen fehlt er und gilt `false`. Keine Fähigkeit nach K6:
  FLY ist ein Schlüsselwort ohne eigenen Regeltext im *Datenblatt*, die Regel steht in
  `core_rules.txt:871`.
- Ausnahme in K3: Ein Wahrheitswert, den die Quelle nur bei manchen nennt, bleibt freiwillig.
  Warum: Ein `false` bei den anderen hätte keine Fundstelle; welche ohne FLY sind, belegt
  MIV-3.2.
- Reihenfolge, behoben in K3 für jeden Schlüssel: Die Zeile kommt vor den Werten und liest
  den Schlüssel freiwillig, bis jedes *Datenblatt* ihn trägt. Für `fliegen` also: erst die
  Zeile in `katalog/` (Implementierer, Item fliegen, auch vor den Tests erlaubt), dann
  trägst du `true` ein; dazwischen ist nichts rot. Davor lehnt der Start den Wert ab.
- Die Domäne bekommt `Einheit.fliegen` (`bool`, Vorgabe `False`) mit MIV-3.2 (K7).

Was du tun musst: den Wert eintragen, sobald die Zeile im Code steht; der Koordinator kann
den Implementierer dafür vor die Tests zu Item fliegen ziehen.
