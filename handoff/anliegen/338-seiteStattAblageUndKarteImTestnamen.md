# Zwei neue Testnamen sagen „Seite“ und „ausgewählte Modelle“ statt der Begriffe des Kriteriums

338 · Kritik · von Fachkritiker (Domäne) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Geprüft: 978bc13 gegen AUF-5.3 bis AUF-5.10 und QUE-3
([Aufstellen](../../domaene/anforderungen/phasen/aufstellen.md),
[Querschnitt](../../domaene/anforderungen/querschnitt.md)). Die Tests treffen ihre Kriterien;
AUF-5.5 fehlt zu Recht (Plan 4, 320 B). 243 Akzeptanztests grün. Ein Befund, an den Namen:

In `technik/tests/akzeptanz/phasen/aufstellen/auf5Test.py`
- `testAuf5_6DieSeiteKennzeichnetImBeispielDesVertragsDieAusgewähltenEinheiten`: AUF-5.6 sagt
  „Die *Ablage* kennzeichnet jede *ausgewählte* *Einheit*“; die Prüfung liest die Ablage
  (`ausgewählteEinheiten`). *Seite* steht nicht im Glossar.
- `testAuf5_7DieSeiteZeichnetImBeispielDesVertragsDieAusgewähltenModelleAusgewählt`: AUF-5.7
  sagt „Die *Karte* kennzeichnet jedes *gesetzte* *Modell* einer *ausgewählten* *Einheit*“.
  Nach dem [Glossar](../../domaene/glossar.md) ist *ausgewählt* ein Zustand der *Einheit*;
  „ausgewählte Modelle“ gibt es fachlich nicht.

Dasselbe „ausgewählten Modells“ steht schon vor 978bc13 in
`testAuf5_7DieKarteZeichnetDenKreisEinesAusgewähltenModellsAndersAlsEinenNichtAusgewählten`.

**Kosten.** Wer die Testliste gegen die Anforderung liest (Abnahme, Stakeholder), findet die
Begriffe des Kriteriums nicht und liest einen Zustand am *Modell*, den die Domäne nicht kennt.
Schreibt der Implementierer danach `Modell.ausgewählt` statt der Ableitung aus der *Einheit*,
weicht der Code vom Glossar ab ([Wir](../../prozess/praemissen/wir.md), 2).

**Gegenvorschlag.** Umbenennen, die Prüfungen bleiben:
- `testAuf5_6DieAblageKennzeichnetImBeispielDesVertragsJedeAusgewählteEinheit`
- `testAuf5_7DieKarteKennzeichnetImBeispielDesVertragsJedesGesetzteModellDerAusgewähltenEinheiten`
- `testAuf5_7DieKarteZeichnetDenKreisEinesModellsDerAusgewähltenEinheitAndersAlsDieAnderen`

Die Datei hat 19.717 Zeichen; die drei Namen kosten zusammen etwa 30 mehr, sie bleibt unter
20.000. Die Helfer `ausgewählteModelle` und `ausgewählteModelleIm` (Hilfsmodule) lesen das Feld
`ausgewählt` am Modell aus V1; ihre Namen beurteilt der Architekt, nicht ich.

Erledigt, wenn die drei Testnamen die Begriffe von AUF-5.6 und AUF-5.7 tragen.

**Stellungnahme.**
