# W3 nennt das gelöschte Kriterium AUF-12.1

1530 · Kritik · von Anforderungsautor → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält nicht auf, kein
Schritt des Happy Path und keine *Sperre* hängen daran. Mit
[1430](1430-restDesGesperrtenModellsInDenKriterien.md) ist AUF-12.1 (‚Modell gesperrt‘)
gelöscht; die Kennung kommt nicht wieder. [web.md, W3](../../technik/architektur/web.md) sagt
trotzdem noch: „Prüft: die Dienst-Tests zu AUF-12.6 und 12.7, zu AUF-12.1 gegen `sperre.json`.“

**Kosten.** W3 nennt einen Test zu einem Kriterium, das es nicht mehr gibt. Wer prüfen will,
was `sperre.json` absichert, sucht einen Test, den es nicht gibt.

**Gegenvorschlag.** „zu AUF-12.1“ aus W3 streichen und den Test nennen, der jetzt gegen
`sperre.json` prüft. Das Beispiel lädt `technik/tests/akzeptanz/dienst.py`; welcher Test es
nutzt, entscheidest du.
Erledigt, wenn `grep -n "AUF-12.1" technik/architektur/web.md` nichts findet.

**Stellungnahme.** Angenommen und umgesetzt. [W3](../../technik/architektur/web.md) nennt jetzt „zu AUF-10.3 gegen
`sperre.json`“: Gegen das Beispiel prüfen `testAuf10_3DerDienstSperrtDasBeendenMitDemBeispielDesVertrags`
(Dienst) und `testAuf10_3DieSeiteNenntBeimBeendenDenGrundDerSperreImBeispiel` (Seite) in
[beendenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/beendenTest.py), wie es
[handlungen.md](../../technik/architektur/handlungen.md) unter „Prüft“ schon sagt.
`grep -n "AUF-12.1" technik/architektur/web.md` findet nichts, ebenso nicht in `technik/architektur/`.

**Nachprüfung.** In Ordnung. W3 nennt AUF-10.3 statt AUF-12.1. Beide genannten Tests stehen
in `beendenTest.py` und prüfen gegen `sperreDesVertrags()`, also gegen `sperre.json`.
AUF-10.3 gibt es in [beenden.md](../../domaene/anforderungen/phasen/aufstellen/beenden.md).
`grep -rn "AUF-12.1" technik/architektur*` findet nichts.
