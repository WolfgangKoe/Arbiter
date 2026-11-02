# Meldung von einheitVon nach dem Umzug

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik am Code zu 6102 (`git diff e1fb48b`). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md) (Namen einer Hilfsfunktion, keine Prüfung rot):
`einheitVon` liegt jetzt in
[phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py) und dient auch
`Schlacht` in der *Bewegungsphase*; seine Meldung sagt weiter „Das Modell gehört nicht zur
Aufstellung“.

**Kosten.** Am Bildschirm nichts. Wer die Meldung in der *Bewegungsphase* liest, sucht den
Fehler in der *Aufstellung*.

**Gegenvorschlag.** Die Meldung ohne *Phase*, etwa „Das Modell gehört keinem der beiden
Spieler“.

**Stellungnahme.** Angenommen. Die Meldung lautet jetzt „Das Modell gehört keinem der beiden
Spieler“ ([phasen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/__init__.py)).

Status: angenommen
