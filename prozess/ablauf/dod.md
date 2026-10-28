# DoD (Item fertig)

1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`;
   Zeilen und Zweige mindestens 95 % für `technik/arbiter`. Mechanismus:
   `formregeln/abdeckung.py` im Lauf von `python3 -m pytest prozess/pruefungen`.
   Ist in `technik/tests` ein Test rot, gilt die Schwelle nicht: Die Prüfung misst nicht und
   nennt die Zahl der roten Tests (Tests vor dem Code brechen auch geteilte Fixtures).
   Mechanismus: `formregeln/abdeckung.py` (`aussetzung`, `verstoß`).
2. Prüfmechanismen grün: `python3 -m pytest prozess/pruefungen` und SonarLint mit
   `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint`. Was sie prüfen:
   [Formregeln](../regeln/formregeln.md), [Kriterienregeln](../regeln/kriterienregeln.md).
   Urteil: Zeilen, die nur Einheitstests erreichen, beurteilt der Reviewer (Vorbedingung,
   fehlendes Kriterium oder tot); Glossar → Code.
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
sagt kein Verhalten außerhalb einer Vorbedingung zu (Anliegen 1751). Mechanismus:
`mutationsregeln/mutation.py` (Befehle: [Mutationsregeln](../regeln/mutationsregeln.md));
„jeder Überlebende“ und Lesbarkeit: nur Text.

Den vollen Lauf (`--voll`) über alle Module, auch `web/`, startet der Koordinator im
Hintergrund, sobald die DoD über das Inkrement grün ist ([Technikphase](technikphase.md) 4);
ändert sich `technik/` danach, startet er ihn neu. Der Lauf hält nichts auf (Anliegen 6960,
F1); seine Lücken: [Prozessphase](prozessphase.md) 1. Mechanismus: nur Text.
Je fertigem Modul schreibt er eine Zeile ins Protokoll (Modul, Mutanten, Überlebende) und
merkt sich die Ergebnisse, ein unterbrochener Lauf setzt dort fort (6960, F2 und F4).
Mechanismus: nur Text (P9 der [Retro 8](../../handoff/retro.md) baut ihn in `mutation.py`).

Schwellen der Werkzeuge: [Werkzeuge](werkzeuge.md).
