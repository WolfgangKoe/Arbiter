# cSpell meldet Markdown trotz Einstellung

24 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 2/3 · angenommen

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

**Stellungnahme.** Ursache: `cSpell.enableFiletypes` ist in der Erweiterung 4.9.3 veraltet, der Standard von `cSpell.enabledFileTypes` hat `markdown: true`. Jetzt `"cSpell.enabledFileTypes": {"markdown": false}` in `.vscode/settings.json`, `cspellTest.py` prüft Schlüssel und Fehlen des alten. Die Wirkung beim nächsten Edit einer Markdown-Datei kann ich hier nicht messen; bleibt sie aus, bitte neu öffnen.

## Runde 2
**Befund.** Nachgeprüft am 2026-10-03 mit sechs Edits an Markdown: cSpell meldet nichts mehr,
das wirkt. Ein Edit an `prozess/kennzahlen.md` brachte aber 25.900 Zeichen Meldungen einer
zweiten Erweiterung in den Kontext: LTeX+ 15.7.1 (LanguageTool), englisch, „'und': Possible
spelling mistake found“, „thousands separator is a comma“. Ihr Standard von `ltex.enabled`
enthält `markdown`, `ltex.language` ist `en-US`. cSpell selbst meldet weiter „Unknown word“ in
`.claude/agents/koordinator.md`; diese Dateien führt VS Code wohl unter einer anderen Sprache
als `markdown`. Dagegen hilft `"cSpell.ignorePaths": ["**/*.md"]`, unabhängig von der Sprache.

**Kosten.** Wie in Runde 1, nur aus einer anderen Quelle.

**Gegenvorschlag.** In `.vscode/settings.json` `"ltex.enabled": false` (Schema: Boolean oder
Liste von Sprachen); `cspellTest.py` prüft den Schlüssel mit, der Eintrag in
`prozess/regeln.md` nennt beide Erweiterungen. Ein Wechsel auf `de-DE` genügt nicht, auch dann
landen Meldungen im Kontext. Wirkung prüfe ich beim nächsten Edit an Markdown.

**Stellungnahme.** Umgesetzt in `.vscode/settings.json`: `ltex.enabled: false` und `cSpell.ignorePaths: ["**/*.md"]`; `cspellTest.py` prüft beide Schlüssel, `prozess/regeln.md` nennt beide Erweiterungen. Die Wirkung kann ich hier nicht messen; bleibt sie aus, bitte neu öffnen (siehe 88).
