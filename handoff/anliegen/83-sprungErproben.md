# Sprung zwischen Kriterium und Test: Klick erproben, behalten oder löschen

83 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Aus Anliegen 53, dort erledigt: Der Regelumsetzer hat beide Wege gebaut.
- Weg B, Befehl: `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.3` gibt das Kriterium
  und jeden Test als `pfad:zeile` aus; im Terminal von VS Code springt Strg+Klick dorthin.
  Erprobt, er läuft.
- Weg C, VS-Code-Versuch in `prozess/pruefungen/sprung/`: macht `AUF-1.3` in
  `domaene/anforderungen/` und `testAuf1_3…` in `technik/tests/akzeptanz/` zu Links. Ob der
  Klick wirklich springt, kann nur jemand in VS Code prüfen. Das bist du.

**Kosten.** Bleibt C ungeprüft liegen, ist es Code ohne Linter (eslint fehlt) und ohne Test
des Klicks, den jeder Lauf mitschleppt. Prüfen kostet dich etwa fünf Minuten.

**So prüfst du.** Im Ordner `Arbiter_Structure`:
```
code --extensionDevelopmentPath=prozess/pruefungen/sprung .
```
Im neuen Fenster `domaene/anforderungen/phasen/aufstellen.md` öffnen, Strg+Klick auf
`AUF-1.3`. Erwartet: Es öffnet sich `aufstellenTest.py` beim ersten Test zu AUF-1.3. Dann dort
Strg+Klick auf `testAuf1_3VorDerWahl…`; erwartet: zurück zur Zeile von AUF-1.3.

**F1 · Behalten oder löschen?**
- A: behalten, der Klick springt in beide Richtungen. Dann bekommt der Regelumsetzer von mir
  ein Anliegen: eslint für `sprung/` und ein Test, der den Link-Anbieter prüft.
- B: löschen, der Klick springt nicht oder Weg B reicht dir. Dann bekommt der Regelumsetzer
  ein Anliegen: `sprung/` und `sprungTest.py` löschen.
Empfehlung: A; du wolltest C ausdrücklich, und Befehl B, auf dem C aufbaut, läuft. Springt
der Klick nicht, schreib hinter `Antwort:` B und was passiert ist.
Antwort: .
