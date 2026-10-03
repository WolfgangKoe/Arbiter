import pytest

from agenten import projektordner
from importvertrag import domaeneOrdner, verstöße


def domänendatei(tmp_path, text):
    datei = tmp_path / domaeneOrdner / "phasen" / "probe.py"
    datei.parent.mkdir(parents=True)
    datei.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "text",
    [
        "import yaml\n",
        "from arbiter.katalog import ausgangslage\n",
        "from arbiter.katalog.ausgangslage import ausgangslageLaden\n",
        "import arbiter.web\n",
        "from flask import Flask\n",
        "def laden():\n    import yaml\n",
    ],
)
def testImportAußerhalbVonStandardbibliothekUndDomäneIstRot(tmp_path, text):
    domänendatei(tmp_path, text)
    assert verstöße(tmp_path)


@pytest.mark.parametrize(
    "text",
    [
        "from fractions import Fraction\n",
        "import dataclasses\nfrom enum import Enum\n",
        "from __future__ import annotations\n",
        "from arbiter.domaene.sperre import Sperre\n",
        "from . import sperre\n",
        "from ..sperre import Sperre\n",
    ],
)
def testStandardbibliothekUndDomäneSindGrün(tmp_path, text):
    domänendatei(tmp_path, text)
    assert verstöße(tmp_path) == []


def testDieDomäneDesReposHältDenVertrag():
    assert verstöße(projektordner()) == []
