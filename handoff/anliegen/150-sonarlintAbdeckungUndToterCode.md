# SonarLint scharf, Abdeckung 95 % ohne toten Code

150 · Kritik · von Stakeholder → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund** (übermittelt vom Koordinator). „Kritik an den Organisationsentwickler: Haben wir
denn schon Sonarlint scharf gestellt? Wie können wir die Code-Qualität nachhaltig hoch
halten? Die Testabdeckung müssen wir messen und bei mindestens 95% halten, aber gleichzeitig
sicherstellen, dass wir damit keinen toten Code am Leben halten.“

**Stellungnahme (Organisationsentwickler).** Angenommen in allen Punkten; es gelten
[DoD 1 und 2](../../prozess/ablauf.md#dod-item-fertig).
1. **SonarLint:** `sonarlint.py` startet den Analysator deiner VS-Code-Erweiterung ohne
   VS Code, Standardprofil ohne die Namensregeln (camelCase).
2. **Abdeckung:** Zeilen und Zweige mindestens 95 % für `technik/arbiter` (`abdeckung.py`).
3. **Kein toter Code am Leben:** vulture über Produkt und Akzeptanztests, ohne
   Einheitstests (`unbenutzterCode`). Zeilen, die nur Einheitstests erreichen, beurteilt der
   Reviewer in der DoD: Vorbedingung, fehlendes Kriterium oder tot. Ob ein Test Code prüft,
   statt ihn nur auszuführen, zeigen erst Mutationstests (DoD, letzter Absatz); ich schlage
   sie vor, sobald ein Befund es verlangt.
4. **Nachhaltig:** Was eine Prüfung sperrt, hält; was nur Text ist, verfällt. Die Kennzahl
   Prozesslast ([Kennzahlen](../../prozess/kennzahlen.md)) achtet darauf, dass die
   Prüfungen nicht schneller wachsen als das Produkt.

Antwort: Bitte Sonarlint scharfstellen.

**Stellungnahme zur Antwort.** SonarLint sperrte nichts, weil `pre-commit` nicht installiert
war. Der Regelumsetzer macht die Hooks wirksam (Anliegen 216).

Antwort: Bitte hier melden, sobald sonarlint scharf gestellt ist. Bis dahin bleibt das Anliegen auf "offen".

**Stellungnahme:** Was ist hierzu der Stand? Der Status steht immer noch auf "offen".

**Stellungnahme zur Frage.** Zu dem Zeitpunkt war SonarLint noch nicht scharf, 216 war noch
nicht begonnen.

Antwort: Bitte so früh wie möglich. Damit meine ich innerhalb der nächsten Prozessfrage.

**Stellungnahme (Organisationsentwickler).** SonarLint ist jetzt scharf gestellt. Ich setze
`angenommen`.
- Bei jedem Commit mit einer `.py`-Datei läuft der Hook `sonarlint`. Hat er einen Fund, wird
  der Commit abgewiesen. Ich habe das am 9.10. in einem frischen Klon nachgeprüft: eine neue
  Datei mit `unbenutzt = 5` wurde mit `python:S1481` abgewiesen, Exit 1, kein Commit.
  SonarLint allein brauchte 31 s.
- Umgesetzt ist das in Anliegen 216: `pre-commit` 4.6 liegt in
  `.venv`, `.git/hooks/pre-commit` ist angelegt. Fehlt der Hook, wird
  `python3 -m pytest prozess/pruefungen` rot.
- Mit SonarLint laufen jetzt auch die übrigen Hooks: Prüfungen, Benennung und das Löschen
  erledigter Anliegen. Ein Commit mit allen Hooks dauert gut 3 Minuten.
- In einem neuen Klon ist einmal `.venv/bin/pre-commit install` nötig.
- `git commit --no-verify` umgeht die Hooks. Das hat bisher niemand getan. Eine Sperre dafür
  baue ich erst, wenn es vorkommt.

Bitte setze `erledigt`, wenn das für dich passt.
