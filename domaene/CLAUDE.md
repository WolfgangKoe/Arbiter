# Domäne

`ziel.md` ändert nur der Stakeholder. Autoren: Planer, Anforderungsautor, UX
([Rollen](../.claude/agents/)).

- `etappen/<nn>-<kurz>.md`, `<nn>` zweistellig: `# Etappe <n> · <Name>`, Zweck in einem
  Satz, wann erreicht. Erreichtes wird gelöscht; höchstens 1.000 Zeichen.
- `anforderungen/<bereich>/<name>.md`: `spielobjekte` (OBJ), `missionsvorbereitung` (MIV),
  `phasen/<phase>` (AUF, BEW, je Phase eins), `querschnitt` (QUE); je Datei eine, nach
  Inhalt benannt. `### <Kürzel>-<n> · <Name>`, `Etappe: <n>`, `Zweck:` in 1–2 Sätzen, bei
  einer Handlung `Am Bildschirm:`, Kriterien `<Kürzel>-<n>.<m>` je ein Satz **Gegeben**,
  **wenn**, **dann** wie AUF-7, Fachbegriffe *kursiv*, mit Fundstelle; abweichend
  `(Etappe <n>)` am Ende, ohne beides keine Etappe (6500). Keine Technik, höchstens 1.200
  Zeichen. Kennungen bleiben und kommen nie wieder; gegen einen Test neu gefasst: neues
  Kriterium.
- `glossar.md`: je Begriff eine Tabellenzeile, höchstens 300 Zeichen. Beziehungen (Teil
  von, gehört zu, Anzahl) mit Fundstelle in der Definition, wer festlegt oder ändert im
  Kriterium.
- `daten/<name>.yaml`: Katalogwerte mit Fundstelle, Ausgangslagen; Schlüssel:
  Code-Bezeichner des Glossars.
- `backlog.md`, `items/<id>.md`: Umfang (Kriterien-IDs), warum jetzt, Abhängigkeit, Link auf
  Anliegen; höchstens 400 Zeichen.

Quellen: `referenz/rules/` (Fundstelle `<datei>:<zeile>`); Absicht:
`referenz/domainRules.md`, `Arbiter-old/Arbiter_Specs/`. Das Ziel geht vor, sonst Ich 1.
