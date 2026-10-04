# Bash-Sandbox statt Heuristik für Anliegen und nur lesbare Pfade

139 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 2/3 · offen

## Runde 1
**Befund.** Rollen dürfen Anliegen nur mit Write und Edit ändern, nur lesbare Pfade gar
nicht. Für Bash prüft das `bashPositivliste.py` per Heuristik am Befehlstext. Ein Skript
(`python3 - <<EOF … write_text …`, `python3 -c`) oder `cd <pfad> && rm …` kommt durch
([138](138-anliegenPerSkriptAmBashSchutzVorbei.md); dem Reviewer passierte es an 132). Dann
greifen Statusrecht und Nummernprüfung nicht. Eine Heuristik am Text bleibt lückenhaft.

**Kosten.** Status, Runde oder Nummer lassen sich unbemerkt setzen. Jede neue Lücke kostet
eine weitere Regel in der Heuristik.

**Gegenvorschlag.** Bordmittel von Claude Code: die
[Bash-Sandbox](https://code.claude.com/docs/en/sandboxing). Das Betriebssystem sperrt das
Schreiben für alle Bash-Befehle und ihre Prozesse, gleich wie sie formuliert sind;
Write und Edit laufen außerhalb und bleiben mit den Hooks möglich. In
`.claude/settings.json`: `sandbox.enabled`, `filesystem.denyWrite` für `handoff/anliegen/`
und die nur lesbaren Pfade, `allowUnsandboxedCommands: false`. Die Heuristik entfällt.
Folgen: Bash-Befehle brauchen für Netzwerk freigegebene Hosts; `erledigteLoeschen.py` löscht
nur noch im SubagentStop-Hook, nicht im Testlauf und nicht im pre-commit (außer `git commit`
steht in `excludedCommands`); `.claude/skills` ist für Bash dann ohnehin gesperrt. Unerprobt: Unter Linux braucht die Sandbox
`bubblewrap` und `socat`; ob sie bei dir laufen, zeigt `/sandbox`. Baut der Regelumsetzer,
zuerst als Versuch mit Scheiter-Test. Das ändert die Rechte aller Rollen, daher deine
Entscheidung.

**F1 · Sandbox statt Heuristik?**
- A: Ja, der Regelumsetzer baut sie und entfernt die Heuristik für Anliegen und nur lesbare
  Pfade.
- B: Nein, die Lücke bleibt dokumentiert (Ablauf, Anliegen), die Heuristik bleibt.
Empfehlung: A.

Antwort: Sandbox klingt grundsätzlich gut, aber das ist noch keine Entscheidung für A. Bitte erläutere mir die Optionen und vor allem die Konsequenzen im Blick auf potentielle technische Schuld, Umgehung von Regeln, die ungesehen bleiben, Bruch mit SOLID und Prinzipien aus diesem Projekt und Tokenkosten. Dagegen bitte auch die Vorteile. Also was lösen wir mit deinen Vorschlägen und welchen Beifang holen damit ein. Das muss ich für eine Entscheidung abwägen können.

## Runde 2
**Befund.** Du willst Optionen, Nutzen und Beifang abwägen. Probe hier: `bwrap` und `socat`
sind installiert, `bwrap` startet (AppArmor sperrt nicht).

**Stellungnahme.** Das Ziel: Keine Rolle ändert per Bash ein Anliegen oder einen nur lesbaren
Pfad, ohne dass es auffällt.
- A, Sandbox. Löst: Jeder Weg ist zu (Skript, `python3 -c`, `cd`), nicht nur die bekannten;
  der Pfadteil von `bashPositivliste.py` (rund 2.500 Zeichen, 5 Funktionen) entfällt, und
  damit Prüfcode, der mit jeder Lücke wächst. Bordmittel statt Eigenbau.
  Beifang: gilt für alle Rollen gleich, nicht je Rolle; Schreibpfade je Rolle bleiben bei
  den Hooks. Unser Code bekommt eine Abhängigkeit von `bubblewrap` und den Einstellungen von
  Claude Code. Ein Scheiter-Test in pytest kann nur die Einstellung lesen, die Sperre selbst
  zeigt nur ein Probelauf. Ungesehen bleibt, was `excludedCommands` ausnimmt, und was du
  mit `!` tippst. `erledigteLoeschen.py` löscht nur noch im Hook, nicht im Testlauf.
  Bash ins Netz nur zu freigegebenen Hosts. Token: weniger Verweigerungen per Hook, eine
  gesperrte Schreibaktion endet mit `Operation not permitted` statt mit einem Grund.
- B, Heuristik bleibt, Lücke dokumentiert. Löst nichts, kostet nichts Neues. Beifang: Wer
  die Lücke nutzt, bleibt unbemerkt, bis ein Kritiker es zufällig sieht (138).
- C, Heuristik erweitern (Pfade in Heredoc und `-c` suchen). Schließt die bekannten Wege,
  sperrt aber auch lesende Skripte und bleibt lückenhaft (Variablen, erzeugte Pfade). Jede
  neue Lücke ist neuer Prüfcode: technische Schuld im Prozess, die Prozesslast steigt.
SOLID und unsere Prinzipien: A trennt am saubersten (das System sperrt, die Hooks prüfen
Rollenrechte), C mischt in eine Datei, was sie nicht erkennen kann.

**F2 · Welche Option?**
- A: Sandbox, zuerst als Versuch: `/sandbox` aktiv, ein Probelauf je Weg aus 138 scheitert,
  dann entfällt der Pfadteil der Heuristik.
- B: Heuristik, Lücke dokumentiert.
- C: Heuristik erweitern.
Empfehlung: A.

Antwort: .
