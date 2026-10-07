import pytest

from formregeln.glossar import domaeneOrdner
from formregeln.importvertrag import verstöße
from gemeinsam.pfade import projektordner, webOrdner


def domänendatei(tmp_path, text, name="phasen/probe.py"):
    datei = tmp_path / domaeneOrdner / name
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
    "name, text",
    [
        ("sperre.py", "from ..katalog import ausgangslage\n"),
        ("sperre.py", "from .. import katalog\n"),
        ("sperre.py", "from ... import x\n"),
        ("phasen/probe.py", "from ...katalog.ausgangslage import ausgangslageLaden\n"),
    ],
)
def testRelativerImportAusDerDomäneHinausIstRot(tmp_path, name, text):
    domänendatei(tmp_path, text, name)
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


@pytest.mark.stand
def testDieDomäneDesReposHältDenVertrag():
    assert (projektordner() / domaeneOrdner).is_dir()
    assert verstöße(projektordner()) == []


def webdatei(tmp_path, text, name="probe.py"):
    datei = tmp_path / webOrdner / name
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "text",
    [
        "from flask import render_template\n",
        "from flask import jsonify, render_template_string\n",
        "import jinja2\n",
        "from markupsafe import Markup\n",
        "import flask.templating\n",
        "import flask\nflask.render_template\n",
        "import flask as f\nf.render_template_string(x)\n",
        "from flask import templating\ntemplating.render_template(x)\n",
        "import flask\nflask.templating.render_template(x)\n",
        "import flask.json\nflask.render_template(x)\n",
        "from flask import *\n",
    ],
)
def testW1HtmlErzeugenInWebIstRot(tmp_path, text):
    webdatei(tmp_path, text)
    assert verstöße(tmp_path)


def testW1FlaskJsonifyInWebIstGrün(tmp_path):
    webdatei(tmp_path, "import flask\nflask.jsonify\nfrom flask import jsonify\n")
    assert verstöße(tmp_path) == []


@pytest.mark.parametrize(
    "text",
    [
        "from flask import jsonify\n",
        "import flask.json\n",
        "from werkzeug.serving import make_server\n",
    ],
)
def testW2FlaskInDarstellungIstRot(tmp_path, text):
    webdatei(tmp_path, text, "darstellung.py")
    assert verstöße(tmp_path)


def testW2FlaskInAnderemWebModulIstGrün(tmp_path):
    webdatei(tmp_path, "from flask import Flask\n", "anwendung.py")
    assert verstöße(tmp_path) == []


@pytest.mark.stand
def testDasWebDesReposHältDenVertrag():
    assert (projektordner() / webOrdner).is_dir()
    assert verstöße(projektordner()) == []
