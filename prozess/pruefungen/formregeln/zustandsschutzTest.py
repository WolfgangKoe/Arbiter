import pytest

from formregeln.glossar import domaeneOrdner
from formregeln.zustandsschutz import lesenGesperrtOrdner, verstöße
from gemeinsam.pfade import katalogOrdner, projektordner, webOrdner


def datei(tmp_path, ordner, text):
    pfad = tmp_path / ordner / "probe.py"
    pfad.parent.mkdir(parents=True)
    pfad.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "text",
    [
        "from dataclasses import dataclass\n@dataclass(eq=False)\nclass Probe:\n    pass\n",
        "from dataclasses import dataclass\n@dataclass\nclass Probe:\n    pass\n",
        "import dataclasses\n@dataclasses.dataclass(frozen=False)\nclass Probe:\n    pass\n",
    ],
)
def testD3DataclassOhneFrozenInDerDomäneIstRot(tmp_path, text):
    datei(tmp_path, domaeneOrdner, text)
    assert verstöße(tmp_path)


def testD3FrozenDataclassIstGrün(tmp_path):
    datei(tmp_path, domaeneOrdner, "@dataclass(frozen=True, eq=False)\nclass Probe:\n    pass\n")
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize("ordner", lesenGesperrtOrdner)
@pytest.mark.parametrize(
    "text", ["aufstellung._stellen\n", "x = aufstellung._stellen[modell]\n", "self._a._b\n"]
)
def testD3ZugriffAufUnterstrichAttributIstRot(tmp_path, ordner, text):
    datei(tmp_path, ordner, text)
    assert verstöße(tmp_path)


@pytest.mark.parametrize(
    "text", ["aufstellung._stellen[modell] = stelle\n", "aufstellung.anDerReihe = spieler\n"]
)
def testD3ZuweisenAnAttributInWebIstRot(tmp_path, text):
    datei(tmp_path, webOrdner, text)
    assert verstöße(tmp_path)


@pytest.mark.parametrize(
    "text",
    [
        'setattr(aufstellung, "anDerReihe", spieler)\n',
        'delattr(aufstellung, "anDerReihe")\n',
        'object.__setattr__(aufstellung, "_stellen", {})\n',
        'object.__setattr__(self, "_stellen", {})\n',
    ],
)
def testD3SchreibenOhneZuweisungInWebIstRot(tmp_path, text):
    datei(tmp_path, webOrdner, text)
    assert verstöße(tmp_path)


def testD3SetattrAnSelfInWebIstGrün(tmp_path):
    datei(tmp_path, webOrdner, 'setattr(self, "name", 1)\n')
    assert verstöße(tmp_path) == []


def testD3SetattrInKatalogIstGrün(tmp_path):
    datei(tmp_path, katalogOrdner, 'setattr(ding, "wert", 1)\n')
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "text", ["self._server = 1\nself._server.x\nname = __name__\nx = Typ.__members__\n"]
)
def testD3SelfUndDunderSindGrün(tmp_path, text):
    datei(tmp_path, webOrdner, text)
    assert verstöße(tmp_path) == []


def testD3ZuweisenInKatalogIstGrün(tmp_path):
    datei(tmp_path, katalogOrdner, "ding.wert = 1\n")
    assert verstöße(tmp_path) == []


@pytest.mark.stand
def testDerCodeDesReposHältDenZustandsschutz():
    assert (projektordner() / webOrdner).is_dir()
    assert verstöße(projektordner()) == []


@pytest.mark.parametrize("ordner", [webOrdner, katalogOrdner])
@pytest.mark.parametrize(
    "text",
    [
        'getattr(aufstellung, "_stellen")\n',
        'hasattr(aufstellung, "_stellen")\n',
        'aufstellung.__dict__["_stellen"]\n',
        "vars(aufstellung)\n",
    ],
)
def testD3UmwegZumUnterstrichZugriffIstRot(tmp_path, ordner, text):
    datei(tmp_path, ordner, text)
    assert verstöße(tmp_path)


@pytest.mark.parametrize(
    "text",
    [
        'getattr(aufstellung, "name")\n',
        'getattr(aufstellung, "__name__")\n',
        "getattr(aufstellung, name)\n",
        "self.__dict__\nvars(self)\n",
        'getattr(self, "_x", None)\n',
        'hasattr(self, "_x")\n',
        "vars()\n",
    ],
)
def testD3GetattrOhneUnterstrichUndSelfSindGrün(tmp_path, text):
    datei(tmp_path, webOrdner, text)
    assert verstöße(tmp_path) == []
