import json
import shutil
import subprocess
from pathlib import Path

import pytest

ordner = Path(__file__).resolve().parent / "sprung"
höchstzeilen = 80


def testDieErweiterungBleibtUnterAchtzigZeilen():
    zeilen = sum(len(datei.read_text(encoding="utf-8").splitlines()) for datei in ordner.iterdir())
    assert zeilen <= höchstzeilen


def testDasManifestNenntDieHauptdatei():
    manifest = json.loads((ordner / "package.json").read_text(encoding="utf-8"))
    assert (ordner / manifest["main"]).is_file()


@pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt")
def testDieMusterFindenKriteriumUndTestname(tmp_path):
    stub = tmp_path / "node_modules" / "vscode"
    stub.mkdir(parents=True)
    (stub / "index.js").write_text("module.exports = {};", encoding="utf-8")
    skript = (
        f"const e = require({json.dumps(str(ordner / 'extension.js'))});"
        "const f = (o, t) => e.treffer(t, o.muster).map((x) => x.eingabe);"
        "console.log(JSON.stringify([f(e.orte[0], 'siehe AUF-1.4 und AUF-12.3'),"
        " f(e.orte[1], 'def testAuf1_4DasKriterium(): ...')]));"
    )
    ergebnis = subprocess.run(
        ["node", "-e", skript],
        capture_output=True,
        text=True,
        check=True,
        env={"NODE_PATH": str(tmp_path / "node_modules"), "PATH": "/usr/bin:/bin"},
    )
    assert json.loads(ergebnis.stdout) == [["AUF-1.4", "AUF-12.3"], ["testAuf1_4"]]
