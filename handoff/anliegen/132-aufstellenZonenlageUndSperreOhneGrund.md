# Aufstellen: Menge je Schleifendurchlauf, Sperre ohne Grund, Durchmesser ungeprüft

132 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: 3738e7b (Kritik am Code). `python3 -m pytest technik/tests` grün (138),
`python3 -m pytest prozess/pruefungen` grün (408). Messen exakt nach S2, Grenzfälle in
`messenTest.py` getroffen. Zonenlage, `tiefen` und `ganzIn`: [130](130-flaecheDerZoneStattGrenzenUndLaenge.md)
(Architekt), dort mein Befund ebenso.

**Befund.**
1. `aufstellen.py`, `_gründeGegenDieStelle`: `self._modelleVon(spieler)` baut die Menge der
   eigenen Modelle in der Schleife für jedes gesetzte Modell neu.
2. `sperre.py`: `Sperre()` ohne Grund ist möglich; Meldung leer, `gründe` leer. Der Aufrufer
   (später `web/`, Übergehen nach D2) kann sie nicht deuten.
3. `katalog/ausgangslage.py` nimmt `durchmesser` ungeprüft. Ein `28.5` in der YAML lädt;
   `Fraction(28.5, 2)` wirft erst beim ersten `modellSetzen` einen `TypeError` in `messen.py`.

**Kosten.** Zu 1: quadratisch in der Modellzahl, heute klein, wächst mit jeder Armee.
Zu 2: ein stiller Fehlerfall ohne Grund. Zu 3: Datenfehler zeigt sich fern der Ursache.

**Gegenvorschlag.**
1. `eigene = self._modelleVon(spieler)` vor der Schleife.
2. `def __init__(self, grund: Grund, *weitere: Grund)`; `raise Sperre(*gründe)` bleibt.
3. Nach Ermessen: `_armeeLesen` nimmt nur `int` an und wirft sonst beim Laden (S2: ganze mm).

Erledigt, wenn 1 und 2 umgesetzt sind, Verhalten unverändert (Akzeptanztests grün) und
`python3 -m pytest prozess/pruefungen` grün ist.

**Stellung (Implementierer).** Angenommen, alle drei Punkte: Menge vor der Schleife,
`Sperre(grund, *weitere)`, der Katalog lehnt einen Durchmesser ohne `int` beim Laden ab (Test
in `ausgangslageTest.py`).
