# Kritik am Code zu Item anhaltenAnBases: Typalias rot, Reste des gesperrten Modells

1440 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt
## Runde 1
**Befund.** Der Schnitt passt: `anhaltenAnEinerBase.py` spiegelt AUF-26 und misst nur mit `messen.anteilBisZurBerührung` (M1, S3), `stellenBeimLoslassen` ist die Abfrage aus [V10](../../technik/architektur/handlungen.md), `modellLoslassen` *setzt* genau deren *Stellen*. Geprüft: `ruff`, Unit-Tests (85), alle Tests unter `technik/tests`: rot nur die vier aus [1460](1460-vierTestsVerlangenWasDerCodeNichtLiefernKann.md).
1. Hält auf ([Ich 3](../../prozess/praemissen/ich.md): eine Prüfung ist rot): `formregeln/benennung.py` meldet „`messen.py`: Zeile 15: `BasenAnStellen`: nicht in camelCase“. Die Prüfung erkennt `Name = X[…]` nur für `tuple`, `list`, `dict` und Ähnliche, nicht für `Collection`.
2. Wartet ([Ich 3](../../prozess/praemissen/ich.md), Form): In `angehalten` sind die Zweige `if modell in stellen` tot. Nach `davor is None` ist jedes *Modell* in `neue` *gesetzt*: Der Block besteht nur aus *gesetzten*, allein ist es das gezogene. `_umAnteil` schreibt `tuple[Fraction, Fraction]` statt `messen.Weg`, `rückungInDieFläche` schreibt `Iterable[tuple[Base, Stelle]]` statt `BasenAnStellen`.
3. Wartet: `modellLoslassen` ruft `_wählbareEinheitVon` zweimal auf, einmal direkt und einmal in `stellenBeimLoslassen`.
4. Wartet ([Kennzahlen](../../prozess/kennzahlen.md), Höchstmaß Code-Modul 12.000): `frontend/seite.js` hat 12.486 Zeichen, im letzten Commit waren es 10.404. Bis zur Teilung (Item des Planers) wächst die Datei nicht mehr.
5. Hält auf (Ich 3: neuer Code verletzt die Architektur, [V10](../../technik/architektur/handlungen.md): „Kein *Modell* wird mehr *gesperrt*“): `_loslassen` legt bei einem *Grund* weiter ein `Gesperrtes` an, statt `Sperre` zu werfen. `gesperrtesModell.py`, `Gesperrtes`, `Grund.modellGesperrt` und das Feld `gesperrt` in `darstellung.py` stehen noch. Davon hängt [1430](1430-restDesGesperrtenModellsInDenKriterien.md) ab, sonst werden Spiegel und Glossar rot. Die Schuld liegt nicht bei dir allein: Der Vertrag, V1, V5 bis V7 und die drei Beispiele, nennt `gesperrt` noch, und das ist mein Schritt aus [Plan 6](../plan.md). Reihenfolge:
   1. Architekt: Vertrag ohne *gesperrtes* *Modell*, im nächsten Lauf.
   2. Testautor: `gesperrt(…)` und `gründeDerGesperrten` aus `ziehenTest.py`, `sperreOhneStelleTest.py` und `setzenPerKlickTest.py` streichen; dazu der Test zu AUF-12.1, falls es noch einen gibt.
   3. Implementierer: `gesperrtesModell.py` entfernen, dazu `_gesperrte`, `gesperrt`, `stelleDesGesperrten`, `gründeDesGesperrten`, `zurücknehmen`, `Grund.modellGesperrt` und das Feld `gesperrt` in `darstellung.py`. In `seite.js` fallen Kreis `gesperrt` und Knopf „zurück“ weg. Ein *Grund*, der nach dem Anhalten bleibt, wirft `Sperre`, und `zurück()` ändert nichts (AUF-17.1).
   4. Anforderungsautor: 1430.

   Bis 3 erledigt ist, ist das Item nicht fertig.

**Kosten.** Zu 1: Die Prüfungen sind rot, das Item kann nicht fertig werden. Zu 2 und 3: Der Leser sucht einen Fall, den es nicht gibt, und eine Messung des Wegs, die schon einen Namen hat.

**Gegenvorschlag.**
1. `type BasenAnStellen = Collection[tuple[Base, Stelle]]` und `type Weg = …`. Python 3.12 kann das, die Prüfung erkennt `type`.
2. Wenn billig: `bewegte = [(modell.base, stellen[modell]) for modell in neue]`, die Rückgabe entsprechend, `Weg` und `BasenAnStellen` in den Signaturen.
3. Wenn billig: `modellLoslassen` holt die *Einheit* über `einheitVon`, nachdem `stellenBeimLoslassen` geprüft hat.
4. Ohne Änderung: Nichts Neues mehr in `seite.js`. Schritt 5.3 macht die Datei nur kleiner.
5. Wie in Befund 5: Schritt 3, sobald der Testautor Schritt 2 erledigt hat. Bis dahin setzt du hier `· wartet auf` und die Nummer seines Anliegens.

**Stellungnahme.**
1. Angenommen und umgesetzt: `BasenAnStellen` und `Weg` in `messen.py` sind `type`-Aliase; `formregeln.benennung` und `ruff` grün, 679 Tests grün vor und nach.
2. Umgesetzt: `angehalten` ohne die toten Zweige (`bewegte` aus `neue`), `_umAnteil` mit `messen.Weg`, `rückungInDieFläche` mit `BasenAnStellen` und `Weg`.
3. Umgesetzt: `modellLoslassen` holt die *Einheit* mit `einheitVon`, nachdem `stellenBeimLoslassen` geprüft hat.
4. Angenommen: Nichts Neues in `seite.js`, sie ist durch 1443 kleiner geworden; die Teilung kommt als Item des Planers.
5. Umgesetzt mit [1443](1443-codeOhneGesperrtesModell.md) (Tests: 681 grün, `prozess/pruefungen` 729 grün).
