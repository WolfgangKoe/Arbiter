# Prüfskripte: `pfadeTest.py` prüft zwei von fünf Ordnern

144 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: ab7fa0c (Kritik am Code). `python3 -m pytest prozess/pruefungen` grün bis auf
`hoechstmassTest` an 124, das am uncommitteten Arbeitsbaum des Stakeholders liegt (in HEAD
3.951 Zeichen). Die sechs Fundstellen aus 142 nutzen `pfade.py`, `standTest.py` ruft `lage`
einmal.

**Befund.**
1. `pfadeTest.py:9`: `doppelteOrdner = (etappenOrdner, itemsOrdner)`. Die Zeile in
   `prozess/regeln.md` sagt „Ordner, die mehrere Prüfungen kennen, stehen nur in
   `pfade.py`“; `akzeptanzOrdner`, `anforderungsOrdner`, `anliegenOrdner` prüft niemand.
   Probe: mit allen fünf Werten aus `pfade.py` meldet der Test heute nur Docstrings, die er
   ausnimmt; er bliebe grün.
2. `plan.py:23`: `rf"\]\(\.\./{itemsOrdner}/…"` setzt den Ordner ungeschützt in den
   regulären Ausdruck. Heute ohne Folgen; ein Ordner mit `.` oder `+` passt dann auf
   Fremdes oder gar nicht.
3. `pfadeTest.py:12`, `docstringKnoten`: baut nach, was `kommentare.py:33`
   (`docstringVerstöße`) schon über `ast.get_docstring` sucht, und vergisst dabei
   `ast.AsyncFunctionDef`. Probe: `async def f():` mit Docstring `Liest domaene/items/.`
   meldet `pfadeTest` als Literal.
4. `pfadeTest.py:31`: `knoten.value in teile` meldet jedes allein stehende `"items"` oder
   `"etappen"`, auch `daten["items"]` (Probe: Fund `['items']`).
5. `pfadeTest.py:40`: Alle `*Test.py` sind ausgenommen, auch `hoechstmassTest.py`, das
   selbst Prüfung ist und in 142 als Fundstelle stand. Ein Literal dort bleibt grün.

**Kosten.** Zu 1: Die Regel verspricht mehr, als der Test hält; ein Umzug von
`handoff/anliegen` übersieht ein neues Literal, derselbe Fall wie 142. Zu 2: klein, latent.
Zu 3 und 4: falscher Alarm, der zum Umgehen erzieht; zwei Stellen, die Docstrings
erkennen, laufen auseinander. Zu 5: klein, solange nur `hoechstmassTest.py` betroffen ist.

**Gegenvorschlag.**
1. `doppelteOrdner` aus allen Zeichenketten von `pfade.py` bilden (etwa `import pfade` und
   `vars(pfade)`), dann die Zeile in `regeln.md` ohne Aufzählung der Ordner.
2. `re.escape(itemsOrdner)` im Muster.
3. Eine Funktion für die Docstring-Knoten in `kommentare.py`, die `docstringVerstöße` und
   `pfadeTest.py` nutzen; sie schließt `AsyncFunctionDef` ein.
4. Ein allein stehendes Segment nur melden, wenn es auf `"domaene"` folgt (Elternknoten
   `ast.BinOp` mit `/`), oder nur ganze Pfade prüfen und Segmente in `regeln.md` als Lücke
   nennen.
5. Die Prüf-Tests (`hoechstmassTest.py`, `komplexitaetTest.py`, `konfigurationTest.py`)
   einschließen oder die Ausnahme in `regeln.md` nennen.

Erledigt, wenn 1 und 2 umgesetzt sind, ein Scheiter-Test je für `async def` (3) und
`daten["items"]` (4) die Form belegt, 5 entschieden ist und `python3 -m pytest
prozess/pruefungen` grün ist.

**Stellungnahme.** Alle fünf umgesetzt. 1: `pfadeTest.py` bildet die Ordner aus
`vars(pfade)`; `regeln.md` zählt sie nicht mehr auf. 2: `re.escape` in `plan.py`. 3:
`docstringKnoten` steht in `kommentare.py` (mit `AsyncFunctionDef`), `docstringVerstöße`
und `pfadeTest.py` nutzen sie; Scheiter-Test `testEinDocstringEinerAsyncFunktionIstErlaubt`.
4: Ein Segment zählt nur als Operand von `/`; Scheiter-Test
`testEinSchlüsselMitDemNamenDesOrdnersIstErlaubt`. 5: Die drei Prüf-Tests sind
eingeschlossen (`hoechstmassTest.py` nutzte zwei Literale, jetzt `pfade.py`); die übrigen
Tests tragen die Ordner als Testdaten und bleiben ausgenommen, die Ausnahme steht in
`regeln.md`. Pytest grün.

**Nachprüfung.** be63161: 1 bis 5 wie gegenvorgeschlagen; die Scheiter-Tests zu 3 und 4
stehen, `python3 -m pytest prozess/pruefungen` 424 grün. Kleinere Folgebefunde in
[147](147-pfadeTestRest.md). Ich setze `erledigt`.
