import json
from pathlib import Path
from urllib.parse import urlparse

klammern = "{}()[];,"


def einheitenJeZeichen(text: str) -> list[int]:
    anfänge = []
    stelle = 0
    for zeichen in text:
        anfänge.append(stelle)
        stelle += len(zeichen.encode("utf-16-le")) // 2
    anfänge.append(stelle)
    return anfänge


def ausgeführteEinheiten(skript: dict, länge: int) -> list[bool]:
    bereiche = [bereich for funktion in skript["functions"] for bereich in funktion["ranges"]]
    bereiche.sort(key=lambda bereich: (bereich["startOffset"], -bereich["endOffset"]))
    ausgeführt = [False] * länge
    for bereich in bereiche:
        for stelle in range(bereich["startOffset"], min(bereich["endOffset"], länge)):
            ausgeführt[stelle] = bereich["count"] > 0
    return ausgeführt


def skripteLesen(messdatei: Path) -> list[dict]:
    if not messdatei.exists():
        return []
    ergebnisse = [json.loads(zeile) for zeile in messdatei.read_text().splitlines()]
    return [skript for lauf in ergebnisse for skript in lauf]


def ausgeführtJeDatei(messdatei: Path, ordner: Path) -> dict[str, list[bool]]:
    jeDatei: dict[str, list[bool]] = {}
    for skript in skripteLesen(messdatei):
        pfad = urlparse(skript["url"]).path.lstrip("/")
        datei = ordner / pfad
        if not pfad.endswith(".js") or not datei.is_file():
            continue
        länge = einheitenJeZeichen(datei.read_text(encoding="utf-8"))[-1]
        bisher = jeDatei.setdefault(pfad, [False] * länge)
        neu = ausgeführteEinheiten(skript, länge)
        jeDatei[pfad] = [alt or jetzt for alt, jetzt in zip(bisher, neu, strict=True)]
    return jeDatei


def codezeilen(text: str) -> list[int]:
    anfänge = einheitenJeZeichen(text)
    zeichenJeZeile = 0
    ergebnis = []
    for zeile in text.splitlines(keepends=True):
        if zeile.strip().strip(klammern):
            ergebnis.append(anfänge[zeichenJeZeile + len(zeile) - len(zeile.lstrip())])
        zeichenJeZeile += len(zeile)
    return ergebnis


def zeilenabdeckung(messdatei: Path, ordner: Path) -> float:
    ausgeführt = ausgeführtJeDatei(messdatei, ordner)
    gesamt = 0
    gedeckt = 0
    for datei in sorted(ordner.rglob("*.js")):
        pfad = datei.relative_to(ordner).as_posix()
        stellen = codezeilen(datei.read_text(encoding="utf-8"))
        markiert = ausgeführt.get(pfad)
        gesamt += len(stellen)
        gedeckt += sum(1 for stelle in stellen if markiert and markiert[stelle])
    return 100 * gedeckt / gesamt if gesamt else 100.0
