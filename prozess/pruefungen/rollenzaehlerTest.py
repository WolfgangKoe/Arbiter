import json
import subprocess

from rollenzaehler import zähle
from stand import protokoll, stand


def testJederRollenlaufZähltFürDieAktuellePhase(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    zähle({"agent_type": "planer"}, tmp_path)
    zähle({"agent_type": "architekt"}, tmp_path)
    zähle({"agent_type": None}, tmp_path)

    zeilen = protokoll(tmp_path).read_text(encoding="utf-8").splitlines()
    assert [json.loads(zeile)["phase"] for zeile in zeilen] == ["Zyklus 1 · Domänenphase"] * 2
    assert "Rollenläufe 2/8" in stand(tmp_path)
