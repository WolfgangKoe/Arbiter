# Akzeptanztests zu Item anhaltenAnBases: Fälle abseits des Happy Path

1352 · Kritik · von Fachkritiker → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet. Die Tests treffen AUF-24.1 und 26.2 bis 26.4. Die
Annahme aus [1320](1320-kreuztDieStreckeEineBaseUndLiegtDasZielFrei.md) folgt dem Kriterium:
Liegt das Ziel frei, springt das *Modell* über die *Base*. Es fehlen vier Fälle:
1. AUF-26.2 gilt für die *Base* jedes anderen *gesetzten* *Modells*. Die Tests halten ein
   *Modell* nur an *Bases* seiner eigenen *Einheit* an. Schritt 5 im Plan („es hält ebenso
   an“) meint aber auch fremde *Bases*.
2. AUF-26.2 zieht die gerade Strecke zur hineingerückten *Stelle* nach 26.1, nicht zum
   Punkt des Loslassens. Im Fall `anDerHineingerücktenStelle` liegen beide auf einer Linie,
   deshalb prüft der Test den Unterschied nicht.
3. AUF-26.3 nach AUF-21.2: Ein Block wird über die Grenze der Zone gezogen und stößt dabei
   an eine fremde *Base*. Dazu gibt es keinen Test.
4. AUF-24.1 mit 26.3 prüfen Dienst und Seite nicht, also einen Block, der schon beim Halten
   vor einer fremden *Base* steht. Diese Tests decken nur das Hineinrücken ab. Plan,
   Schritt 4, sagt: „hält schon beim Ziehen … vor fremden *Bases* an“. Diesen Fall prüft
   nur die Domäne.

**Kosten.** Je Fall ein Parameter oder ein Test. Ohne diese Fälle fällt ein Fehler nur an
seltenen Stellen nicht auf. Bei 4 ist er sichtbar, verlangt aber, dass die Seite der Antwort
des Dienstes nicht folgt.

**Gegenvorschlag.** In der nächsten Technikphase:
1. `testAuf26_2…OhneGrund` mit einem *Modell* einer anderen *Einheit* im Weg
   (`andereEinheitAufgestellt`), dazu die *Ebene* als *Modell*.
2. Einen `Zug`, der schräg über die Grenze führt: Start (4″, 20″), Loslassen (12″, 26″),
   *Base* im Weg an der hineingerückten *Stelle* (9″ − 1 Radius, 26″). Die Strecke endet dort.
3. Ein Domänentest zu 26.3: Das Ziel liegt jenseits der Innenkante, die fremde *Base* liegt
   an der hineingerückten *Stelle*.
4. `testAuf24_1DieKarteZeigtBeimHalten…` mit dem Fall `blockVorEinerFremdenBase` oder
   `warbossVorDenBoyz`.

**Stellungnahme.** Alle vier Fälle umgesetzt, mit zwei Abweichungen (unten):
1. `anhaltenAnEinerBaseTest.py`: `testAuf26_2EinModellHältAnDerBaseEinesModellsEinerAnderenEinheitAnOhneGrund`
   mit `andereEinheitAufgestellt`, je ohne Auswahl und mit dem *Modell* als *Ebene*.
2. `anhalten.py`: neuer `Zug` `schrägÜberDieGrenze` (Start 4″/20″, Loslassen 12″/26″, *Base* im Weg bei
   9″ − 1 Radius/26″). Er steht auch in den Zügen der Abfrage (26.4). Dazu
   `testAuf26_2ZielDerStreckeIstDieHineingerückteStelleNichtDerPunktDesLoslassens`.
3. `anhaltenAnEinerBaseTest.py`: `testAuf26_3NachDemHineinrückenKürztDerBlockDenWegVorEinerBaseAnDerHineingerücktenStelle`
   (Domäne, beide *Modelle* als gezogenes): Das *Ziel* liegt bei 12″, die fremde *Base* an der
   hineingerückten *Stelle*; alle *Modelle* gehen um denselben Weg, die *Base* des gezogenen
   liegt auf der Strecke zur hineingerückten *Stelle* und stößt an, nichts überdeckt.
4. `blockAlsGanzesTest.py`: `testAuf24_1DieKarteZeigtBeimHaltenDenBlockVorEinerFremdenBaseDortWoErBeimLoslassenSteht`
   (Maus und Finger) mit `blockVorEinerFremdenBase`.

Abweichung zu 2: Die Strecke prüft der Test mit `liegtNahAnDerStrecke` (Toleranz 1e-9) statt
exakt, weil die Richtung (5 − Radius, 6) kein Pythagoras-Dreieck ist und der Halt am Raster sonst
keine exakte Gerade ergäbe; die Strecke zum Punkt des Loslassens würde trotzdem verfehlt, denn
der Test verlangt den Halt an der *Base*.
Abweichung zu 4: nur das erste *Modell* gezogen, weil ein Test mit beiden Fällen mehr als fünf
Parameter bräuchte; den Fall mit dem zweiten *Modell* prüft die Domäne bei 24.1 schon.

Alle Tests laufen mit dem vorhandenen Code grün (523 bestanden in `phasen/aufstellen`), ruff
und Format sind sauber.

Nachgeprüft (Fachkritiker): in Ordnung, beide Abweichungen trage ich mit. Mit einer Strecke zum
Punkt des Loslassens (Mutation in `/tmp`) sind die neuen Tests zu 26.2 und 26.3 rot.
