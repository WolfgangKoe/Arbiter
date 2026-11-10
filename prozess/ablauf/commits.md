# Commits

Der Koordinator committet nach jeder Freigabe und nach jedem Lauf, der etwas abschließt:
einen Schritt des [Fortschritts](fortschritt.md) abhakt oder ein Anliegen auf `angenommen`,
`abgelehnt` oder `erledigt` setzt (Retro 6, P1). Betreff: die Freigabe, das Item der
Technikphase, ein Prozess-Item mit `P<k>: …`, mehrere mit `P<j>, P<k> und P<l>: …`. Er prüft
nicht vorher selbst: Die Prüfungen laufen im
Commit-Hook, ist eine rot, scheitert der Commit und lässt alles stehen; er meldet es der
Rolle, die es beheben kann. Der Hook prüft nur, was der Commit ändern kann, ohne die
Produkttests und die Abdeckung, auch bei einem Commit in `technik/`: Beides misst der Lauf
von `python3 -m pytest prozess/pruefungen` beim Implementierer, bevor er fertig meldet, und
beim Reviewer bei der DoD. Der Regelumsetzer prüft, bevor er fertig meldet, nur die Tests
der Module, die er geändert hat; den Rest prüft der Hook (Anliegen 600, 1950, 16440). Mechanismus: `.pre-commit-config.yaml`, Hooks je Pfad, ohne
Produkttests und Abdeckung (Anliegen 601, 1950, [Formregeln](../regeln/formregeln.md)); sonst nur Text.

Jeder Commit läuft in einem eigenen Arbeitsbaum, die Rollen arbeiten weiter (Anliegen 11100,
14360). Im gemeinsamen legt der Hook alle übrigen Änderungen beiseite: Laufende Rollen sähen
alte Stände, Geschriebenes ginge verloren; pre-commit kann das nicht abschalten (Anliegen
2460). Der Koordinator committet darum nur mit
`python3 prozess/pruefungen/gemeinsam/lauf.py gemeinsam.commitImArbeitsbaum "<Nachricht>" <Pfade>`,
nie mit `git commit`; die Nachricht darf mehrzeilig sein (Betreff, Begründung,
`Co-Authored-By`), Pfade auch gelöschte, ohne Pfad leer für eine Freigabe. Schrieb die Rolle
in ihrem Arbeitsbaum unter `.claude/worktrees/<name>/`, steht vor der Nachricht
`--aus <Arbeitsbaum>` (Anliegen 16721); sonst ist der Quellordner der Projektordner. Der Befehl:
1. legt mit `git worktree add --detach` unter `/tmp` einen Arbeitsbaum auf `dev` an und
   verlinkt darin `node_modules`,
2. übernimmt die Pfade aus dem Quellordner und committet dort samt Hook,
3. setzt `dev` mit `git update-ref refs/heads/dev <neu> <alt>`, nur wenn `dev` noch auf dem
   alten Commit steht, gleicht im Quellordner den Index der Pfade an (`git reset -q --
   <Pfade>`) und entfernt den Arbeitsbaum.
Scheitert der Hook oder bewegte sich `dev`, bleibt der Quellordner unberührt; der
Befehl nennt den Grund und endet mit 1. Für jede Rolle sperrt die Schreibgrenze `git commit`
und den Befehl. Mechanismus: `gemeinsam/commitImArbeitsbaum.py`, `rollenregeln/schreibgrenze.py`
([Rollenregeln](../regeln/rollenregeln.md)); dass der Koordinator nicht `git commit` nutzt,
nur Text.
