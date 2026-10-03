# Importvertrag lässt relative Ausbrüche durch, Freigabe-Antwort kippt bei jeder Änderung

125 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 89364ab und 1b2a3f9 (Kritik am Code).

**Befund.**
1. `importvertrag.py` (`importierteModule`) lässt jeden relativen Import durch. In
   `domaene/sperre.py` führt `from ..katalog import ausgangslage` aus `arbiter.domaene`
   heraus, in `domaene/phasen/` ebenso `from ...katalog.ausgangslage import x`. Nachgestellt:
   `verstöße` liefert `[]`. Der Docstring „relative Importe bleiben im Paket“ stimmt nicht;
   123 verlangte „relativ eingeschlossen“, also aufgelöst.
2. `seitFreigabeUnverändert` wertet jede Änderung nach der Freigabe als neue Frage. Ersetzt
   `erledigteLoeschen.py` (`linksErsetzen`, sucht auch in `handoff/`) einen Link auf ein
   gelöschtes Anliegen, oder ergänzt der Absender eine Notiz vor `beantwortet`, ist wieder
   der Stakeholder dran, obwohl die Freigabe geantwortet hat: der Fall 83, den 121 beheben soll.
3. Drei Fassungen von „letzte Freigabe“: `jüngsteFreigabe` (Etappe|Plan|Retro),
   `codekritik.commitsSeitDerFreigabe` (jeder Betreff `Freigabe …`) und die Schleife in
   `freigabeCommit`. `dran` und `offeneAnliegenJeRolle` rufen je Anliegen an den Stakeholder
   `jüngsteFreigabe` (ganzes `git log`) und drei weitere git-Aufrufe; der Stand läuft in
   mehreren Hooks.
4. `domaeneOrdner = "technik/arbiter/domaene"` steht in `glossar.py` und `importvertrag.py`.
   Wandert der Ordner, ist `testDieDomäneDesReposHältDenVertrag` still grün (`rglob` auf
   nichts).
5. [wir.md](../../prozess/praemissen/wir.md), Regel 8: „Docstrings höchstens einzeilig“.
   Zweizeilig: `wartetAuf`, `seitFreigabeUnverändert`, Modul-Docstring `importvertrag.py`.
   `wartetAuf` und die Zeile in `prozess/regeln.md` sagen „Fragen an den Stakeholder“; Code und
   [Ablauf](../../prozess/ablauf.md#anliegen) gelten für jedes Anliegen an ihn.
6. Klein: `kennzahlen.py` baut `zeilen = []` und hängt sofort an (Listenliteral reicht);
   `konfigurationTest.py` liest `pyproject()` zweimal; `requires-python` wiederholt
   `target-version = "py312"` von ruff, das ruff aus `requires-python` ableitet.

**Kosten.** Zu 1: A1 bleibt mit einer Zeile umgehbar, ohne dass eine Prüfung rot wird. Zu 2:
Antworten bleiben liegen, sobald ein Hook die Datei anfasst. Zu 3: Codekritik und Dran können
verschiedene Freigaben meinen; vier Subprozesse je Anliegen in jedem Stand. Zu 4 bis 6:
doppelte Pflege, Regelbruch, Wortlaut weicht ab.

**Gegenvorschlag.**
1. Relative Importe auflösen: Paket der Datei aus ihrem Pfad unter `technik/`, `level - 1`
   Teile abschneiden, Modul anhängen, dann `erlaubt`. Scheiter-Test: `from ..katalog import x`
   in `domaene/sperre.py` rot, `from ..sperre import Sperre` in `domaene/phasen/` grün.
2. Statt „Datei unverändert“: Der Kopf lag im Freigabe-Commit schon so vor
   (`git show <freigabe>:<pfad>`, `kopfAusText`, gleiche Runde, `offen`). Eine neue Runde des
   Absenders bleibt beim Stakeholder, Linkersatz und Notizen nicht. Ein git-Aufruf statt
   drei. Ändert das die Regel in `prozess/ablauf.md`, geht es als Anliegen an den
   Organisationsentwickler.
3. Eine Funktion „letzte Freigabe“ in `gitAufruf.py`, die `codekritik.py` und `anliegen.py`
   nutzen, mit einer Festlegung, welche Betreffe zählen; in `dran` einmal je Aufruf.
4. Eine Konstante, die `glossar.py` und `importvertrag.py` teilen; die Repo-Probe prüft, dass
   der Ordner existiert.
5. Docstrings einzeilig, Rest in den Namen; „Anliegen an den Stakeholder“ wie im Ablauf.
6. Nach Ermessen.

**Stellungnahme.** Alle sechs Punkte umgesetzt, Scheiter-Tests in `importvertragTest.py`
und `anliegenTest.py`; Einträge in `prozess/regeln.md`. Zu 2: Die Regel in `ablauf.md` ist
enger als „unverändert“ (gleiche Runde); der Organisationsentwickler passt den Wortlaut an.
Organisationsentwickler: Wortlaut in [Ablauf](../../prozess/ablauf.md#anliegen) angepasst.
