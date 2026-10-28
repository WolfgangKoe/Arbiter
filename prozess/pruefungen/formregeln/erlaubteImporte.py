kastenNamen = ("seite", "web", "anwendung", "katalog", "speicher", "domaene", "start")
alleAußerStart = frozenset(kastenNamen) - {"start"}

erlaubteZiele = {
    "start": alleAußerStart,
    "web": frozenset({"anwendung"}),
    "anwendung": frozenset({"domaene"}),
    "katalog": frozenset({"domaene"}),
    "speicher": frozenset({"anwendung"}),
    "domaene": frozenset(),
    "seite": frozenset(),
}


def kastenDesModuls(modul: str) -> str | None:
    teile = modul.split(".")
    if teile[0] != "arbiter" or len(teile) == 1:
        return None
    return teile[1]


def pfeilErlaubt(von: str, nach: str, mitCode: frozenset[str]) -> bool:
    if von == nach or nach in erlaubteZiele.get(von, frozenset()):
        return True
    return von == "web" and nach == "domaene" and "anwendung" not in mitCode
