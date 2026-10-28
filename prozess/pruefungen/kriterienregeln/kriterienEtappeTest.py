from kriterienregeln.kriterienEtappe import etappeJeKriterium
from kriterienregeln.kriterium import Kriterium


def testEinKriteriumNenntSeineEtappeAmSatzendeSonstDieDerAnforderungSonstKeine(tmp_path):
    datei = tmp_path / "anforderung.md"
    datei.write_text(
        "### AU-1 · A\n\nEtappe: 2\n\n- AU-1.1 Eins.\n- AU-1.2 Zwei. (Etappe 3)\n\n"
        "### AU-2 · B\n\n- AU-2.1 Drei.\n- AU-2.2 Vier. (Etappe 2)\n",
        encoding="utf-8",
    )
    assert etappeJeKriterium(datei) == {
        Kriterium("AU", 1, 1): 2,
        Kriterium("AU", 1, 2): 3,
        Kriterium("AU", 2, 1): None,
        Kriterium("AU", 2, 2): 2,
    }
