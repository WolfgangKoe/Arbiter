# Glossar: Code-Bezeichner in camelCase

29 · Kritik · von Organisationsentwickler (Prozess) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Funktionen, Methoden, Variablen und Parameter heißen in camelCase
([Prämisse](../../prozess/praemissen/wir.md), Entscheidung des Stakeholders). Drei
Code-Bezeichner im [Glossar](../../domaene/glossar.md) stehen in snake_case:
`an_der_reihe`, `aufstellen_der_einheit_beenden`, `einheit_in_aufstellung`.

**Kosten.** Der Testautor benennt nach dem Glossar wörtlich; bleibt es, verletzt jeder
Test entweder das Glossar oder die Prämisse, und die Prüfung Glossar ↔ Code meldet beides.

**Gegenvorschlag.** `anDerReihe`, `aufstellenDerEinheitBeenden`, `einheitInAufstellung`,
vor dem nächsten Lauf des Testautors.

**Stellungnahme.** Angenommen und umgesetzt: Das Glossar führt `anDerReihe`,
`aufstellenDerEinheitBeenden`, `einheitInAufstellung`. Die übrigen Code-Bezeichner
(`gewinner`, `aufgestellt`, `setzen`, Klassen in PascalCase) entsprechen der Prämisse schon.
Die Gründe in ‚…‘ (‚nicht wählbar‘ usw.) sind Namen, keine Glossarbegriffe; wie sie als
Enum-Werte heißen, regelt die Prämisse nach
[Anliegen 28](28-benennungOffenePunkte.md), F1.
