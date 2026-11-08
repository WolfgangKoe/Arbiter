# Domäne: die Fachlogik

[Übersicht](../architektur.md).

## Grundschnitt der Domäne
`arbiter/domaene/` spiegelt `domaene/anforderungen/`:
- Ein Ordner der Anforderungen ist ein Modul (`spielobjekte.py`), ein Paket, sobald eine
  seiner Anforderungen ein Modul hat; darin, was mehrere brauchen (`Aufstellung`,
  `Bewegungsphase`). Die *Schlacht* (`querschnitt/schlachtrunden.py`) führt Zug,
  *Schlachtrunde* und *Phase* und reicht weiter, was eine *Phase* tut.
- Eine Anforderung mit eigenen Regeln der Domäne wird ein gleichnamiges Modul
  (`phasen/aufstellen/auswahl.md` → `auswahl.py`); Anzeige und Bedienung (QUE-2) liegen
  in `web/` und `frontend/`.
- Ohne Anforderung nur die Werkzeuge `sperre.py` (`Sperre`, `Grund`) und `messen.py` (M1).

Wird ein Modul zum Paket, bleiben die Importe dessen, was im Ordnermodul bleibt. Prüft:
kein Modul ohne Spiegel `formregeln/spiegel.py`; was wohin gehört der Reviewer.

## Stelle und Rechnen
- **S1** Eine *Stelle* ist der Mittelpunkt der *Base*, `Stelle(x, y)` in Zoll, Ursprung in
  einer Ecke des Spielfelds; x läuft entlang der ersten Seitenlänge aus `onlyWar.yaml` (44″),
  y entlang der zweiten (60″). Die erste *Aufstellungszone* liegt an der Kante x = 0, die
  zweite an x = 44. Prüft: die Fixture `zone`.
- **S2** Gerechnet wird exakt mit `fractions.Fraction`, ohne Toleranz und ohne Wurzel:
  Durchmesser in ganzen mm, 1″ = 254/10 mm, Abstände als Quadrate verglichen; mit `float`
  überdecken sich zwei berührende Boyz. `web/` rundet jede Zahl einer Anfrage auf die nächste
  `Fraction` mit Nenner bis 10⁶ (`limit_denominator`). Warum: Die Seite schickt *Stellen* als
  double zurück (V8); ungerundet überdeckte ein berührendes *Modell* (BEW-1.7, QUE-1.2).
  Gerundet kommt eine mit Nenner bis 10⁶ exakt an (solche Brüche liegen ≥ 10⁻¹² auseinander,
  das double ≤ 10⁻¹⁴ daneben), eine aus dem Anhalten (S3) bis 1/(2·10⁶)″ daneben.
  Ausnahme: Die Kandidaten der Suche in die freie Fläche (M1) sind `float`, das Urteil
  über sie exakt.
  Prüft: `Stelle` ohne `Fraction` wirft `TypeError` (`spielobjekteTest.py`), die Rundung
  `anwendungTest.py`, die Grenzfälle der Akzeptanztests.
- **S3** Anhalten (AUF-29.1, [V10](vertrag/aufstellen/ziehen.md)): Die Berührung ist eine
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
- **D3** Zustand ändern nur Handlungen und das Auswählen ([V3](vertrag/aufstellen/auswahl.md)).
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
  Berührung (S3) und vor der letzten, der kürzeste Weg in die freie Fläche zwischen Kreisen
  ([Fliegen](vertrag/bewegung/fliegen.md)). Prüft: nur Text; Auslöser: zweite
  Baseform (Etappe 6), dann je Baseform ein Vertragstest.
