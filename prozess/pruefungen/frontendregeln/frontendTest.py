"""Scheiter-Test: eslint und stylelint über technik/frontend/ (Anliegen 242)."""

import json
import re
import shutil

import pytest

from frontendregeln.frontend import eslintVerstöße, stylelintVerstöße, verstöße
from gemeinsam.pfade import frontendOrdner, wurzel

verstoßFreiesJavaScript = (
    "// Regel: wir.md 5, Achsen heißen x und y\n"
    "export function abstand(x, y) {\n"
    "  const weite = x - y;\n"
    "  return weite;\n"
    "}\n"
)
verstoßFreiesCss = (
    ":root {\n  --hintergrund: #0f0e0c;\n}\n\n"
    ".fläche {\n  background: var(--hintergrund);\n  fill: url(#add);\n}\n"
)
beideWerkzeuge = 2
zuVieleFälle = "".join(f"  if (wert === {zahl}) {{ return {zahl}; }}\n" for zahl in range(16))
zuKomplexeFunktion = f"export function wählen(wert) {{\n{zuVieleFälle}  return 0;\n}}\n"


def probeAnlegen(tmp_path, name: str, inhalt: str):
    for datei in ("eslint.config.mjs", ".stylelintrc.json"):
        shutil.copy(wurzel / datei, tmp_path / datei)
    plugins = tmp_path / "prozess" / "pruefungen" / "frontendregeln"
    plugins.mkdir(parents=True, exist_ok=True)
    for plugin in (wurzel / "prozess" / "pruefungen" / "frontendregeln").glob("*.mjs"):
        shutil.copy(plugin, plugins / plugin.name)
    (tmp_path / "node_modules").symlink_to(wurzel / "node_modules")
    (tmp_path / frontendOrdner).mkdir(parents=True, exist_ok=True)
    (tmp_path / frontendOrdner / name).write_text(inhalt, encoding="utf-8")


def testSauberesJavaScriptIstGrün(tmp_path):
    probeAnlegen(tmp_path, "seite.js", verstoßFreiesJavaScript)
    assert eslintVerstöße(tmp_path) == ""


def testDasKlonenDerTemplateIstGrün(tmp_path):
    klon = (
        "export const knoten = "
        'document.getElementById("vorlage").content.firstElementChild.cloneNode(true);\n'
    )
    probeAnlegen(tmp_path, "seite.js", klon)
    assert eslintVerstöße(tmp_path) == ""


def testSauberesCssIstGrün(tmp_path):
    probeAnlegen(tmp_path, "seite.css", verstoßFreiesCss)
    assert stylelintVerstöße(tmp_path) == ""


@pytest.mark.parametrize(
    ("regel", "quelltext"),
    [
        pytest.param("no-var", "var wert = 1;\nexport default wert;\n", id="var"),
        pytest.param("camelcase", "const mein_wert = 1;\nexport default mein_wert;\n", id="snake"),
        pytest.param("id-length", "const ab = 1;\nexport default ab;\n", id="zu kurz"),
        pytest.param("id-length", "const i = 1;\nexport default i;\n", id="einbuchstabig"),
        pytest.param("prefer-const", "let wert = 1;\nexport default wert;\n", id="let"),
        pytest.param("eqeqeq", "export const gleich = (x, y) => x == y;\n", id="=="),
        pytest.param("no-unused-vars", "const ungenutzt = 1;\n", id="ungenutzt"),
        pytest.param("complexity", zuKomplexeFunktion, id="16"),
        pytest.param(
            "no-restricted-properties",
            'export const knoten = document.createElement("div");\n',
            id="createElement",
        ),
        pytest.param(
            "no-restricted-properties",
            'export const knoten = document.createElementNS("x", "g");\n',
            id="createElementNS",
        ),
        pytest.param("no-restricted-properties", 'document.write("a");\n', id="write"),
        pytest.param(
            "no-restricted-syntax",
            'document.body.innerHTML = "<span></span>";\n',
            id="innerHTML",
        ),
        pytest.param(
            "no-restricted-syntax",
            'document.body.outerHTML = "<span></span>";\n',
            id="outerHTML",
        ),
        pytest.param(
            "no-restricted-syntax",
            'document.body.insertAdjacentHTML("beforeend", "<span></span>");\n',
            id="insertAdjacentHTML",
        ),
        pytest.param("arbiter/kommentare", "// erklärt nur\nexport const eins = 1;\n", id="Prosa"),
        pytest.param("arbiter/kommentare", "/* Block */\nexport const eins = 1;\n", id="Block"),
        pytest.param("arbiter/kommentare", "// Warum: TODO\nexport const eins = 1;\n", id="TODO"),
    ],
)
def testEinVerstoßGegenDieJavaScriptRegelIstRot(tmp_path, regel, quelltext):
    probeAnlegen(tmp_path, "seite.js", quelltext)
    assert regel in eslintVerstöße(tmp_path)


@pytest.mark.parametrize(
    ("regel", "quelltext"),
    [
        pytest.param("selector-class-pattern", ".mein-kind { margin: 0; }\n", id="kebab"),
        pytest.param("custom-property-pattern", ":root { --mein-wert: 1px; }\n", id="Variable"),
        pytest.param("arbiter/farbenNurInRoot", ".karte { color: #fff; }\n", id="Hex"),
        pytest.param("arbiter/farbenNurInRoot", ".karte { color: rgb(1, 2, 3); }\n", id="rgb"),
        pytest.param("color-named", ":root { --rand: red; }\n", id="Name"),
    ],
)
def testEinVerstoßGegenDieCssRegelIstRot(tmp_path, regel, quelltext):
    probeAnlegen(tmp_path, "seite.css", quelltext)
    assert regel in stylelintVerstöße(tmp_path)


def testFehlendeWerkzeugeSindRotMitDemBefehlZumInstallieren(tmp_path):
    with pytest.raises(AssertionError, match="npm install"):
        verstöße(tmp_path)


def testDerLeereOrdnerIstGrün(tmp_path):
    probeAnlegen(tmp_path, "seite.js", verstoßFreiesJavaScript)
    (tmp_path / frontendOrdner / "seite.js").unlink()
    assert verstöße(tmp_path) == []


def testBeideWerkzeugeMeldenGetrennt(tmp_path):
    probeAnlegen(tmp_path, "seite.js", "var wert = 1;\nexport default wert;\n")
    (tmp_path / frontendOrdner / "seite.css").write_text(".mein-kind { margin: 0; }\n")
    assert len(verstöße(tmp_path)) == beideWerkzeuge


@pytest.mark.stand
def testDasFrontendIstSauber():
    assert verstöße(wurzel) == []


def testDiePaketdateiPinntDieMinorVersionenMitBegründung():
    paket = json.loads((wurzel / "package.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"9\.\d+\.\*", paket["devDependencies"]["eslint"])
    assert re.fullmatch(r"16\.\d+\.\*", paket["devDependencies"]["stylelint"])
    assert set(paket["warum"]) == {"eslint", "stylelint"}


def testNodeModulesSindIgnoriert():
    zeilen = (wurzel / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "node_modules/" in zeilen
