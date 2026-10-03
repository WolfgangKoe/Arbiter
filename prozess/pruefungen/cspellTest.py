import json
from pathlib import Path

wurzel = Path(__file__).resolve().parents[2]


def einstellungen() -> dict:
    return json.loads((wurzel / ".vscode" / "settings.json").read_text(encoding="utf-8"))


def testCspellPrüftKeinMarkdown():
    assert einstellungen()["cSpell.enabledFileTypes"]["markdown"] is False


def testCspellÜbergehtMarkdownDateienUnabhängigVonDerSprache():
    # Warum: VS Code führt manche `.md` (etwa `.claude/agents/`) nicht unter der Sprache `markdown`.
    assert "**/*.md" in einstellungen()["cSpell.ignorePaths"]


def testLtexPrüftKeinMarkdown():
    # Warum: LTeX+ (LanguageTool) meldet deutschen Text als englische Rechtschreibfehler.
    assert einstellungen()["ltex.enabled"] is False


def testDieVeralteteEinstellungFehltDennSieÜberstimmtDieneue():
    # Warum: `cSpell.enableFiletypes` ist veraltet; die Erweiterung (4.9.3) führt `markdown: true`
    # in `cSpell.enabledFileTypes` als Standard, `!markdown` im alten Schlüssel wirkte nicht.
    assert "cSpell.enableFiletypes" not in einstellungen()
