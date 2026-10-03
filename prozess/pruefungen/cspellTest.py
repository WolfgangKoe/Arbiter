import json
from pathlib import Path

wurzel = Path(__file__).resolve().parents[2]


def testCspellPrüftKeinMarkdown():
    einstellungen = json.loads((wurzel / ".vscode" / "settings.json").read_text(encoding="utf-8"))
    assert "!markdown" in einstellungen["cSpell.enableFiletypes"]
