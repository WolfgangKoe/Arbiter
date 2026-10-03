# VS-Code-Erweiterung sprung/ löschen

118 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder hat in [83](83-sprungErproben.md) entschieden: Die Erweiterung
`prozess/pruefungen/sprung/` wird gelöscht. Sie wirkte nur in einem zweiten Fenster, der Klick
ist nie gelungen. Der Sprung geht über den Namen (Strg+T, Strg+Umschalt+F) und den Befehl,
siehe [T2](../../technik/architektur.md).

**Kosten.** Toter Code samt Test bleibt sonst liegen und wird beim Umbau nach
[114](114-pruefskripteOrdnenUndLesbarMachen.md) mit umgezogen.

**Gegenvorschlag.**
1. `prozess/pruefungen/sprung/` und `prozess/pruefungen/sprungTest.py` löschen.
2. Die Zeile „Spur vom Kriterium zum Test“ in `prozess/regeln.md` ohne `sprung/`,
   `sprungTest.py` und „VS-Code-Versuch; Klick unerprobt“.
3. `--json` in `rueckverfolgung.py` löschen, falls nur die Erweiterung es braucht.
4. Beim Umbau nach 114 entfällt `sprung/` in der Gliederung; am besten in einem Zug mit 114.

Wählt der Stakeholder in 83 F2 B, entsteht die Erweiterung neu als Paket; der heutige Stand
liegt dann in git.

Erledigt, wenn kein Pfad mehr `sprung` nennt (außer Anliegen) und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme.** Angenommen und umgesetzt: `sprung/` und `sprungTest.py` gelöscht, `--json`
samt Test aus `rueckverfolgung.py` entfernt (nur die Erweiterung brauchte es), Zeile in
`prozess/regeln.md` bereinigt. Kein Pfad nennt mehr `sprung`.
