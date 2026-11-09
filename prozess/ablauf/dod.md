# DoD (Item fertig)

1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`;
   Zeilen und Zweige mindestens 95 % für `technik/arbiter`, Zeilen mindestens 95 % für
   `technik/frontend/` (gemessen in den Bildschirmtests). Mechanismus:
   `formregeln/abdeckung.py` im Lauf von `python3 -m pytest prozess/pruefungen`, wie er misst:
   [Formregeln](../regeln/formregeln.md).
   Ist in `technik/tests` ein Test rot, gilt keine Schwelle: Die Prüfung misst nicht und
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

Belege zu 1 und 2, auch „Tests grün“ des Implementierers ([Technikphase](technikphase.md) 3):
Jeder Lauf ist vollständig, ohne `-x` oder `--maxfail`; `prozess/pruefungen` dauert rund elf
Minuten, die Rolle startet ihn im Hintergrund (Anliegen 8042). Schreibt nach ihrem Auftrag
daneben ein Lauf in `technik/` oder `prozess/pruefungen/`, prüft sie auf einem Abzug ihres
Stands: `git clone --no-hardlinks <Projekt> /tmp/<Name>`, darin `.venv` und `node_modules`
als Verweis auf die des Projekts (`ln -s`), `.venv/bin/pre-commit install`, ihre
uncommitteten Dateien vom Projekt aus mit `cp --parents <Datei> /tmp/<Name>`. Ihre Meldung
nennt den Stand: `Stand <Commit> und <n> eigene Dateien` auf dem Abzug, sonst
`Stand <Commit> und Arbeitsbaum` (Anliegen 8022). Mechanismus: nur Text.

Bei einer Oberfläche gelten auch Bildschirmtest grün, Mockup gelöscht.

## Mutationslauf
Er gehört nicht zur DoD und hält nichts auf (Anliegen 6960, F1; 15960). Einmal je Zyklus
startet ihn der Koordinator im Hintergrund nach `Freigabe Review`, neben der Prozessphase:
gezielt über die seit `Freigabe Plan` geänderten Zeilen der Domänenmodule, je Mutant mit den
Tests, die seine Zeile ausführen. Ist mit der Freigabe die Etappe erreicht, läuft an seiner
Stelle der volle (`--voll`, alle Module, auch `web/`; Anliegen 8961). Kein weiterer Lauf,
kein Neustart, wenn sich `technik/` ändert. Mechanismus: nur Text; Befehle, Kerne und
Merkzettel: [Mutationsregeln](../regeln/mutationsregeln.md).
Je fertigem Modul zeigt er seinen Stand im Protokoll, ein unterbrochener Lauf setzt dort fort
(6960, F2 und F4). Mechanismus: `mutationsregeln/mutation.py`.
Schwelle: 95 % gefangene Mutanten. Darunter wird jeder Überlebende angegangen, nicht nur bis
zur Schwelle: ein Test, der ihn fängt, oder, ist er gleichwertig, eine Begründung in
`mutationsregeln/gleichwertig.json`, dann zählt er nicht (Anliegen 1740). Code ändert sich
dafür nur, wenn er lesbarer wird; ein Test sagt kein Verhalten außerhalb einer Vorbedingung
zu (Anliegen 1751). Mechanismus: `mutationsregeln/mutation.py`; „jeder Überlebende“ und
Lesbarkeit: nur Text.
Endet der Lauf, schreibt der [Reviewer](../../.claude/agents/reviewer.md) die Überlebenden
gesammelt als Anliegen, bereit vor der nächsten Domänenphase: fehlt ein Kriterium, an den
Anforderungsautor mit `Wartet auf: Domänenphase`, sonst an den Testautor mit
`Wartet auf: Technikphase` (Anliegen 1671, F2; 15960). Mechanismus: nur Text.

Schwellen der Werkzeuge: [Werkzeuge](werkzeuge.md).
