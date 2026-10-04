# Domäne

`ziel.md` ändert nur der Stakeholder.

- `etappen/<nn>-<kurz>.md`, `<nn>` zweistellig: erste Zeile `# Etappe <n> · <Name>`, Zweck
  in einem Satz, Bedingung fürs Erreichen. Die kleinste Nummer ist aktuell;
  Erreichtes wird gelöscht. Höchstens 1.000 Zeichen.
- `anforderungen/<bereich>.md`, Bereiche `spielobjekte`, `phasen/<phase>`, `querschnitt`:
  je Anforderung `### <Kürzel>-<n> · <Name>`, Zweck in 1–2 Sätzen, Kriterien
  `<Kürzel>-<n>.<m>` je ein Satz, Fachbegriffe *kursiv*, regelbasiert mit Fundstelle.
  Keine Technik, höchstens 1.200 Zeichen. Eine Kennung bleibt, solange ihr Kriterium gilt,
  und kommt nie wieder; eine Neufassung gegen einen Test ist ein neues Kriterium.
- `glossar.md`: je Begriff `Begriff | englischer Regelbegriff | Code-Bezeichner |
  Definition`, höchstens 300 Zeichen. Beziehungen (Teil von, gehört zu, Anzahl) stehen mit
  Fundstelle in der Definition, wer festlegt oder ändert im Kriterium.
- `daten/<name>.yaml`: Katalogwerte mit Fundstelle, Ausgangslagen; Schlüssel sind
  Code-Bezeichner des Glossars.
- `backlog.md`, `items/<id>.md`: Umfang (Kriterien-IDs), warum jetzt, Abhängigkeit, Link auf
  Anliegen; höchstens 400 Zeichen.

Quellen: Regeltexte in `referenz/rules/` (Fundstelle `<datei>:<zeile>`). Alte
Spezifikationen (`referenz/domainRules.md`, `Arbiter-old/Arbiter_Specs/`) zeigen die
Absicht des Stakeholders. Das Ziel geht vor; Widerspruch oder Lücke wird eine Frage.

Mechanismus: nur Text, Höchstmaß der Etappen `hoechstmassTest.py`.
