# Der Test zu AUF-8.4 ruft `modellZurücklegen` auf

1190 · Kritik · von Implementierer → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, denn eine Prüfung ist rot.
`testAuf8_4EinModellEinerAufgestelltenEinheitIstAufEinerAblageNichtWählbar` in
[ziehenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py) ruft
`aufstellung.modellZurücklegen` auf. Nach [V5](../../technik/architektur/handlungen.md) heißt
die Handlung `modellAufAblageLoslassen`; die Tests zu AUF-12.5 und AUF-16 rufen sie so auf.

**Kosten.** Rot bleibt der Commit gesperrt; ein zweiter Name für dieselbe Handlung wäre Altlast.

**Gegenvorschlag.** Im Test `modellAufAblageLoslassen` aufrufen. Erledigt, wenn der Test grün ist.

**Stellungnahme.**
Angenommen und umgesetzt: Der Test ruft `modellAufAblageLoslassen` auf, ziehenTest.py ist grün.
