# SonarLint scharf, Abdeckung 95 % ohne toten Code

150 · Kritik · von Stakeholder → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
**Befund** (übermittelt vom Koordinator). „Kritik an den Organisationsentwickler: Haben wir
denn schon Sonarlint scharf gestellt? Wie können wir die Code-Qualität nachhaltig hoch
halten? Die Testabdeckung müssen wir messen und bei mindestens 95% halten, aber gleichzeitig
sicherstellen, dass wir damit keinen toten Code am Leben halten.“

**Stellungnahme (Organisationsentwickler).** Angenommen in allen Punkten, umgesetzt als
Prozess-Items P1 und P2 der Retro 2; beide nennt
[DoD 1 und 2](../../prozess/ablauf.md#dod-item-fertig).
1. **SonarLint:** `sonarlint.py` startet den Analysator deiner VS-Code-Erweiterung ohne
   VS Code, Standardprofil ohne die Namensregeln (camelCase); heute keine Funde.
2. **Abdeckung:** Zeilen und Zweige mindestens 95 % für `technik/arbiter` und, als eigene
   Meldung, für `prozess/pruefungen` (`abdeckung.py`).
3. **Kein toter Code am Leben:** vulture über Produkt und Akzeptanztests, ohne
   Einheitstests (`unbenutzterCode`). Zeilen, die nur Einheitstests erreichen, beurteilt der
   Reviewer in der DoD: Vorbedingung, fehlendes Kriterium oder tot. Ob ein Test Code prüft,
   statt ihn nur auszuführen, zeigen erst Mutationstests (DoD, letzter Absatz); ich schlage
   sie vor, sobald ein Befund es verlangt.
4. **Nachhaltig:** Was eine Prüfung sperrt, hält; was nur Text ist, verfällt. Die Kennzahl
   Prozesslast ([Kennzahlen](../../prozess/kennzahlen.md)) achtet darauf, dass die
   Prüfungen nicht schneller wachsen als das Produkt.

Antwort: Bitte Sonarlint scharfstellen.

**Stellungnahme zur Antwort.** Du hast recht: SonarLint sperrt nichts. `sonarlint.py` hält
einen Commit nur als Hook aus `.pre-commit-config.yaml` auf, und `pre-commit` ist weder
installiert noch in `pyproject.toml`; `.git/hooks/` enthält nur Beispiele. Heute läuft
keiner dieser Hooks, auch die Abdeckung der Prüfskripte nicht. SonarLint lief nur, wenn der
Regelumsetzer es aufrief. Er macht die Hooks wirksam, mit einer Prüfung, die rot wird,
solange sie nicht installiert sind ([216](216-commitHooksWirksamMachen.md)); bis dahin ist
die Sperre in DoD 2 als nur Text markiert. Wartet auf 216.

Antwort: Bitte hier melden, sobald sonarlint scharf gestellt ist. Bis dahin bleibt das Anliegen auf "offen".

**Stellungnahme zur Antwort.** So machen wir es: 150 bleibt `offen`. Sobald 216 umgesetzt ist
und SonarLint beim Commit sperrt, melde ich es hier und setze `angenommen`.

Nach dem Rückbau (be16d8d) entfällt die Abdeckung der Prüfskripte; 95 % und vulture für
das Produkt bleiben. Offen bleibt SonarLint beim Commit (216).

**Stellungnahme:** Was ist hierzu der Stand? Der Status steht immer noch auf "offen".

**Stellungnahme zur Frage.** SonarLint ist noch nicht scharf gestellt. Der Status `offen`
trifft den Stand.
- Die Prüfung gibt es, und sie ist grün: `python3 prozess/pruefungen/gemeinsam/lauf.py
  formregeln.sonarlint` meldete am 9.10. „keine Funde“. Sie läuft aber nur, wenn jemand sie
  aufruft. Im Lauf der Prüfungen ist sie nicht enthalten, und beim Commit läuft sie nicht,
  weil `pre-commit` nicht installiert ist.
- Scharf stellt sie [216](216-commitHooksWirksamMachen.md) beim Regelumsetzer. Das Anliegen
  ist seit dem 4.10. offen und nicht begonnen, weil Plan 4 Vorrang hatte. Die [Moderation](../moderation.md) reiht es hinter
  [304](304-sammelfehlerBrechenPrueflaufAb.md) ein, das ebenfalls offen ist. Beide ändern
  Hook-Code, und es darf nur einer gleichzeitig laufen.
- Richtig wäre der Kopf `offen · wartet auf 216`. Den Zusatz liest `anliegen.py` noch nicht
  ([Backlog](../../prozess/backlog.md)). Deshalb führt mich der Stand als dran.

Sobald 216 erledigt ist und ein Commit mit einem SonarLint-Fund abgewiesen wird, melde ich
es hier und setze `angenommen`. Willst du es vor dem Ende von Plan 4, kann der Koordinator
den Regelumsetzer mit 304 und danach 216 beauftragen. Neben Plan 4 geht das nur, solange
die Dateien getrennt sind ([Gleichzeitige Läufe](../../prozess/ablauf.md#gleichzeitige-läufe)).

Antwort: Bitte so früh wie möglich. Damit meine ich innerhalb der nächsten Prozessfrage.
