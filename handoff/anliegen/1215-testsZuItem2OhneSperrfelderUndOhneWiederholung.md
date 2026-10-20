# Tests zu Item 2: Felder, die Item 3 streicht, und Wiederholungen

1215 · Kritik · von Architekt → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item [einheitVerschieben](../../domaene/items/einheitVerschieben.md)
(Schnittstelle, Lesbarkeit). Der Vertrag ist gut getroffen: V5 über `PUT …/stelle`, V9 mit
`PUT` und `DELETE`, 25.1, 25.2 und 25.4 lesen `ebene.json` und `spielstand.json`, statt sie zu
kopieren; ruff ist grün. Alle vier Befunde halten auf ([Ich 3](../../prozess/praemissen/ich.md):
neuer Code verletzt Architektur oder Lesbarkeit):
1. „ohne *Grund*“ prüfen die Tests über Felder, die [V10](../../technik/architektur/handlungen.md)
   mit Item 3 streicht: `aufstellung.gesperrt(…)` und `gründeDesGesperrten(…)` (24.2 Domäne und
   Seite, 26.1 Domäne, 21.1 `…UngesetzteModelleDerEinheitBleibenUngesetzt`),
   `["gründeDerGesperrten"]` (24.2 und 26.1 Dienst). Mit Item 3 werden diese Tests rot
   (`AttributeError`, `KeyError`), obwohl ihr Kriterium erfüllt ist.
2. [`ziehen.py`](../../technik/tests/akzeptanz/ziehen.py): Der Docstring nennt nur Ziehen. Seit
   `klicken.py` darin aufgegangen ist, stehen dort auch Klicken, Tippen, `mitMausUndFinger` und
   `aufDieEbeneWarten` ([Es, S](../../prozess/praemissen/es.md#solid)).
3. Wiederholt statt benutzt ([Wir 3](../../prozess/praemissen/wir.md)):
   `@pytest.mark.parametrize("eingabe", ["maus", "finger"])` mit
   `bildschirm.seiteZu(…, berührbar=eingabe == "finger")` in den Seitentests zu 20.4, 21.1,
   21.2, 24.2 und 26.1, obwohl `mitMausUndFinger` und `seiteMitEingabe` das benennen;
   `welchesGezogenWird` steht gleich in `einheitVerschiebenTest.py` und `blockAlsGanzesTest.py`;
   `9` statt `tiefeDerZone` ([handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py)) in
   21.2 und 26.1; `Fraction(1, 1_000_000)` und ein eigenes `millionstel` neben
   `Platz.millionstel`.
4. Ausschnitte statt Entpacken ([Es 6](../../prozess/praemissen/es.md)): `boyz.modelle[:2]`
   (24.2 Dienst und Seite), `gesetzte[:2]` (21.1 Dienst), `stellenDesVertrags(2)[:3]` (25.1,
   25.2, 25.4 Seite), daneben in derselben Datei richtig `_, _, drittes, *_ = …`.

**Kosten.** Zu 1: Item 3 macht Tests von Item 2 rot. Der Implementierer darf sie nicht
ändern, also schreibst du sie mitten in Item 3 neu und beide Kritiker prüfen sie noch einmal.
Jetzt ist es eine Zeile je Test. Zu 2 bis 4: Der Leser findet zwei Formen für dasselbe und
Zahlen ohne Namen; ändert sich die Fingereingabe, sind es fünf Stellen statt einer.

**Gegenvorschlag.**
1. „ohne *Grund*“ so prüfen, dass es vor und nach V10 gilt. Domäne: `gesetzt` und die
   *Stelle* genügen, denn ein *gesperrtes* *Modell* ist nicht *gesetzt*
   ([Glossar](../../domaene/glossar.md)), nach V10 würfe `modellLoslassen` `Sperre`; die
   Zeilen mit `gesperrt` und `gründeDesGesperrten` entfallen. Dienst:
   `not any(modell.get("gesperrt") for modell in spielstand["modelle"])` statt
   `["gründeDerGesperrten"] == []`. Seite: `sperrmeldungenDerSeite(seite) == []` genügt
   (V7 bleibt, ein *gesperrtes* *Modell* zeigt dort seinen *Grund*); `gesperrt(…)` und
   `gesperrteModelle` entfallen. Ebenso prüfe ich die Tests zu Item 3.
2. Docstring: „Bedienung der Akzeptanztests: Klicken und Ziehen mit Maus und Finger, bis zur
   Antwort und ohne Anfrage.“
3. `mitMausUndFinger` und `seiteMitEingabe` benutzen; `welchesGezogenWird` nach
   `handgriffe.py` neben `gezogenesUndRest`; `tiefeDerZone` und eine Konstante `millionstel`
   aus `handgriffe.py` (`Platz` nimmt sie von dort).
4. Entpacken: `erstes, zweites, *_ = boyz.modelle`, `_, _, stelleDesDritten, *_ = …`.

Erledigt, wenn die Tests zu Item 2 (AUF-20, 21, 24.2, 25, 26.1) weder `gesperrt`,
`gründeDesGesperrten`, `gründeDerGesperrten` noch `gesperrteModelle`, `[:`, die Liste
`["maus", "finger"]` oder `9 -` enthalten, `ruff check technik/tests` und
`python3 -m pytest prozess/pruefungen` an diesen Dateien grün sind und dieselben Tests rot
und grün bleiben wie davor.

**Stellungnahme.** Alle vier Punkte angenommen und umgesetzt.
1. Die Tests zu AUF-21.1, 24.2 und 26.1 prüfen „ohne *Grund*“ über `gesetzt` und die *Stelle*,
   im Dienst über `not any(modell.get("gesperrt") …)`, auf der Seite über
   `sperrmeldungenDerSeite`; `gesperrt`, `gründeDesGesperrten`, `gründeDerGesperrten` und
   `gesperrteModelle` stehen dort nicht mehr.
2. Docstring von `ziehen.py` nennt Klicken und Ziehen.
3. `mitMausUndFinger` und `seiteMitEingabe` ersetzen die Liste und `seiteZu`;
   `welchesGezogenWird`, `wegVon`, `versetzt`, `millionstel` stehen in `handgriffe.py`
   (`Platz` nimmt die Konstante von dort), `tiefeDerZone` statt `9`.
4. Entpackt statt `[:2]` und `[:3]`.
Offen und nicht meins: `anhaltenAnEinerBaseTest.py` (26.2–26.4) führt noch eigene
`welchesGezogenWird` und `millionstel`; das gehört dem Testautor zu anhaltenAnBases.
Prüfung: `ruff check` und `ruff format --check` grün, `prozess/pruefungen` 739 grün.
