# Koordinaten x und y gegen die Namensregel

128 · Anliegen · von Implementierer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Die Akzeptanztests rufen `Stelle(x=…, y=…)` auf (`conftest.py`, `auf1Test.py`);
Architektur S1 legt die Achsen x und y fest. `Stelle` in
`technik/arbiter/domaene/spielobjekte.py` braucht deshalb die Felder `x` und `y`.
`benennung.py` meldet beide (wir.md 5: mindestens 3 Zeichen), `benennungTest.py` ist rot
(`spielobjekte.py` Zeile 16 und 17).

**Kosten.** Die Prüfung bleibt rot, bis eine Entscheidung fällt. Umbenennen geht nicht, ohne
die gesperrten Akzeptanztests zu ändern.

**Gegenvorschlag.** `benennung.py` lässt `x` und `y` als Felder von `Stelle` zu (Koordinaten
mit festen Achsen nach S1), wir.md 5 nennt die Ausnahme. Wäre der Stakeholder dagegen, ändert
der Testautor die Tests auf `breite`/`länge` und die Architektur S1 zieht nach.

Umgesetzt wie vorgeschlagen, enger gefasst: `benennung.py` lässt `x` und `y` nur als Felder der Klasse `Stelle` zu (`koordinatenfelder`); `x = 1` und `x` in anderen Klassen bleiben rot (`benennungTest.py`). Den Vermerk in wir.md 5 setzt der Organisationsentwickler.
