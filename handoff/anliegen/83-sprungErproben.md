# Sprung zwischen Kriterium und Test: Klick erproben, behalten oder löschen

83 · Fragen · von Architekt (Technik) → Stakeholder · Runde 2/3 · offen

## Runde 1
**Befund.** Aus Anliegen 53, dort erledigt: Der Regelumsetzer hat beide Wege gebaut.
- Weg B, Befehl: `python3 prozess/pruefungen/rueckverfolgung.py AUF-1.3` gibt das Kriterium
  und jeden Test als `pfad:zeile` aus; im Terminal von VS Code springt Strg+Klick dorthin.
- Weg C, VS-Code-Erweiterung in `prozess/pruefungen/sprung/`: macht `AUF-1.3` in
  `domaene/anforderungen/` und `testAuf1_3…` in `technik/tests/akzeptanz/` zu Links.

**Kosten.** Bleibt C ungeprüft liegen, ist es Code ohne Linter (eslint fehlt) und ohne Test
des Klicks, den jeder Lauf mitschleppt.

**Stellungnahme (Stakeholder).** Muss ich VS Code dafür neu starten? Denn aktuell
funktioniert es nicht.

## Runde 2
**Befund.** Nein, dein VS Code musst du nicht neu starten. Die Erweiterung ist nicht
installiert; sie wirkt nur in einem zweiten Fenster, das der Befehl unten öffnet. Sein Titel
beginnt mit „[Extension Development Host]“ (deutsch: „[Erweiterungsentwicklungshost]“). In
deinem gewohnten Fenster passiert beim Klick nichts, das ist erwartet.

Ich habe die Erweiterung in einem eigenen VS Code 1.140 ohne andere Erweiterungen gestartet
und den Link-Anbieter abgefragt: In `aufstellen.md` liefert er 7 Links, `AUF-1.3` zeigt auf
`aufstellenTest.py` Zeile 133; in `aufstellenTest.py` 39 Links, jeder Test zeigt auf die Zeile
seines Kriteriums. Die Links stimmen also. Ungeprüft bleibt nur der Klick selbst in deinem
Fenster mit deinen Erweiterungen.

**So prüfst du.** Im Terminal, im Ordner `Arbiter_Structure` (absolute Pfade, damit der
Befehl nicht vom Arbeitsordner abhängt):
```
code --extensionDevelopmentPath="$PWD/prozess/pruefungen/sprung" "$PWD"
```
1. Es öffnet sich ein zweites Fenster mit dem Titel oben. Nur dort prüfen.
2. War so ein Fenster schon offen, dort Strg+Umschalt+P, „Developer: Reload Window“: Die
   Erweiterung wurde seit Runde 1 geändert, ein offenes Fenster kennt die alte Fassung.
3. `domaene/anforderungen/phasen/aufstellen.md` öffnen (Quelltext, nicht die Vorschau),
   Strg gedrückt halten und über `AUF-1.3` fahren: Es wird unterstrichen. Klick; erwartet:
   `aufstellenTest.py` öffnet sich bei Zeile 133.
4. Dort Strg+Klick auf `testAuf1_3VorDerWahl…`; erwartet: zurück zu Zeile 9 von
   `aufstellen.md`. Öffnet sich stattdessen eine kleine Vorschau mit Verweisen, kommt dir die
   Python-Erweiterung (Pylance) mit „Gehe zu Definition“ zuvor; dann schreib das dazu.

**Kosten.** Etwa fünf Minuten.

**Gegenvorschlag.** Wie Runde 1.

**F1 · Behalten oder löschen?**
- A: behalten, der Klick springt in beide Richtungen. Dann bekommt der Regelumsetzer von mir
  ein Anliegen: eslint für `sprung/` und ein Test, der den Link-Anbieter prüft (so wie meine
  Probe oben, nur dauerhaft).
- B: löschen, der Klick springt nicht oder Weg B reicht dir. Dann bekommt der Regelumsetzer
  ein Anliegen: `sprung/` und `sprungTest.py` löschen.
Empfehlung: A; du wolltest C ausdrücklich, und die Links stimmen. Springt der Klick nicht,
schreib hinter `Antwort:` B und bei welchem Schritt (1 bis 4) es hakt.
Antwort: .
