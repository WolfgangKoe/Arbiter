import json

import pytest

from pfade import wurzel


def einstellungen() -> dict:
    return json.loads((wurzel / ".vscode" / "settings.json").read_text(encoding="utf-8"))


@pytest.mark.stand
def testCspellPrüftKeinMarkdown():
    assert einstellungen()["cSpell.enabledFileTypes"]["markdown"] is False


@pytest.mark.stand
def testCspellÜbergehtMarkdownDateienUnabhängigVonDerSprache():
    # Warum: VS Code führt manche `.md` (etwa `.claude/agents/`) nicht unter der Sprache `markdown`.
    assert "**/*.md" in einstellungen()["cSpell.ignorePaths"]


@pytest.mark.stand
def testLtexPrüftKeinMarkdown():
    # Warum: LTeX+ (LanguageTool) meldet deutschen Text als englische Rechtschreibfehler.
    assert einstellungen()["ltex.enabled"] is False


@pytest.mark.stand
def testDieVeralteteEinstellungFehltDennSieÜberstimmtDieneue():
    # Warum: `!markdown` im veralteten `cSpell.enableFiletypes` wirkte nicht (Erweiterung 4.9.3).
    assert "cSpell.enableFiletypes" not in einstellungen()
