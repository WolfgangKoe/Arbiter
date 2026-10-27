# Katalog: Datenblätter und Ausgangslage

Übersicht und Schichten: [Architektur](../architektur.md).

- **A3** Katalogdaten stehen nur als YAML in `domaene/daten/`, `katalog/` liest sie
  (`yaml.safe_load`, nach K5). Prüft: nur Text; Auslöser: erstes Modul in `speicher/`.

## Gliederung
Auslöser der Tests zu K1, K3 bis K5: das Item, das `katalog/` auf diese Gliederung umstellt.
- **K1** `domaene/daten/katalog/<fraktion>/` hält je Art eine Datei (`datenblaetter.yaml`,
  später `waffen.yaml`), der Ordner heißt wie die Fraktion in camelCase. Die Ausgangslage
  nennt je *Einheit* nur `fraktion` (ein Name kann in zwei Fraktionen stehen), `datenblatt`
  und je Modellart die Zahl ihrer *Modelle*; einen Namen, den die Fraktion nicht kennt, lehnt
  der Start ab. Prüft: Einheitstests in `tests/einheit/katalog/`.
- **K2** Die Ebenen sind fest: Fraktion (Ordner), Art (Datei), Datenblatt, Modellart, Wert.
  Das Profil (`core_rules.txt:561`) und der *Durchmesser* stehen bei der Modellart, auch wenn
  alle gleich sind; was für die ganze *Einheit* gilt, beim Datenblatt. Ergänzt wird nur um
  einen Schlüssel, eine Datei je Art oder einen Fraktionsordner, nie durch Umgliedern.
  Prüft: nur Text, Urteil des Reviewers.
- **K3** `katalog/` führt je Ebene eine Tabelle Schlüssel → Prüfung des Werts; der Schlüssel
  ist der Bezeichner aus dem Glossar. Ein unbekannter Schlüssel ist ein Fehler (so kommt kein
  `oc` hinein), ein fehlender auch: Wer einen Schlüssel einführt, trägt ihn in jedes
  Datenblatt ein. Die Zeile darf vor dem Kriterium kommen, das den Wert liest; die Domäne
  bekommt ihn erst mit diesem. Prüft: Einheitstests je Fall.
- **K4** Ein Wert ist eine Zahl in der Einheit des Glossars, ohne Zeichen (`bewegungsweite: 5`).
  Eine andere Form (Strich `core_rules.txt:565`, Würfel `:483`, Schadensprofil `:586`) bekommt
  er mit der ersten Anforderung, die ihn liest, in seiner Zeile aus K3, unter seinem
  Schlüssel. Prüft: Tabelle aus K3.
- **K5** Datenblätter und Modellarten sind Abbildungen mit ihrem Namen als Schlüssel. Keine
  Datei in `domaene/daten/` hat einen Schlüssel zweimal in einer Abbildung oder Anker und
  Verweise (`&`, `*`); `yaml.safe_load` ließe ein zweites `Boyz` still das erste
  überschreiben. `katalog/` prüft dazu die Knoten aus `yaml.compose`, ohne Untertyp des
  Laders ([Es](../../prozess/praemissen/es.md), L). Prüft: Einheitstest je Fall.
- **K6** Je Wert eine Zeile, die Fundstelle als Kommentar am Ende, die Quellen im Kopf der
  Datei. Eine Fähigkeit steht nur mit Name und Regeltext im YAML; was sie bewirkt, steht im
  Code ihrer Anforderung wie jede Sperre ([Domäne, D4](domaene.md)). Prüft: nur Text, Urteil
  des Reviewers.

Die Form; die Modellarten legt der Anforderungsautor fest:
```yaml
Boyz:                     # katalog/orks/datenblaetter.yaml
  modellarten:
    Ork Boy:
      bewegungsweite: 5   # units.yaml:501
      durchmesser: 32     # orks_boyz.yaml:21
- fraktion: orks          # ausgangslage.yaml, je Einheit
  datenblatt: Boyz
  modelle:
    Ork Boy: 10
```
