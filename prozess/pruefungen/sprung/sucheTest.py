import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

import rueckverfolgung

wurzel = Path(__file__).resolve().parents[3]
suche = Path(__file__).resolve().parent / "suche.js"
skript = """
const suche = require(process.argv[1]);
const [wurzel, namen] = [process.argv[2], JSON.parse(process.argv[3])];
console.log(JSON.stringify(namen.map((name) => ({
  name,
  bereich: suche.testMuster.exec(name)?.[0],
  ziele: suche.kriteriumZu(wurzel, name).map((ziel) => [ziel.datei, ziel.zeile + 1]),
}))));
"""

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt")


def namenJeKriterium():
    namen = {}
    for kriterium, stellen in rueckverfolgung.teststellen(wurzel).items():
        for _, pfad, zeile in stellen:
            text = (wurzel / pfad).read_text(encoding="utf-8").splitlines()[zeile - 1]
            namen.setdefault(kriterium, []).append(re.search(r"def (\w+)", text)[1])
    return namen


def testSucheFindetZuJedemTestDieKriteriumszeileUndDenGanzenNamen():
    namen = namenJeKriterium()
    alle = [name for jeKriterium in namen.values() for name in jeKriterium]
    ausgabe = subprocess.run(
        ["node", "-e", skript, suche, str(wurzel), json.dumps(alle)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    gefunden = {eintrag["name"]: eintrag for eintrag in json.loads(ausgabe)}
    stellen = rueckverfolgung.kriteriumsstellen(wurzel)
    for kriterium, jeKriterium in namen.items():
        erwartet = [[str(wurzel / pfad), zeile] for _, pfad, zeile in stellen[kriterium]]
        for name in jeKriterium:
            assert gefunden[name]["bereich"] == name, name
            assert gefunden[name]["ziele"] == erwartet, name
