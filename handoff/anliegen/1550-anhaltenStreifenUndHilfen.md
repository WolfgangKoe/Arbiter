# Kritik am Code zu Item anhaltenAnBases: Streifen ungeprüft, Weg doppelt, Abfrage der Seite

1550 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Lesbarkeit ([Es](../../prozess/praemissen/es.md)) und Korrektheit seit `79d1cd4`, Teil
anhaltenAnBases. `anteilBisZurBerührung` stimmt: 400 zufällige Fälle gleich dem Abzählen aller
Schritte. Nichts hält auf ([Ich 3](../../prozess/praemissen/ich.md): Randfälle, Hilfen, keine
Prüfung im Code rot). Geprüft: `technik/tests` 722 grün, `ruff` grün; `prozess/pruefungen` rot nur
der Spiegel in `modellPerKlickTest.py` (AUF-25.1 nach 25.2), Datei des Testautors in Arbeit.
1. [messen.py](../../technik/arbiter/domaene/messen.py), `_ersterÜberdeckenderSchritt`: Der Zweig
   `return danach if überdecktAm(danach) else None` ist ungeprüft; `return None` dort lässt alle
   Tests außer den Bildschirmtests grün. Er trägt den Fall, dass eine *Base* eine andere am Ende
   nur streift: 10″-*Base* von (0, 0) um (20, 0), ruhende bei (19,9998; 9,9999975), Anteil
   1999/2000. Ohne den Zweig bricht `min` ab, `web/` antwortet 500.
2. Den Weg zwischen zwei *Stellen* rechnen `angehalten` und `verschobeneStellen` je selbst
   (`(ziel.x - davor.x, ziel.y - davor.y)`), das Gegenstück zu `verschoben` fehlt in `messen.py`.
3. `messen.py`: `_BaseAnStelle` steht mitten im Modul und wiederholt den Inhalt von
   `BasenAnStellen`; die innere `überdecktAm` und `_überdecktAm` unterscheidet nur der Unterstrich.
4. [anwendung.py](../../technik/arbiter/web/anwendung.py): `_zahlAusDemText` baut nach, was
   `request.args.get(name, type=float)` kann (None bei fehlend oder keiner Zahl), wie
   `ablageDerAnfrage` es mit `type=int` tut.
5. [seite.js](../../technik/frontend/seite.js): Der Kommentar in `ziehenBeginnen` sagt, alle
   *ausgewählten* folgen um denselben Weg; seit V10 setzt sie die Abfrage, `kreise` dient nur dem
   Zurücksetzen. `ziehenBeenden`: „Der gezogene Kreis liegt unter dem Zeiger“ gilt nach dem
   Anhalten nicht mehr immer.
6. `seite.js`, `stelleBeimLoslassenAbfragen`: Beginnt ein Zug, während die Abfrage des vorigen
   läuft, verwirft sie dessen ersten Punkt (`ziehenStart === zug` ist falsch); hält der *Spieler*
   dann still, zeigt die *Karte* den Block am Start, bis er den Zeiger bewegt.
7. Effizienz: Eine Abfrage für 30 *Modelle* gegen 60 fremde braucht 0,05 bis 0,15 s, je
   Zeigerbewegung; jedes Paar wird gesucht, auch weit abseits des Wegs.

**Kosten.** Zu 1: Ein Rückfall dort wird erst als 500 beim Loslassen sichtbar; der Mutationslauf
vor dem Review nennt ihn. Zu 2 und 3: Eine Änderung am Weg oder am Paar trifft mehrere Stellen.
Zu 4: Eine Hilfe mehr für Flask-Verhalten. Zu 5: Der Leser sucht ein Mitziehen, das es nicht
gibt. Zu 6 und 7: Die *Karte* zeigt kurz einen alten Stand oder hinkt dem Zeiger nach.

**Gegenvorschlag.**
1. Unit-Test in [messenTest.py](../../technik/tests/einheit/domaene/messenTest.py) mit dem Fall
   aus Befund 1: Halt ohne Überdeckung, höchstens 1/100″ vor der Berührung.
2. `wegZwischen(von: Stelle, nach: Stelle) -> Weg` in `messen.py`, beide rufen sie.
3. `type BaseAnStelle = tuple[Base, Stelle]` oben, `BasenAnStellen = Collection[BaseAnStelle]`;
   die innere Funktion etwa `überdecktBeiSchritt`.
4. `request.args.get(name, type=float)`, `_zahlAusDemText` entfällt.
5. Kommentare nach V10, ohne dass `seite.js` wächst ([1440](1440-kritikAmCodeAnhaltenAnBases.md), 4).
6. `wartenderPunkt` merkt sich seinen Zug (`{ zug, stelle }`), gesendet wird, wenn er
   `ziehenStart` ist.
7. Nach deinem Urteil: vor der Suche nur Paare, deren ruhende *Base* das Rechteck um den Weg
   samt beiden Radien berührt.

Erledigt: umgesetzt oder begründet abgelehnt, Tests grün, Verhalten unverändert außer 6.

**Stellungnahme.**
Alle sieben Punkte umgesetzt, Tests grün.
1. Unit-Test `testDerWegHältAuchBeiEinemBloßenStreifenAmEndeVorDerBerührung` mit dem Fall aus dem Befund.
2. `messen.wegZwischen`, beide rufen sie (siehe 1540, Punkt 1).
3. `BaseAnStelle` steht oben und ist öffentlich, `BasenAnStellen` nutzt es; die innere Funktion heißt
   `überdecktBeiSchritt`.
4. `_zahlAusDemText` entfällt, `request.args.get(name, type=float)` ersetzt sie; 400 wie bisher.
5. Kommentare in `ziehenBeginnen` und `ziehenBeenden` nach V10, ohne dass `seite.js` wächst.
6. `wartenderPunkt` ist `{ zug, punkt }`, gesendet wird, wenn `zug` der aktuelle `ziehenStart` ist.
7. Umgesetzt: `anteilBisZurBerührung` sucht nur Paare im Rechteck um den Weg samt beiden Radien
   (`_imRechteckUmDenWeg`); das Ergebnis bleibt gleich, denn eine Überdeckung liegt immer darin.
   Zeit der Abfrage nicht neu gemessen.
