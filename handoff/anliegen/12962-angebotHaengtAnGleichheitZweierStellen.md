# Das Angebot nach dem Ziehen hängt an der Gleichheit zweier Stellen

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Am Stand 90a2d9d, ergänzend zu Anliegen 12702, 12903 und 12904:
1. `hältAnDerGrenze` in `Bewegungsphase._gezeigt`
   (`technik/arbiter/domaene/phasen/bewegung/__init__.py`) erschließt durch Vergleich zweier
   getrennt gerechneter *Stellen*, ob BEW-3.1 oder 6.2 anhielt; `anteileAbZuvor` rechnet
   dieselben Anteile, die `gleiten` über `_anteilBisZumAnhalten` schon nahm, noch einmal.
2. `_verschobenUm` (ebenda) ist `_verschoben` aus `phasen/aufstellen/anhaltenAufDemWeg.py`
   (zu 12702, 2).
3. `testEinFremdesModellHinterDerBewegungsweiteLenktDasZiehenZumFreienZielNichtInDieBaseUm`
   (`technik/tests/einheit/domaene/phasen/bewegungTest.py`) prüft, dass das *Modell* vor der
   *Base* anhält; der Name sagt, es werde nicht umgelenkt.

**Kosten.** 1: Das Angebot stimmt nur, solange beide Rechnungen dieselbe *Stelle* ergeben; jede
Änderung an einer (etwa *Fliegen*) muss die andere mitziehen. 2: dieselbe Rechnung zweimal. 3:
Der Leser erwartet einen anderen Fall, als der Test prüft.

**Gegenvorschlag.** 1: Das Ergebnis des Gleitens trägt, welcher Anteil anhielt (29.1 mit Anteil
oder *Base*), und daraus folgt der Wert, den 12904 an `Gezeigt` hängt. 2: die Funktion aus
12702, 2. 3: etwa `testHältDasModellVorDerBaseAnDieInDieBewegungsweiteReicht`.

**Stellungnahme.** Teils erledigt. Punkt 1: `hältAnDerGrenze` kommt aus den `Anteile`
desselben Gleitens (`anhaltenVorFremdenBases.py`), kein Vergleich zweier *Stellen* mehr.
Punkt 3: Der Test mit dem irreführenden Namen steht nicht mehr in `tests/einheit`. Punkt 2
(`verschobenUm` in `normaleBewegung.py` neben `_verschoben` in `anhaltenAufDemWeg.py`) ist ein
Doppel von [12702](12702-gleitenBautVorhandeneHelferNach.md) Punkt 2 und bleibt dort offen.
