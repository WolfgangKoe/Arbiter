# Domäne

Was Arbiter kann. Es schreiben der Planer (Etappen, Backlog, Items) und der
Anforderungsautor (Anforderungen, Glossar); `ziel.md` ändert nur der Stakeholder.

- `etappen.md`: je Etappe `## Etappe <n> · <Name>`, Zweck in einem Satz, Bedingung, wann
  sie erreicht ist. Die erste Etappe ist die aktuelle; Erreichtes wird gelöscht.
  Höchstens 2.000 Zeichen.
- `anforderungen/<bereich>.md`, Bereiche `spielobjekte`, `phasen/<phase>`, `querschnitt`:
  je Anforderung `### <Kürzel>-<n> · <Name>`, Zweck in ein bis zwei Sätzen, Kriterien
  `<Kürzel>-<n>.<m>` je ein Satz, Fachbegriffe *kursiv*, regelbasiert mit Fundstelle.
  Keine Technik, keine Historie. Je Anforderung höchstens 1.200 Zeichen.
- `glossar.md`: eine Zeile je Begriff, `Begriff | englischer Regelbegriff | Code-Bezeichner |
  Definition`, höchstens 300 Zeichen. Zugriff per grep.
- `backlog.md`, `items/<id>.md`: Umfang (Kriterien-IDs), warum jetzt, Abhängigkeit, Link auf
  Anliegen; höchstens 400 Zeichen. Ein erledigtes Item wird gelöscht.

Quellen, nur lesen: Regeltexte in `ArbiterMap/reference/rules/` (Fundstelle
`<datei>:<zeile>`). Alte Spezifikationen (`Arbiter/Arbiter_Specs/*.pdf`,
`ArbiterMap/docs/spec/domain_rules.md`) zeigen die Absicht des Stakeholders; das Ziel geht
vor, ein Widerspruch wird eine Frage.

Höchstmaße: nur Text, bis eine Prüfung sie sperrt.
