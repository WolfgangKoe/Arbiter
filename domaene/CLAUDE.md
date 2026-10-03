# Domäne

`ziel.md` ändert nur der Stakeholder.

- `etappen/<nn>-<kurz>.md`, `<nn>` zweistellig: erste Zeile `# Etappe <n> · <Name>`, Zweck
  in einem Satz, Bedingung, wann sie erreicht ist. Die kleinste Nummer ist die aktuelle
  Etappe; Erreichtes wird gelöscht. Höchstens 1.000 Zeichen.
- `anforderungen/<bereich>.md`, Bereiche `spielobjekte`, `phasen/<phase>`, `querschnitt`:
  je Anforderung `### <Kürzel>-<n> · <Name>`, Zweck in 1–2 Sätzen, Kriterien
  `<Kürzel>-<n>.<m>` je ein Satz, Fachbegriffe *kursiv*, regelbasiert mit Fundstelle.
  Keine Technik. Je Anforderung höchstens 1.200 Zeichen. Eine Kennung gilt, solange ihr
  Kriterium gilt; neue bekommen die nächste freie Nummer, gelöschte kommen nicht wieder.
  Widerspricht eine Neufassung einem bestehenden Test, ist sie ein neues Kriterium.
- `glossar.md`: eine Zeile je Begriff, `Begriff | englischer Regelbegriff | Code-Bezeichner |
  Definition`, höchstens 300 Zeichen.
- `daten/<name>.yaml`: Katalogwerte mit Fundstelle, Ausgangslagen der Etappen; Schlüssel
  sind Code-Bezeichner im Glossar.
- `backlog.md`, `items/<id>.md`: Umfang (Kriterien-IDs), warum jetzt, Abhängigkeit, Link auf
  Anliegen; höchstens 400 Zeichen.

Quellen: Regeltexte in `referenz/rules/` (Fundstelle `<datei>:<zeile>`). Alte
Spezifikationen (`referenz/domainRules.md`, `Arbiter/Arbiter_Specs/*.pdf`) zeigen die
Absicht des Stakeholders; das Ziel geht vor, ein Widerspruch wird eine Frage.

Mechanismus: nur Text, Höchstmaß der Etappen `hoechstmassTest.py`.
