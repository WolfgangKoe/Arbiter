import json
import subprocess

from rollenzaehler import zaehle
from stand import protokoll, stand


def test_jeder_rollenlauf_zaehlt_fuer_die_aktuelle_phase(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    zaehle({"agent_type": "planer"}, tmp_path)
    zaehle({"agent_type": "architekt"}, tmp_path)
    zaehle({"agent_type": None}, tmp_path)

    zeilen = protokoll(tmp_path).read_text(encoding="utf-8").splitlines()
    assert [json.loads(z)["phase"] for z in zeilen] == ["Zyklus 1 · Domänenphase"] * 2
    assert "Budget 2/8 Rollenläufe" in stand(tmp_path)
