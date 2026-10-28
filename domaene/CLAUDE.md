# Domäne

`ziel.md` ändert nur der Stakeholder.

- `etappen/<nn>-<kurz>.md`, `<nn>` zweistellig: `# Etappe <n> · <Name>`, Zweck in einem
  Satz, Bedingung fürs Erreichen. Aktuell: kleinste Nummer; Erreichtes wird gelöscht.
  Höchstens 1.000 Zeichen.
- `anforderungen/<bereich>/<name>.md`, Bereiche `spielobjekte` (OBJ), `missionsvorbereitung`
  (MIV), `phasen/<phase>` (je Phase ein Kürzel: AUF, BEW), `querschnitt` (QUE): je Datei
  eine, nach Inhalt benannt.
  `### <Kürzel>-<n> · <Name>`, `Zweck:` in 1–2 Sätzen, bei einer Handlung `Am Bildschirm:`,
  Kriterien `<Kürzel>-<n>.<m>` je ein Satz mit **Gegeben**, **wenn**, **dann** wie AUF-7,
  Fachbegriffe *kursiv*, regelbasiert mit Fundstelle. Keine Technik, höchstens 1.200
  Zeichen. Kennungen bleiben und kommen nie wieder; eine Neufassung gegen einen Test ist
  ein neues Kriterium.
- `glossar.md`: je Begriff eine Tabellenzeile, höchstens 300 Zeichen.
  Beziehungen (Teil von, gehört zu, Anzahl) mit Fundstelle in der Definition, wer
  festlegt oder ändert im Kriterium.
- `daten/<name>.yaml`: Katalogwerte mit Fundstelle, Ausgangslagen; Schlüssel:
  Code-Bezeichner des Glossars.
- `backlog.md`, `items/<id>.md`: Umfang (Kriterien-IDs), warum jetzt, Abhängigkeit, Link auf
  Anliegen; höchstens 400 Zeichen.

Quellen: `referenz/rules/` (Fundstelle `<datei>:<zeile>`); Absicht:
`referenz/domainRules.md`, `Arbiter-old/Arbiter_Specs/`; Vorbild für Happy Path, Bedienung,
Aussehen: ArbiterMap, Arbiter-old. Das Ziel geht vor, sonst Ich 1.
