# SonarLint-Prüfung: leerer Lauf, Laufzeit, Version

180 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
Kritik am Code zu Commit `f76a862` (P2 der [Retro 2](../retro.md)). Der Lauf ist stabil:
Ich habe 71 Dateien gezählt, je eine `publishDiagnostics` zur erwarteten Datei, keine
Verwechslung.

**Befund.**
1. **Falsch grün.** `dateienSammeln` liefert für einen fehlenden Ordner nichts, und
   `funde(wurzel, [])` gibt `[]` zurück. Ausprobiert mit `technik/gibtsNicht`. Wird ein
   Ordner aus `geprüfteOrdner` umbenannt, prüft SonarLint ihn nicht mehr und meldet grün.
   Das ist dieselbe Fehlerart wie bei der Abdeckung (vulture-Fehler galt als leer).
2. **Laufzeit.** `testSonarLintMeldetNichtsZuProduktUndPrüfskripten` braucht 22 s,
   `testEineUngenutzteVariableIstEinFund` 9 s. Die Suite steigt von 18 s auf 48 s. Sie läuft
   im Hook `pruefungen` bei jedem Commit, auch bei reinen Handoff-Commits. Für die Abdeckung
   ist das schon gelöst (eigener Hook mit
   `files`).
3. **Version.** `erweiterungFinden` nimmt `sorted(...)[-1]`, sortiert also nach Text: Bei
   `…-6.9.0-…` und `…-6.10.0-…` gewinnt 6.9.0. Liegen nach einem Update beide Versionen da,
   prüft die Sperre mit der alten. Außerdem ist die Version nicht festgelegt: Ein Update von
   VS Code bringt still neue Regeln. Für ruff, complexipy, coverage und vulture schließt
   `pyproject.toml` genau das aus.
4. **Prozessverweis im Code.** `sonarlint.py` Zeile 13 `(Anliegen 179)` und der Docstring
   von `sonarlintTest.py` `(Anliegen 150)`. [wir.md](../../prozess/praemissen/wir.md) 8
   verbietet Prozessverweise. Erledigte Anliegen werden gelöscht, dann zeigt der Verweis
   ins Leere.
5. **Kleinigkeiten.** Den Parameter `erweiterung` von `funde` übergibt kein Aufrufer.
   `fundText` liest den Pfad zurück aus der URI (`removeprefix("file://")`, ohne
   Prozent-Dekodierung). Bei einem Klon unter einem Pfad mit Leerzeichen bricht
   `relative_to` ab, obwohl `fundeAufnehmen` die Datei schon als `self.erwartet` kennt.
   Nach Ablauf der Wartezeit meldet die Prüfung „hat sich vor dem Ergebnis beendet“ statt
   der Wartezeit.

**Kosten.** 1: Eine Sperre, die nach einer Umbenennung still weniger prüft. 2: etwa 30 s mehr
je Commit, jede neue Prüfung im Stand legt weiter zu. 3: Die Sperre weicht still von der
Sicht des Stakeholders ab. 4, 5: Lese- und Pflegeaufwand, eine irreführende Meldung.

**Gegenvorschlag.**
1. Jeder Ordner aus `geprüfteOrdner` existiert und enthält mindestens eine `.py`-Datei,
   sonst rot mit dem Ordnernamen. Scheiter-Test: fehlender Ordner.
2. Ein eigener Hook `sonarlint` in `.pre-commit-config.yaml` mit `python3
   prozess/pruefungen/sonarlint.py`, `files: \.py$`. Den Stand-Test aus der Suite nehmen,
   wie bei der Abdeckung. Steht der Aufruf in DoD 2, geht das an den
   Organisationsentwickler, wie zuvor beim Aufruf der Abdeckung.
3. Die erwartete Version als Konstante (etwa `6.0.`). Ist eine andere installiert, wird
   die Prüfung rot und nennt beide; der Regelumsetzer hebt die Version bewusst. Gibt es
   mehrere Ordner, wird nach Versionszahl sortiert, nicht nach Text.
4. `# Warum: technik/tests/einheit hat noch Funde zu S5778` ohne Nummer. Docstring ohne
   Verweis.
5. `erweiterung` streichen, `fundText` den Pfad übergeben und die Wartezeit in der Meldung
   nennen (etwa ein Merker, den der `Timer` setzt).
