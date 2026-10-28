import re

import pytest

from formregeln.werkzeugaufruf import pyproject
from gemeinsam.pfade import wurzel

konfiguration = wurzel / ".pre-commit-config.yaml"


def hooksLesen(text: str) -> dict[str, dict[str, str]]:
    hooks: dict[str, dict[str, str]] = {}
    aktuell: dict[str, str] = {}
    for zeile in text.splitlines():
        kennung = re.match(r"\s+- id: (\S+)", zeile)
        if kennung:
            aktuell = hooks.setdefault(kennung.group(1), {})
            continue
        feld = re.match(r"\s{8}(\w+): (.*)", zeile)
        if feld:
            aktuell[feld.group(1)] = feld.group(2).strip()
    return hooks


def ausgelösteHooks(text: str, geänderteDateien: list[str]) -> set[str]:
    return {
        kennung
        for kennung, hook in hooksLesen(text).items()
        if hook.get("always_run") == "true"
        or any(re.search(hook.get("files", "(?!)"), datei) for datei in geänderteDateien)
    }


def entries(text: str, kennungen: set[str]) -> str:
    hooks = hooksLesen(text)
    return " | ".join(hooks[kennung]["entry"] for kennung in sorted(kennungen))


alsHooks = konfiguration.read_text(encoding="utf-8")


def testEinCommitNurInHandoffStartetWederAbdeckungNochProben():
    ausgelöst = ausgelösteHooks(alsHooks, ["handoff/anliegen/601-commitHooksNachPfad.md"])
    assert {"abdeckung", "proben"}.isdisjoint(ausgelöst)
    assert "stand" in ausgelöst


def testEinCommitInTechnikStartetKeineProduktTests():
    ausgelöst = ausgelösteHooks(alsHooks, ["technik/arbiter/domaene/sperre.py", "pyproject.toml"])
    assert "abdeckung" not in ausgelöst
    assert "abdeckung" not in hooksLesen(alsHooks)
    assert "-m abdeckung" not in alsHooks
    assert "technik/tests" not in alsHooks


def testEinCommitInDenPrüfskriptenStartetDieProbenNichtDieAbdeckung():
    ausgelöst = ausgelösteHooks(alsHooks, ["prozess/pruefungen/formregeln/benennung.py"])
    assert "proben" in ausgelöst
    assert "abdeckung" not in ausgelöst


@pytest.mark.parametrize(
    "datei", ["pyproject.toml", ".pre-commit-config.yaml", "eslint.config.mjs", ".gitignore"]
)
def testEineKonfigurationStartetDieProben(datei):
    assert "proben" in ausgelösteHooks(alsHooks, [datei])


def testDerStandLäuftBeiJedemCommitOhneDieAbdeckung():
    standEntry = entries(alsHooks, {"stand"})
    assert "-m" in standEntry
    assert "not abdeckung" in standEntry


def testDieProbenNehmenDenStandNichtMit():
    assert '-m "not stand"' in entries(alsHooks, {"proben"})


def testDerHookBenennungEntfälltWeilDerStandIhnEnthält():
    assert "benennung" not in hooksLesen(alsHooks)


def testDieMarkeAbdeckungIstEingetragen():
    marken = " ".join(pyproject()["tool"]["pytest"]["ini_options"]["markers"])
    assert "abdeckung:" in marken


def testNurDieAbdeckungstestsTragenDieMarkeAbdeckung():
    trägerMitMarke = [
        datei.name
        for datei in sorted((wurzel / "prozess" / "pruefungen").rglob("*Test.py"))
        if "pytest.mark.abdeckung" in datei.read_text(encoding="utf-8")
        and datei.name != "commitHooksTest.py"
    ]
    assert trägerMitMarke == ["abdeckungTest.py"]


def testDasLöschenErledigterAnliegenLäuftNichtImCommitHook():
    assert "erledigteLoeschen" not in hooksLesen(alsHooks)
    assert "erledigteLoeschen" not in alsHooks
