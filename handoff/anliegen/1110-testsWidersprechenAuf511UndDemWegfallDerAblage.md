# Bestehende Tests widersprechen AUF-5.11 und dem Wegfall des Ziehens aus der Ablage

1110 · Fragen · von Testautor → Architekt · Runde 1/3 · erledigt

## Runde 1
**Befund.** Zu Item setzenPerKlick sind erst die Tests zu AUF-18 und AUF-19.4 geschrieben
([setzenPerKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/setzenPerKlickTest.py),
[gesperrterKlickTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/gesperrterKlickTest.py));
sie sind rot, weil `Aufstellung.karteAnklicken` fehlt. Offen und im Bestand noch nicht
angepasst:
1. [auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py) hält zwei
   *ausgewählte* *Einheiten* zugleich (AUF-5.4 „LässtDieAndere…“, AUF-5.8, 5.10); AUF-5.11 und
   die *Auswahl* im Glossar kennen höchstens eine. Dort müssen 5.3 und 5.6 durch 5.11 und 5.12
   ersetzt werden, das Beispiel des Vertrags (`spielstand.json`) hat kein `inAufstellung` mehr.
2. Tests, die eine *Einheit* aus der *Ablage* ziehen (`einheitZiehen`, `einheitLoslassen`,
   `einheitAufAblageLoslassen`): AUF-8.5, 8.6, 14.1, 15.1, 16.1, 16.2, 16.4, 16.5 fallen weg,
   ebenso `testQue3_4EineEinheitAufDieKarteZiehen…` in `bedienungTest.py`. `handgriffe.eineGesperrteFormation`
   und `einGesperrtesModell` brauchen den Weg „Ziehen auf ein *gesetztes*“ (Plan 6).
3. Die Schnittstelle, die ich festlege: `karteAnklicken(stelle)`, `auswählen(einheit)`
   (setzt jede andere ab), `modellSetzen` bleibt für Vorgeschichten.

**Kosten.** Ohne die Anpassung bleiben Tests rot oder prüfen Entfallenes.

**Gegenvorschlag.** Ich setze sie in der nächsten Sitzung um; bitte prüfe 3.

**Stellungnahme.** Alle drei Punkte gelten, mit diesen Ergänzungen:
1. Es fallen alle Tests weg, die zwei *ausgewählte* *Einheiten* zugleich voraussetzen (auch
   5.3 „LässtDieAndere…“, 5.10 „DieAndere…“). Die Beispiele sind schon angepasst:
   [spielstand.json](../../technik/architektur/vertrag/spielstand.json) und
   [sperre.json](../../technik/architektur/vertrag/sperre.json) ohne `inAufstellung`; nach V2
   ist nach dem Warboss, dann den Necron Warriors nur noch diese *ausgewählt*. Die
   *Einheit in Aufstellung* bleibt in der Domäne (`einheitInAufstellung`, AUF-7.1, 5.8),
   fehlt nur im JSON.
2. Die Liste deckt sich mit dem Item. Mit AUF-15.1 und dem Test zu AUF-9.1
   „EinModellDerFormation…“ (Weg AUF-8.5) hat `eineGesperrteFormation` keinen Nutzer mehr:
   löschen, nicht umbauen; die *gesperrte* *Formation* kommt mit dem Block (Items 2, 3).
   `einGesperrtesModell`: zwei *Modelle* mit `modellSetzen`, das zweite mit
   `modellLoslassen` auf das erste (AUF-8.2), ohne `auswählen`, so gilt es auch nach
   AUF-21.1 wie [V6](../../technik/architektur/handlungen.md). Gleiches gilt für jeden Test,
   dessen Handlung `modellLoslassen` mit einem nicht *gesetzten* *Modell* ist (AUF-9.1
   „AußerhalbDerZone“, „AufDemModellDesAnderenSpielers“): Das ist Ziehen aus der *Ablage*,
   in der Domäne offen bis AUF-16.7 (Plan 7). `einheitZiehen` (ziehen.py) und
   `einheitAufAblageLoslassen` (dienst.py) fallen mit weg. QUE-3.4 bleibt mit den Tests zum
   *Modell* belegt.
3. Bestätigt, wie V3 und V5:
   - `karteAnklicken(stelle)` ohne *Einheit*: Welcher sie gilt, entscheidet die Domäne
     (V5). Sperren nach AUF-19.4 und 12.1 als `Sperre` vor jeder Änderung (D2). Ob der Klick
     ein *Modell* trifft, entscheidet die Seite (V8). Dienst: `PUT /api/karteAnklicken`.
   - `auswählen(einheit)` setzt jede andere ab, auch die des anderen *Spielers* (Glossar,
     *Auswahl*); `abwählen` bleibt (AUF-5.4).
   - `modellSetzen` bleibt: das *Setzen* der Domäne nach QUE-1 und AUF-7.2, 7.3 (dort die
     Handlung) und für Vorgeschichten, ohne Route; neu in V5. Warum keine Vorgeschichten
     per Klick: Jede hinge dann an der *Formation* und an AUF-18.3.
