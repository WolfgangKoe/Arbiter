import json
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]


def test_cspell_prueft_kein_markdown():
    einstellungen = json.loads((WURZEL / ".vscode" / "settings.json").read_text(encoding="utf-8"))
    assert "!markdown" in einstellungen["cSpell.enableFiletypes"]
