import shlex
from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import projektordner, relativZurWurzel
from lesen.agenten import darfSchreiben, schreibpfade
from rollenregeln.bashSchreiben import (
    ausweg,
    liegtInTmp,
    nichtLesbar,
    verbotenesSchreiben,
    weg,
)
from rollenregeln.entfernen import urteil
from rollenregeln.pfadsperren import pfadsperren
from rollenregeln.regelnNurInProzessphase import regelnGesperrt, regelnMeldung

schreibwerkzeuge = ("Write", "Edit")
koordinator = "koordinator"
abhakenModule = ("standregeln.abhaken", "standregeln.hindernis")


def abhakenFürAndere(befehl: str, rolle: str | None) -> bool:
    try:
        wörter = shlex.split(befehl)
    except ValueError:
        return False
    modul = next((wort for wort in wörter if wort in abhakenModule), None)
    if modul is None:
        return False
    genannt = wörter[wörter.index(modul) + 1 : wörter.index(modul) + 2]
    return not genannt or genannt[0].casefold() != (rolle or "").casefold()


def vorBash(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    if eingabe.rolle == koordinator:
        return None
    if abhakenFürAndere(str(eingabe.angaben.get("command") or ""), eingabe.rolle):
        return verweigerung(
            f"Schreibgrenze: {eingabe.rolle} hakt und meldet nur eigene Zeilen: "
            f"`lauf.py {abhakenModule[0]} {eingabe.rolle} <Schritt>`."
        )

    def entfernenDerRolle(name: str, wörter: list[str]) -> str | None:
        return urteil(name, wörter, eingabe.rolle, wurzel)

    gefunden = verbotenesSchreiben(str(eingabe.angaben.get("command") or ""), entfernenDerRolle)
    if gefunden is None:
        return None
    hinweis = ausweg if gefunden == nichtLesbar else ""
    return verweigerung(
        f"Schreibgrenze: {eingabe.rolle} darf per Bash nicht schreiben ({gefunden}). {weg}{hinweis}"
    )


def vorDemSchreiben(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    rolle = eingabe.rolle
    if not rolle:
        return None
    if eingabe.werkzeug == "Bash":
        return vorBash(eingabe, wurzel)
    if eingabe.werkzeug not in schreibwerkzeuge:
        return None
    angaben = eingabe.angaben
    ziel = Path(angaben.get("file_path") or "")
    relativ = relativZurWurzel(ziel, wurzel)
    außerhalb = relativ is None
    if relativ is None:
        relativ = str(ziel)
    for gesperrt, meldung in pfadsperren:
        if gesperrt(relativ):
            return verweigerung(f"Schreibgrenze: {relativ}: {meldung}")
    if not außerhalb and regelnGesperrt(relativ, wurzel, rolle):
        return verweigerung(f"Schreibgrenze: {relativ}: {regelnMeldung}")
    if (außerhalb and liegtInTmp(relativ)) or darfSchreiben(relativ, schreibpfade(rolle, wurzel)):
        return None
    return verweigerung(
        f"Schreibgrenze: {rolle} darf {relativ} nicht schreiben. "
        "Kritik an fremden Artefakten wird ein Anliegen."
    )


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    return vorDemSchreiben(eingabe, wurzel) if eingabe.ereignis == "PreToolUse" else None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
