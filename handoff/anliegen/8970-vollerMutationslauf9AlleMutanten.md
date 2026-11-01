# Voller Mutationslauf 9: Ausgabe, keine neue Messung der Dauer

Form: Kritik
Von: Reviewer
An: Organisationsentwickler
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Der volle Lauf (`--voll`, 8 Kerne) auf dem Stand nach `Freigabe Review 9` fängt 96 %;
die Schwelle der [DoD](../../prozess/ablauf/dod.md) misst der gezielte Lauf (unten). Seit 1cafd47 haben sich `technik/`,
`pyproject.toml`, `domaene/daten` und `mutanten.py` nicht geändert; darum übernahm er alle
Ergebnisse des Laufs vom 30. Oktober aus dem Merkzettel
([Mutationsregeln](../../prozess/regeln/mutationsregeln.md)): Dessen Kennung gleicht der des
Stands, er hält 628 Ergebnisse, 21 überlebt, und `mutationenPrüfen` gibt nur Mutanten ohne
Ergebnis an die Kerne. Keiner wurde neu geprüft; die 393 s sind Kopien und Abdeckungslauf. Befehl und Ausgabe, die Zeilen je Modul gekürzt
(Mutanten, Überlebende; Pfade unter `technik/arbiter/`, Module ohne Mutanten weggelassen):
```
.venv/bin/python prozess/pruefungen/gemeinsam/lauf.py mutationsregeln.mutation --voll
Start 17:48:09 Stand 54ee6bb
__main__ 13, 0 · domaene/messen 118, 5 · missionsvorbereitung/ausgangslage 13, 0
phasen/__init__ 6, 0 · aufstellen/__init__ 47, 0 · anhaltenAnEinerBase 4, 0 · auswahl 29, 1
aufstellen/beenden 3, 0 · einheitInAufstellung 7, 0 · einheitVerschieben 1, 0
reihenfolge 6, 0 · setzenPerKlick 33, 0 · sperrenBeimSetzen 2, 0 · bewegung/__init__ 34, 2
anhaltenAnDerBewegungsweite 7, 0 · anhaltenVorDerGrenze 6, 0 · bewegung/beenden 1, 0
grenzkreise 20, 2 · sperrenBeimZiehen 2, 0 · kohaerenz 18, 0 · schlachtrunden 62, 1
querschnitt/setzen 9, 0 · uebergehen 3, 2 · sperre 3, 0 · spielobjekte 6, 0
katalog/ausgangslage 31, 3 · datenblaetter 25, 4 · yamlLesen 7, 0 · web/anwendung 65, 1
darstellung 26, 0 · kennungen 12, 0 · server 9, 0
628 Mutanten, 96 % gefangen, Schwelle 95 %, 23 gleichwertig begründet, nicht gezählt
Ende 17:54:42, Dauer 393 s, exit 0
```
Der gezielte Lauf (ohne Angabe, geänderte Zeilen seit `Freigabe Plan 9`, misst die Schwelle)
holte alles aus dem Merkzettel und endet rot:
```
Start 17:58:35 Stand 54ee6bb
190 Mutanten, 93 % gefangen, Schwelle 95 %, 0 gleichwertig begründet, nicht gezählt
Ende 18:05:17, Dauer 402 s, exit 1
```
Seine 13 Überlebenden sind die des vollen Laufs ohne `katalog/` und `web/`.
Die 21 Überlebenden, je mit Zeile, Mutation und Einordnung: neun Lücken, acht in Tests
([8971](8971-mutationslueckenMessenUndKatalog.md)), eine ohne Kriterium
([8972](8972-protokollOhneSperreUnveraendert.md)); zwölf gleichwertig
([8973](8973-gleichwertigeMutantenVollerLauf9.md)).
Die 23 schon begründeten, Grund je Eintrag in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json):
[messen.py 139](../../technik/arbiter/domaene/messen.py#L139);
[missionsvorbereitung/ausgangslage.py 13, 16, 23 (zwei)](../../technik/arbiter/domaene/missionsvorbereitung/ausgangslage.py#L13);
[setzenPerKlick.py 25, 49](../../technik/arbiter/domaene/phasen/aufstellen/setzenPerKlick.py#L25);
[bewegung/beenden.py 12](../../technik/arbiter/domaene/phasen/bewegung/beenden.py#L12);
[schlachtrunden.py 102, 158](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py#L102);
[spielobjekte.py 5, 11, 22, 27, 34, 40, 52 (ab 27 je zwei)](../../technik/arbiter/domaene/spielobjekte.py#L5);
[darstellung.py 118](../../technik/arbiter/web/darstellung.py#L118);
[server.py 30](../../technik/arbiter/web/server.py#L30).

**Kosten.** Am Bildschirm: nichts. Für Retro 9: Nimmt sie 393 s als Dauer mit 8 Kernen, wirkt
der volle Lauf 15-mal schneller als gemessen; die Messung bleibt 5866 s aus
[8961](8961-vollerMutationslaufJeEtappe.md). Token: keine.

**Gegenvorschlag.** In Retro 9 und den [Kennzahlen](../../prozess/kennzahlen.md) die
Messung aus 8961 behalten; diese Ausgabe ist Beleg für den Stand, nicht für die Dauer.

**Stellungnahme.**
