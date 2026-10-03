# Aufstellungszone: die Fläche steht in Kommentaren statt in der Schnittstelle

130 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · erledigt

## Runde 1
Gegenstand: 3738e7b (Kritik am Code): `messen.ganzIn`, `Ausgangslage.tiefen`,
`Aufstellung._grenzenInX`, `katalog/ausgangslage.py`. Tests grün (138), Prüfungen grün.
A1, A2, A3 und M1 sind eingehalten; die Befunde betreffen nur die Form der Schnittstelle.

**Befund.**
1. `ganzIn(base, stelle, grenzenInX, länge)` beschreibt die Fläche ungleich: in x zwei
   Grenzen, in y nur eine Länge ab 0. Was gemeint ist, sagt erst der Docstring. Damit weiß
   `messen.py`, wo die Zone auf dem Spielfeld liegt (y beginnt bei 0). Nach S1 gehört das
   zur Aufstellung, nicht zur Messung. M1 verspricht „eine *Base* liegt *ganz in* einer
   Fläche“, jede Fläche.
2. `Ausgangslage.tiefen: tuple[Fraction, Fraction]` braucht einen `# Warum:`-Kommentar für
   die Reihenfolge und in `_grenzenInX` den Index `list(Aufstellungszone).index(zone)`
   (`wir.md`, Regel 6). Die Zuordnung Zone → Tiefe steht im Kommentar statt im Typ.
3. `katalog` liest `Spielfeldkante: 60` aus `onlyWar.yaml` nicht. S1 legt die Zonen an
   x = 0 und x = 44, also entlang der 60″. Ändert jemand die Kante in der YAML-Datei,
   ändert sich still nichts.

**Kosten.** Heute klein, aber jede Phase, die `ganzIn` ruft, erbt die Schieflage. Beispiel:
„ganz auf dem Spielfeld“ beim Bewegen wäre `ganzIn(base, stelle, (0, 44), 60)`. Eine Zone
an einer kurzen Kante oder in einer Ecke (andere Aufstellungskarten) lässt sich gar nicht
ausdrücken. Zu 2: Ein Tupel, dessen Bedeutung ein Kommentar erklärt, ist genau der Fall
„Zahl statt Begriff“. Zu 3: Daten und Code widersprechen sich, ohne dass ein Test rot wird.

Zum Vergleich, was gut lesbar ist: `überdecken` und `abstandHöchstens` im selben Modul
brauchen keinen Docstring, weil ihre Parameter symmetrisch sind und der Name die Frage stellt.

**Gegenvorschlag** (kleinster Schnitt, ohne neuen Begriff):
1. `ganzIn(base, stelle, grenzenInX, grenzenInY)`, beide als `(von, bis)`; der Docstring
   entfällt. `Aufstellung` berechnet beide Paare, y als `(0, länge)`.
2. `Ausgangslage.tiefen: dict[Aufstellungszone, Fraction]`. Der Katalog bildet es aus den
   Schlüsseln der YAML-Datei: `Aufstellungszone[name]` für `erste` und `zweite`. Kommentar
   und Index entfallen, die Namen in Daten und Code sind dieselben.
3. `katalog` wirft `ValueError`, wenn eine `Spielfeldkante` nicht der zweiten Seitenlänge
   entspricht (S1). Dazu ein Einheitstest in `tests/einheit/katalog/` (mit `__init__.py`).

Größerer Schnitt, nur wenn ihr ihn wollt: ein Wert `Fläche` mit beiden Grenzpaaren in
`spielobjekte.py`. Das ist eine neue Klasse der Domäne, braucht also einen Glossareintrag
(`glossar.py`) und damit ein Anliegen an den Anforderungsautor. Meine Empfehlung: jetzt den
kleinen Schnitt; `Fläche` erst, wenn eine zweite Aufstellungskarte kommt.

**Erledigt, wenn:** `ganzIn` nimmt zwei gleich gebaute Grenzpaare und hat keinen Docstring
zur Form; `tiefen` kommt ohne Index und ohne Kommentar aus; ein Einheitstest zeigt den
`ValueError` bei abweichender `Spielfeldkante`; Akzeptanztests unverändert grün.

**Stellung (Implementierer).** Angenommen, der kleine Schnitt, alle drei Punkte.
`ganzIn` nimmt zwei Grenzpaare, `tiefen` ist `dict[Aufstellungszone, Fraction]`, der Katalog
wirft bei abweichender `Spielfeldkante`; Test in `tests/einheit/katalog/ausgangslageTest.py`.
