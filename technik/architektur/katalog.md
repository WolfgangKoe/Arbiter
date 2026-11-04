# Katalog: Datenblätter und Ausgangslage

[Übersicht](../architektur.md).

- **A3** Katalogdaten stehen nur als YAML in `domaene/daten/`, nie in der Datenbank;
  `katalog/` liest sie (K5). Prüft: nur Text; Auslöser: erstes Modul in `speicher/`.

## Gliederung
- **K1** `domaene/daten/katalog/<fraktion>/` hält je Art eine Datei (`datenblaetter.yaml`,
  später `waffen.yaml`), der Ordner heißt wie die Fraktion in camelCase. Die Ausgangslage
  nennt je *Einheit* genau `fraktion` (ein Name kann in zwei Fraktionen stehen), `datenblatt`
  und `modelle`: je Modellart die Zahl ihrer *Modelle*, ganz und über 0. Eine Fraktion ohne
  Ordner, ein Datenblatt, das sie nicht kennt, eine Modellart, die es nicht nennt, lehnt der
  Start ab. Prüft: Einheitstests je Fall.
- **K2** Die Ebenen sind fest: Fraktion (Ordner), Art (Datei), Datenblatt, Modellart, Wert.
  Das Profil (`core_rules.txt:561`) und der *Durchmesser* stehen bei der Modellart, auch wenn
  alle gleich sind; was für die ganze *Einheit* gilt, beim Datenblatt. Ergänzt wird nur um
  einen Schlüssel, eine Datei je Art oder einen Fraktionsordner, nie durch Umgliedern.
  Prüft: nur Text, Urteil des Reviewers.
- **K3** `katalog/` führt je Ebene und für den Eintrag der Ausgangslage (K1) eine Tabelle
  Schlüssel → Prüfung des Werts; der Schlüssel ist der Bezeichner aus dem Glossar. Ein
  unbekannter Schlüssel ist ein Fehler (so kommt kein `oc` hinein), ein fehlender auch: Wer
  einen Schlüssel einführt, trägt ihn in jedes Datenblatt ein. Die Zeile kommt vor den
  Werten und liest den Schlüssel freiwillig, bis jedes Datenblatt ihn trägt; so ist dazwischen
  nichts rot. Sie darf vor dem Kriterium kommen, das den Wert liest; die Domäne bekommt ihn
  erst mit diesem. Ausnahme: Ein Wahrheitswert, den die Quelle nur bei manchen nennt, bleibt
  freiwillig, fehlt er, gilt `false`: `fliegen` beim Datenblatt, `true` nur mit FLY (MIV-3.2,
  `core_rules.txt:871`). Warum: Ein `false` hätte keine Fundstelle (K6). Prüft:
  Einheitstests je Fall.
- **K4** Ein Wert ist eine Zahl in der Einheit des Glossars, ohne Zeichen (`bewegungsweite: 5`),
  oder ein YAML-Wahrheitswert `true`, `false` (`fliegen: true`, gelesen nur als `bool`).
  Eine andere Form (Strich `core_rules.txt:565`, Würfel `:483`, Schadensprofil `:586`) bekommt
  er mit der ersten Anforderung, die ihn liest, in seiner Zeile aus K3, unter seinem
  Schlüssel. Prüft: Tabelle aus K3.
- **K5** Datenblätter und Modellarten sind Abbildungen mit ihrem Namen als Schlüssel. Keine
  Datei in `domaene/daten/` hat einen Schlüssel zweimal in einer Abbildung (`safe_load` ließe
  ein zweites `Boyz` still das erste überschreiben), Anker oder Verweise (`&`, `*`): geprüft
  an den Knoten aus `yaml.compose`, ohne Untertyp des Laders
  ([Es](../../prozess/praemissen/es.md), L). Prüft: Einheitstest je Fall.
- **K6** Je Wert eine Zeile, die Fundstelle als Kommentar am Ende, die Quellen im Kopf der
  Datei. Eine Fähigkeit steht nur mit Name und Regeltext im YAML; was sie bewirkt, steht im
  Code ihrer Anforderung wie jede Sperre ([Domäne, D4](domaene.md)). Prüft: nur Text, Urteil
  des Reviewers.

Die Form zeigen [orks/datenblaetter.yaml](../../domaene/daten/katalog/orks/datenblaetter.yaml)
und [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml); die Modellarten legt der
Anforderungsautor fest.

## Aufbau
- **K7** Je Modul eine Aufgabe, Fehler als `ValueError`: `yamlLesen.py` liest jede Datei aus
  `domaene/daten/` nach K5, `eintragLesen.py` hält die Prüfungen eines Eintrags, die mehr
  als ein Modul nutzt (Tabelle nach K3, Abbildung nach K5, ganze Zahl über 0),
  `datenblaetter.py` liest die Datenblätter einer Fraktion nach K3, K4,
  `ausgangslage.py` baut die Ausgangslage, ohne Datei prüfbar (`ausgangslageAus`), aus den
  Dateien `ausgangslageLaden()`. Die Domäne bekommt,
  was MIV-1.5 liest: je *Modell* `modellart`, den Namen; die *Einheit* heißt wie ihr
  *Datenblatt*, ihre *Modelle* in der Folge von `modelle`; mit MIV-3.2 je *Einheit* `fliegen`
  (`bool`, Vorgabe `False`). Die *Fraktion* nicht (K3), der
  Spielstand bleibt. Prüft: Einheitstests `tests/einheit/katalog/<modul>Test.py`, MIV-1.5, MIV-2.1 und
  MIV-3.2 je ein Akzeptanztest an `ausgangslageLaden()`; die Schnittstelle nur Text.
