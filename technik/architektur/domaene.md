# Domäne: die Fachlogik

Übersicht und Schichten: [Architektur](../architektur.md).

## Grundschnitt der Domäne
`arbiter/domaene/` spiegelt `domaene/anforderungen/`:
- Ein Ordner der Anforderungen ist ein Modul (`spielobjekte.py`), ein Paket
  (`phasen/aufstellen/__init__.py`), sobald eine seiner Anforderungen ein Modul hat. Darin
  liegt, was mehrere seiner Anforderungen brauchen (`Aufstellung`, Spielobjekte).
- Eine Anforderung mit eigenen Regeln der Domäne wird ein gleichnamiges Modul:
  `phasen/aufstellen/auswahl.md` → `phasen/aufstellen/auswahl.py` (`Auswahl`). Anzeige und
  Bedienung (`karte.md`) liegen in `web/` und `frontend/`.
- Ohne Anforderung nur die Werkzeuge `sperre.py` (`Sperre`, `Grund`) und `messen.py` (M1).

Wird ein Modul zum Paket, bleiben die Importe dessen, was im Ordnermodul bleibt. Prüft:
kein Modul ohne Spiegel `formregeln/spiegel.py`; was wohin gehört der Reviewer.

## Stelle und Rechnen
- **S1** Eine *Stelle* ist der Mittelpunkt der *Base*, `Stelle(x, y)` in Zoll, Ursprung in
  einer Ecke des Spielfelds; x läuft entlang der ersten Seitenlänge aus `onlyWar.yaml` (44″),
  y entlang der zweiten (60″). Die erste *Aufstellungszone* liegt an der Kante x = 0, die
  zweite an x = 44. Prüft: die Fixture `zone`.
- **S2** Gerechnet wird exakt mit `fractions.Fraction`, ohne Toleranz und ohne Wurzel:
  Durchmesser in ganzen mm, 1″ = 254/10 mm, Abstände als Quadrate verglichen. Mit `float`
  überdecken sich zwei berührende Boyz. `web/` übersetzt jede Zahl einer Anfrage in die
  nächste `Fraction` mit Nenner höchstens 10⁶ (`limit_denominator`, höchstens 1/(2·10⁶)″
  daneben). Warum: Der Spielstand zeigt *Stellen* als double, die Seite schickt sie so zurück
  (V8); ohne Rundung käme etwa x = 160/127 um die letzte Ziffer des double verschoben an, und
  ein berührendes *Modell* überdeckte (BEW-1.7, BEW-2.6). Eine *Stelle* mit Nenner bis 10⁶
  kommt exakt zurück: Zwei solche Brüche liegen mindestens 10⁻¹² auseinander, ein double auf
  dem Spielfeld höchstens 10⁻¹⁴ daneben. Eine *Stelle* aus dem Anhalten (S3) kann einen
  größeren Nenner haben und kommt dann bis 1/(2·10⁶)″ daneben zurück.
  Prüft: `Stelle` ohne `Fraction` wirft `TypeError` (`spielobjekteTest.py`), die Rundung
  `anwendungTest.py`, die Grenzfälle der Akzeptanztests.
- **S3** Anhalten (AUF-29.1, [V10](vertrag/aufstellen.md)): Die Berührung ist eine
  Wurzel, darum hält Arbiter auf einem Raster des Wegs an: Anteil k/n mit
  n = ⌈100 · (|Δx| + |Δy|)⌉, das größte k vor der ersten Überdeckung, exakt nachgeprüft (S2);
  so liegt der Halt höchstens 1/100″ vor der Berührung, wie die *Formation* (`setzenPerKlick.py`).
  Vorbild: `ArbiterMap/backend/app/domain/geometry.py:942`. Prüft: V10, Unit-Tests zu `messen.py`.

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, `@dataclass(eq=False)`. Werte
  (`Stelle`, `Base`) nach Inhalt. Prüft: Akzeptanztests (gleiche Armeen, gleiche Stellen).
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand; so überspringt
  ein Übergehen die Prüfung und protokolliert. Prüft: je Handlung und Grund ein
  Akzeptanztest auf den unveränderten Zustand.
- **D3** Zustand ändern nur Handlungen und das Auswählen ([Vertrag, V3](vertrag/aufstellen.md)).
  Spielobjekte sind `frozen`, Sammlungen Tupel oder `MappingProxyType`. Die Phase hält ihren
  Zustand in `_`-Feldern, lesbar über Properties ohne Setter oder Abfragen
  (`aufstellung.gesetzt(modell)`). Andere Schichten lesen keine `_`-Felder; `web/` ändert
  Attribute nur an `self`, nie per `object.__setattr__`, das `frozen` umgeht.
  Prüft: Python wirft bei der Zuweisung; der Rest nur Text.
- **D4** Gründe, die zusammen gelten, stehen in einer Tabelle Grund → Prüfung oder
  Grund → Befund im Modul ihrer Anforderung (`sperrenBeimSetzen.py`, `beenden.py`); die
  Handlung sammelt ein, ein neuer Grund ist eine Zeile; ein ausschließender Grund bleibt
  Wächter. Prüft: `formregeln/gruendeTabellen.py`
  ([Regeln](../../prozess/regeln/formregeln.md)).
- **M1** Die Baseform kennt in der Domäne nur `messen.py`; Phasen messen nur mit dessen
  Messungen: *überdecken*, *Abstand* höchstens, *ganz in* einer Fläche, der kürzeste Weg,
  der *Bases* gemeinsam *ganz in* eine Fläche rückt, der Anteil eines Wegs bis zur ersten
  Berührung (S3). Prüft: nur Text; Auslöser: zweite
  Baseform (Etappe 6), dann je Baseform ein Vertragstest.
