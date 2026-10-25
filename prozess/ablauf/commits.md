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
