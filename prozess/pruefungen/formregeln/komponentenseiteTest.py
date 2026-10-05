import pytest

from formregeln.komponentenseite import seitenDatei, stilDatei, verstöße
from gemeinsam.pfade import frontendOrdner, mockupOrdner, wurzel

stilProbe = ".einheitenKarte { color: red; }\n.spieler1 .name { margin: 0.5rem; }\n"
seiteProbe = (
    '<link rel="stylesheet" href="komponenten.css">'
    '<div class="einheitenKarte spieler1"><p class="name">x</p></div>'
)


@pytest.mark.stand
def testDieKomponentenseiteHältDieRegel():
    assert verstöße(wurzel) == []


def probe(
    tmp_path,
    stil: str | None = stilProbe,
    seite: str | None = seiteProbe,
    mockup: str | None = None,
):
    frontend = tmp_path / frontendOrdner
    frontend.mkdir(parents=True)
    if stil is not None:
        (frontend / stilDatei).write_text(stil, encoding="utf-8")
    if seite is not None:
        (frontend / seitenDatei).write_text(seite, encoding="utf-8")
    if mockup is not None:
        ordner = tmp_path / mockupOrdner
        ordner.mkdir(parents=True)
        (ordner / "a.html").write_text(mockup, encoding="utf-8")
    return tmp_path


def testVollständigeSeiteIstGrün(tmp_path):
    assert verstöße(probe(tmp_path)) == []


def testOhneStilDateiIstGrün(tmp_path):
    assert verstöße(probe(tmp_path, stil=None, seite=None)) == []


def testFehlendeSeiteNebenDemStilIstRot(tmp_path):
    assert verstöße(probe(tmp_path, seite=None)) == [
        f"{frontendOrdner}/{seitenDatei}: fehlt neben {stilDatei}"
    ]


def testSeiteOhneLinkAufDenStilIstRot(tmp_path):
    seite = '<div class="einheitenKarte spieler1"><p class="name">x</p></div>'
    assert verstöße(probe(tmp_path, seite=seite)) == [
        f"{frontendOrdner}/{seitenDatei}: verlinkt {stilDatei} nicht"
    ]


def testKlasseAusDemStilOhneClassIstTot(tmp_path):
    seite = seiteProbe.replace(" spieler1", "")
    meldungen = verstöße(probe(tmp_path, seite=seite))
    assert len(meldungen) == 1
    assert "spieler1" in meldungen[0]
    assert "tot" in meldungen[0]


def testZahlInEinemWertIstKeineKlasse(tmp_path):
    stil = ".einheitenKarte { margin: 0.5rem; }"
    seite = '<link href="komponenten.css"><p class="einheitenKarte">x</p>'
    assert verstöße(probe(tmp_path, stil=stil, seite=seite)) == []


def testKlasseImMockupOhneStilIstNeu(tmp_path):
    meldungen = verstöße(probe(tmp_path, mockup='<p class="einheitenKarte frisch">x</p>'))
    assert meldungen == [f"{mockupOrdner}/a.html: Klasse frisch fehlt in {stilDatei}, sie ist neu"]


def testKlasseInEinerFrontendSeiteOhneStilIstNeu(tmp_path):
    wurzelOrdner = probe(tmp_path)
    (wurzelOrdner / frontendOrdner / "index.html").write_text(
        '<p class="frisch">x</p>', encoding="utf-8"
    )
    assert verstöße(wurzelOrdner) == [
        f"{frontendOrdner}/index.html: Klasse frisch fehlt in {stilDatei}, sie ist neu"
    ]


def testBekannteKlassenInMockupsSindGrün(tmp_path):
    assert verstöße(probe(tmp_path, mockup='<p class="einheitenKarte name">x</p>')) == []
