from arbiter.domaene.spielobjekte import Einheit, Modell, Spieler


def einheitVon(beideSpieler: tuple[Spieler, Spieler], modell: Modell) -> Einheit:
    for spieler in beideSpieler:
        einheit = spieler.armee.einheitVon(modell)
        if einheit is not None:
            return einheit
    raise ValueError("Das Modell gehört keinem der beiden Spieler")


def gegnerVon(beideSpieler: tuple[Spieler, Spieler], spieler: Spieler) -> Spieler:
    return next(andere for andere in beideSpieler if andere is not spieler)
