# DoD (Item fertig)

1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`;
   Zeilen und Zweige mindestens 95 % für `technik/arbiter`. Mechanismus:
   `formregeln/abdeckung.py` im Lauf von `python3 -m pytest prozess/pruefungen`.
   Ist in `technik/tests` ein Test rot, gilt die Schwelle nicht: Die Prüfung misst nicht und
   nennt die Zahl der roten Tests (Tests vor dem Code brechen auch geteilte Fixtures).
   Mechanismus: `formregeln/abdeckung.py` (`aussetzung`, `verstoß`).
2. Prüfmechanismen grün. Mechanismus: Benennung und Spiegel (`formregeln/benennung.py`), Kriterium ↔
   Test (`kriterienregeln/rueckverfolgung.py`: Kennung höchstens einmal je Datei; ein Kriterium ohne Test ist
   rot, sobald ein offenes Item eines freigegebenen Plans es nennt, vorher nennt es der
   Stand), Komplexität (`formregeln/werkzeugaufruf.py`, `complexipyAufrufen`), Code →
   Glossar (`formregeln/glossar.py`), Kommentare und Docstrings nach `prozess/praemissen/es.md` 8
   (`formregeln/kommentare.py`), toter Code (vulture über `technik/arbiter` und
   `technik/tests/akzeptanz`, ohne Einheitstests: `unbenutzterCode` in `formregeln/abdeckung.py`), alle
   im Lauf von `python3 -m pytest prozess/pruefungen`, ruff dort über `formregeln/werkzeugaufruf.py` (`ruffAufrufen`);
   SonarLint (Standardprofil ohne Namensregeln, Ordner nach [Formregeln](../regeln/formregeln.md)) mit
   `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint`, beim Commit als Hook
   `sonarlint` ([Formregeln](../regeln/formregeln.md), Anliegen 216); Höchstmaße nur Text ([Kennzahlen](../kennzahlen.md)). Urteil: Zeilen,
   die nur Einheitstests erreichen, beurteilt der Reviewer (Vorbedingung, fehlendes
   Kriterium oder tot); Glossar → Code.
3. Item gelöscht, die Anforderung beschreibt das gebaute Verhalten. Mechanismus: nur Text.
4. Review geschrieben, Fachkritik hat gegen Ziel, Etappe und Kriterien abgenommen (Urteil).
   Mechanismus: nur Text.

Bei einer Oberfläche gelten auch Bildschirmtest grün, Mockup gelöscht. Dazu die
Mutationsschwelle: mindestens 95 % gefangene Mutanten in den geänderten Zeilen der
Domänenmodule. Je Mutant laufen nur die Tests, die seine Zeile ausführen (Zeilen auf
Modulebene, Tests in einem eigenen Prozess: alle); ein Ergebnis gilt, solange `technik/`,
`pyproject.toml` und `domaene/daten` gleich sind (Merkzettel `.git/arbiter/mutation.json`).
Unter 95 % wird jeder Überlebende angegangen, nicht nur bis zur Schwelle: ein Test, der ihn
fängt, oder, ist er gleichwertig, eine Begründung in `mutationsregeln/gleichwertig.json`, dann
zählt er nicht (Anliegen 1740). Code ändert sich dafür nur, wenn er lesbarer wird; ein Test
sagt kein Verhalten außerhalb einer Vorbedingung zu (Anliegen 1751). Der volle Lauf (`--voll`)
über alle Module, auch `web/`, läuft nur in der Prozessphase ([Schritt 1](prozessphase.md)) und
hält nichts auf. Mechanismus: `mutationsregeln/mutation.py` (Befehle:
[Mutationsregeln](../regeln/mutationsregeln.md)); „jeder Überlebende“ und Lesbarkeit: nur Text.

Schwellen der Werkzeuge: [Werkzeuge](werkzeuge.md).
