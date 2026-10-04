# SonarLint scharf, Abdeckung 95 % ohne toten Code

150 · Kritik · von Stakeholder → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

## Runde 1
**Befund** (übermittelt vom Koordinator). „Kritik an den Organisationsentwickler: Haben wir
denn schon Sonarlint scharf gestellt? Wie können wir die Code-Qualität nachhaltig hoch
halten? Die Testabdeckung müssen wir messen und bei mindestens 95% halten, aber gleichzeitig
sicherstellen, dass wir damit keinen toten Code am Leben halten.“

**Stellungnahme (Organisationsentwickler).** Angenommen in allen Punkten, umgesetzt als
Prozess-Items P1 und P2 der [Retro 2](../retro.md).

1. **SonarLint ist nicht scharf gestellt.** [Ablauf, Werkzeuge](../../prozess/ablauf.md#technikphase)
   verlangt eine Sperre mindestens so streng wie SonarLint; abgeglichen hat das niemand.
   SonarLint 6.0.1 läuft nur in deinem VS Code mit dem Standardprofil, die Agenten sehen
   seine Meldungen nie. Gesperrt wird über ruff (`pyproject.toml`), complexipy (kognitive
   Komplexität 15, dieselbe Zählung wie Sonar S3776) und die eigenen Prüfungen.
   P2: zuerst ein Wegwerf-Versuch, ob der Analysator der Erweiterung (`sonarlint-ls.jar`,
   `analyzers/sonarpython.jar`, mitgelieferte JRE) ohne VS Code im Lauf der Prüfungen läuft;
   dann sperrt SonarLint selbst. Sonst bildet der Regelumsetzer die Python-Regeln des Profils
   „Sonar way“ auf ruff ab, der Rest steht als nur Text in `prozess/regeln.md`. Bis dahin ist
   jede Meldung, die du in VS Code siehst, als Anliegen ein Befund für eine Regel.

2. **Abdeckung**, Zweige, gemessen an `9b47519` mit `coverage` außerhalb des Repos:
   - `technik/arbiter`, alle Tests: 100 %.
   - nur Akzeptanztests: 94 %. Acht Zeilen erreicht nur ein Einheitstest: Vorbedingungen in
     `aufstellen.py` (42, 44, 81, 94), Datenprüfung in `katalog/ausgangslage.py` (21, 50, 52, 55).
   - `prozess/pruefungen`: 93 %.
   P1: Zweigabdeckung mindestens 95 % für `technik/arbiter` und `prozess/pruefungen`, im
   Lauf von `python3 -m pytest prozess/pruefungen`, darunter rot.

3. **Kein toter Code am Leben.** Ein Einheitstest hält Code grün, den kein Kriterium braucht;
   eine Zahl allein verhindert das nicht. Darum in P1 zusätzlich:
   - vulture über `technik/arbiter` sperrt Unbenutztes (bisher nur Text).
   - Die Abdeckung allein aus den Akzeptanztests wird mitgemessen. Jede Zeile, die nur
     Einheitstests erreichen, listet die Prüfung; der Reviewer urteilt in der DoD:
     Vorbedingung oder Datenprüfung nach Architektur (bleibt), fehlendes Kriterium (Anliegen
     an den Anforderungsautor) oder tot (weg).
   Abdeckung zeigt, dass Code lief, nicht, dass ein Test ihn prüft. Das zeigen
   Mutationstests (Ablauf, DoD, letzter Absatz); sie schlage ich vor, sobald ein Befund es
   verlangt.

4. **Nachhaltig.** Was eine Prüfung sperrt, hält; was nur Text ist, verfällt. Retro 2 macht
   drei Regeln prüfbar, die nur Text waren: Abdeckung und toter Code (P1), SonarLint (P2),
   Höchstmaße für Module, Testdateien, Plan, Review und Retro (P3). Die neue Kennzahl
   Prozesslast ([Kennzahlen](../../prozess/kennzahlen.md)) achtet darauf, dass die Prüfungen
   nicht schneller wachsen als das Produkt (heute 183.000 zu 12.700 Zeichen).

Umgesetzt: P1 (`abdeckung.py`, 6753eed) und P2 (`sonarlint.py`, 1cd5dfd); beide nennt
[DoD 1 und 2](../../prozess/ablauf.md#dod-item-fertig).
