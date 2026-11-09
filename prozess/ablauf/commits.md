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
beim Reviewer bei der DoD. Alles prüft der Regelumsetzer, bevor er fertig meldet
(Anliegen 600, 1950). Mechanismus: `.pre-commit-config.yaml`, Hooks je Pfad, ohne
Produkttests und Abdeckung (Anliegen 601, 1950, [Formregeln](../regeln/formregeln.md)); sonst nur Text.

Jeder Commit läuft in einem eigenen Arbeitsbaum, die Rollen arbeiten weiter (Anliegen 11100,
14360). Im gemeinsamen legt der Hook alle übrigen Änderungen beiseite: Laufende Rollen sähen
alte Stände, Geschriebenes ginge verloren; pre-commit kann das nicht abschalten (Anliegen
2460). Ein Befehl mit Betreff und Pfaden (auch gelöschten, ohne Pfad leer für eine Freigabe):
1. legt mit `git worktree add --detach` unter `/tmp` einen Arbeitsbaum auf `dev` an und
   verlinkt darin `node_modules`,
2. übernimmt die Pfade aus dem gemeinsamen Arbeitsbaum und committet dort samt Hook,
3. setzt `dev` mit `git update-ref refs/heads/dev <neu> <alt>`, nur wenn `dev` noch auf dem
   alten Commit steht, gleicht im gemeinsamen den Index der Pfade an (`git reset -q --
   <Pfade>`) und entfernt den Arbeitsbaum.
Scheitert der Hook oder bewegte sich `dev`, bleibt der gemeinsame Arbeitsbaum unberührt; der
Befehl nennt den Grund und endet mit 1. Ein `git commit` daneben sperrt die Schreibgrenze.
Mechanismus: nur Text, bis [P4](../../handoff/retro.md) den Befehl in `prozess/pruefungen/`
und die Sperre in `rollenregeln/schreibgrenze.py` baut; erprobt an einem Klon mit echtem
Hook und an einer Kopie in `/tmp` (Rückweg: Commit `P4:` zurücknehmen).
