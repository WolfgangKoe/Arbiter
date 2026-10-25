import json

from gemeinsam.pfade import projektordner

verboteneBefehle = (
    "Bash(sed -i*)",
    "Bash(sed * -i*)",
    "Bash(sed --in-place*)",
    "Bash(sed * --in-place*)",
    "Bash(python3 -c*)",
    "Bash(python3 -)",
    "Bash(python3 - *)",
    "Bash(python -c*)",
    "Bash(python -)",
    "Bash(python - *)",
)


def sperrenDerEinstellungen() -> list[str]:
    einstellungen = projektordner() / ".claude" / "settings.json"
    return json.loads(einstellungen.read_text(encoding="utf-8"))["permissions"]["deny"]


def testSedImPlaceUndPythonSchnipselSindFürClaudeCodeVerboten():
    fehlend = [regel for regel in verboteneBefehle if regel not in sperrenDerEinstellungen()]
    assert not fehlend


def testPythonModuleUndPrüfskripteBleibenErlaubt():
    verboten = " ".join(sperrenDerEinstellungen())
    assert "python3 -m" not in verboten
    assert "prozess/pruefungen" not in verboten
