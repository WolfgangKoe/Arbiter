import json
from pathlib import Path

wurzel = Path(__file__).resolve().parents[2]


def einstellungen() -> dict:
    return json.loads((wurzel / ".vscode" / "settings.json").read_text(encoding="utf-8"))


def testCspellPrüftKeinMarkdown():
    assert einstellungen()["cSpell.enabledFileTypes"]["markdown"] is False


def testDieVeralteteEinstellungFehltDennSieÜberstimmtDieneue():
    # Warum: `cSpell.enableFiletypes` ist veraltet; die Erweiterung (4.9.3) führt `markdown: true`
    # in `cSpell.enabledFileTypes` als Standard, `!markdown` im alten Schlüssel wirkte nicht
    # (Anliegen 24).
    assert "cSpell.enableFiletypes" not in einstellungen()
