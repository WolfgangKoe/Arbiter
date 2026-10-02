# cSpell meldet Markdown trotz Einstellung

24 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

Bearbeitung in der Prozessphase von Zyklus 1.

## Runde 1
**Befund.** Ein einziges Edit an `handoff/anliegen/22-…md` brachte am 2026-10-02 rund 25.000
Zeichen cSpell-Meldungen in den Kontext der Rolle („Anliegen“, „Runde“, „offen“: Unknown
word). `.vscode/settings.json` enthält `"cSpell.enableFiletypes": ["!markdown"]`, und
`test_cspell.py` ist grün: Der Test prüft den Text der Einstellung, nicht ihre Wirkung.

**Kosten.** Jedes Edit an einer Markdown-Datei kostet jede schreibende Rolle ein Vielfaches
der Änderung, in VS-Code-Sitzungen in jeder Phase.

**Gegenvorschlag.** Ursache in der Erweiterung prüfen (Schlüssel, Version, Ebene der
Einstellung) und einen Scheiter-Test, der die Wirkung zeigt, etwa über die Meldungen, die ein
`PostToolUse`-Hook nach einem Edit sieht.

**Stellungnahme.**
