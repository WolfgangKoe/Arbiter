# Prüfskripte: `pfadeTest.py` hält Listen von Hand, die sich ableiten lassen

147 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Gegenstand: be63161 (Kritik am Code), Folge von [144](144-pfadeTestDeckt.md).
`python3 -m pytest prozess/pruefungen`: 424 grün.

**Befund.**
1. `pfadeTest.py:11`: `prüfTests` zählt drei Prüf-Tests von Hand auf. `cspellTest.py` ist
   ebenso ein Test ohne eigenes Modul, also selbst Prüfung, und fehlt (heute ohne Literal).
   Ein neuer Prüf-Test bleibt ausgenommen, ohne dass jemand es merkt.
2. `pfadeTest.py:10`: `alleOrdner` nimmt nur Namen auf `Ordner`; `prozess/regeln.md` sagt
   „jeder Wert aus `pfade.py`“. Ein Wert `planDatei = "handoff/plan.md"` bliebe ungeprüft.
   `testAlleOrdnerAusPfadeWerdenGeprüft` ist bei leerer Liste grün (`all([])`), etwa nach
   einer Umbenennung der Werte.
3. `pfadeTest.py:46`: `endswith(("Test.py", "pfade.py"))` nimmt jede Datei auf `pfade.py`
   aus (etwa ein künftiges `schreibpfade.py`), vorher nur `pfade.py` selbst.
4. `pfadeTest.py:15`, `pfadSegmente`: erkennt Segmente nur als Operand von `/`.
   `wurzel.joinpath("handoff", "anliegen")`, `Path(wurzel, "domaene", "items")` und
   `f"{wurzel}/items"` bleiben grün (Probe). Heute nutzt kein Prüfskript diese Formen.
5. `kommentare.py:30`: `docstringKnoten` ist als `list[tuple[ast.AST, ast.Expr]]`
   annotiert, hängt aber `teil.body[0]` an (Typ `ast.stmt`); mypy strikt
   ([Ablauf, Werkzeuge](../../prozess/ablauf.md#dod-item-fertig)) meldet das.
   `docstringVerstöße` ruft danach `ast.get_docstring` ein zweites Mal je Knoten.

**Kosten.** 1 bis 3: Die Regel verspricht mehr, als der Test hält; die Lücke öffnet sich
still bei der nächsten Datei oder Umbenennung. 4: klein, solange alle Prüfskripte `/`
nutzen. 5: klein; rot, sobald mypy kommt.

**Gegenvorschlag.**
1. Prüf-Tests ableiten: `*Test.py`, zu dem kein `<name>.py` im Ordner liegt.
2. `alleOrdner` aus allen Zeichenketten von `pfade.py`, deren Name nicht mit `_` beginnt
   (sonst zählen `__doc__` und `__file__` mit); der Test prüft zusätzlich, dass die Liste
   nicht leer ist.
3. `datei.name != "pfade.py"` wie vorher.
4. Die Formen als bekannte Lücke in die Zeile von `regeln.md`, oder `Call` mit Attribut
   `joinpath` und `Path(...)` wie `/` behandeln; ein Scheiter-Test je Form.
5. `docstringKnoten` liefert `(knoten, ausdruck, text)` mit passender Annotation;
   `docstringVerstöße` nutzt `text`.

Erledigt, wenn 1 bis 3 umgesetzt sind, ein Scheiter-Test die leere oder unvollständige
Liste aus 2 rot zeigt, 4 und 5 entschieden sind und `python3 -m pytest prozess/pruefungen`
grün ist.
