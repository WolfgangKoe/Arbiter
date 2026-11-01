# Ein Testlauf, der grün meldet, braucht einen festen Stand

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder fand die Schwankung der roten Tests der *Leisten*
([leistenTest.py](../../technik/tests/akzeptanz/querschnitt/leistenTest.py)) ungeklärt. Hält auf
nach [Kritik](../../prozess/ablauf/kritik.md): „Tests grün“ des Implementierers ist der Beleg im
Fortschritt, und der Beleg hängt heute davon ab, wer gerade daneben schreibt.
1. Auf dem Stand von Commit `0015ae7` (in `/tmp` ausgepackt, `git archive`) ist
   `leistenTest.py` dreimal gleich rot: 6 Fehlschläge, 15 Fehler im Aufbau; die *Leiste*
   *Protokoll* fehlt noch (Item gemeinsamUebergehen). Der Test selbst schwankt nicht, er
   startet den Befehl auf einem freien Port.
2. Derselbe Gesamtlauf `python3 -m pytest technik/tests` ergab auf `0015ae7` 327 rote
   Tests und 15 Fehler, im Arbeitsbaum zur selben Zeit 373 und 24: Dort ändern Testautor und
   Implementierer gleichzeitig Tests und Code.
   [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md) 1 trennt nur die
   Dateien, die ein Lauf schreibt; ein Testlauf liest aber alle Tests und den ganzen Code.
3. Mit `-x` endet ein Lauf am ersten roten Test; welche Tests rot sind, sieht man dann nur
   bis dahin, je nach Stand verschieden. Der Stakeholder sah, dass der Implementierer
   `prozess/pruefungen` nicht vollständig ohne `-x` laufen ließ.

**Kosten.** Bleibt es, meldet eine Rolle grün oder rot für einen Stand, den es so nie gab;
der Stakeholder sucht dann einen Fehler im Test, der in einem Nachbarlauf liegt. Token: ein
Satz im Ablauf; ein Lauf auf einem Abzug kostet rund 6 Minuten wie heute.

**Gegenvorschlag.** Bestehende Regel anpassen (Ich 4): in
[Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md) ergänzen, dass ein Lauf, der
Tests oder Prüfungen als Beleg meldet („Tests grün“, [DoD](../../prozess/ablauf/dod.md) 1 und
2), entweder allein am Arbeitsbaum läuft oder auf einem Abzug seines Stands, und immer ohne
`-x`; seine Meldung nennt den Stand. Bis dahin genügt, dass der Koordinator „Tests grün“ nicht
neben einem Lauf des Testautors startet. Ob du daraus einen Mechanismus machst, entscheidest
du mit dem Regelumsetzer.

**Stellungnahme.** Umgesetzt mit P2 der [Retro 9](../retro.md), bestehende Regel angepasst
(Ich 4): [DoD](../../prozess/ablauf/dod.md), Absatz „Belege zu 1 und 2“, gilt auch für
„Tests grün“ (Technikphase 3 verlinkt DoD 1, 2): Läufe vollständig, ohne `-x`; schreibt nach
dem Auftrag daneben ein Lauf in `technik/` oder `prozess/pruefungen/`, prüft die Rolle auf
einem Abzug; die Meldung nennt den Stand. [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md)
verlinkt den Absatz, statt ihn zu wiederholen (Wir 3).
- Abzug erprobt: `git clone --no-hardlinks` nach `/tmp`, `.venv` und `node_modules`
  verlinkt, `pre-commit install` (`git archive` fehlt das `.git` mancher Prüfungen). Auf
  `90801c5`: `technik/tests` 6:27 min, `prozess/pruefungen` 10:10 min. Auf `1ff5ee3`: ein
  Fehler, der nur im Abzug in `technik/arbiter` steht, macht dort die Tests rot; der Abzug
  prüft also seinen Code, nicht den des Projekts.
- Mechanismus: nur Text. `isolation: worktree` von Claude Code zweigt vom Standardzweig ab
  und verlangt Zusammenführen: zu teuer. Ein Skript erst, wenn es wieder vorkommt.
