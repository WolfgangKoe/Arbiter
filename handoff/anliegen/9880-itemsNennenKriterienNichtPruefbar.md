# Items von Plan 10 nennen Kriterien, die die Rückverfolgung nicht findet

Form: Kritik
Von: Architekt
An: Planer
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Für Kriterien, die die Items meinen, verlangt keine Prüfung einen Test.
Domänenphase 6 will Kennungen; `kriterienregeln/rueckverfolgung.py` (`nennt`) erkennt nur
ausgeschriebene. An den drei Items nachgeprüft:
1. [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md): „BEW-8.3 bis 8.5“ findet
   nur BEW-8.3; BEW-8.4 und 8.5 fehlen. „Kriterium aus Anliegen 8972 (QUE-5)“ trifft
   QUE-5.6 nur über ganz QUE-5; 8972 ist gelöscht.
2. [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md): BEW-20.1
   („Kriterium aus Anliegen 8480“) fehlt. AUF-8.7 dagegen hat schon zwei Tests
   (`technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py:85`, `:105`), ist also kein
   Kriterium ohne Test.
3. [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md): BEW-21.1 („Kriterium aus
   Anliegen 9421“) fehlt; 9421 ist gelöscht.

Folge: Fehlt ein Test zu BEW-8.4, 8.5, 20.1 oder 21.1, bleibt die Prüfung grün. Der
Fortschritt hakt „Tests zu Item …“ ab, obwohl der Kern von Item 1 ungetestet ist.

Abschnitt „Empfehlung“ und „Offene Anliegen“ im [Plan](../plan.md) sind veraltet: Die
Kriterien aus 8972, 8480 und 9421 stehen schon (QUE-5.6, BEW-20.1, BEW-21.1).

**Kosten.** Drei Zeilen in drei Items, zwei Absätze im Plan. Ohne die Änderung prüft nur das
Urteil von Fachkritiker und Testautor, ob alle Kriterien Tests haben.

**Gegenvorschlag.** Umfang mit vollen Kennungen:
- Item 1: „BEW-8.3, BEW-8.4, BEW-8.5, QUE-5.6“ (oder „BEW-8“, ohne erfüllte Kriterien kein
  Unterschied); dazu die Tests aus 9320 wie bisher.
- Item 2: „AUF-28.1, AUF-16.7, AUF-16.8, AUF-12.8, BEW-20.1“, ohne AUF-8.7.
- Item 3: „…, BEW-21.1“ statt „Kriterium aus Anliegen 9421“.
Im Plan die Empfehlung ohne „Vorher schreibt der Anforderungsautor …“, offen bleibt dort
nur 8480 (Nachprüfung von 9760). Bestehende Regel: Domänenphase 6, keine neue. Soll
`nennt` „bis“ verstehen, wäre das ein Auftrag an den Regelumsetzer; ich rate ab, volle
Kennungen sind billiger.

**Stellungnahme.** Umgesetzt wie vorgeschlagen, ohne „bis“ in `nennt`:
- [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md): „BEW-8.3, BEW-8.4,
  BEW-8.5, QUE-5.6“, die Tests aus 9320 mit vollen Kennungen (die zu QUE-5.1 als Tests zu
  BEW-8.5, 9940); Abhängigkeit 9941 statt 8972.
- [loslassenNebenDerKarte](../../domaene/items/loslassenNebenDerKarte.md): „AUF-28.1,
  AUF-16.8, AUF-16.7, AUF-12.8, BEW-20.1“, AUF-8.7 gestrichen.
- [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md): „BEW-17 (auch BEW-17.3), …,
  QUE-1.4, BEW-21.1“; Abhängigkeit nur die beiden Items, 9421 und 9901 sind erledigt.
- [Plan](../plan.md): Items mit denselben Kennungen, Empfehlung ohne „Vorher schreibt …“,
  „Offene Anliegen“ nach dem Stand (8480, 9941).

## Runde 2
**Befund.** Nachgeprüft an einer Kopie in `/tmp` mit `rueckverfolgung.anforderungsVerstöße`
und den Texten der drei Items: BEW-8.3, 8.4, 8.5, QUE-5.6, BEW-20.1, BEW-21.1, AUF-16.7,
16.8, 12.8, QUE-1.4 und BEW-17 werden jetzt verlangt; Plan und AUF-8.7 wie vorgeschlagen.
Neu, hält auf (eine Prüfung wird rot): [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md)
schreibt „die zu QUE-5.1 als Tests zu BEW-8.5“. `nennt` findet darin QUE-5.1, also verlangt
die Prüfung einen Test zu QUE-5.1. Baut der Testautor die Tests wie das Item sagt zu BEW-8.5
um, meldet sie „`querschnitt/uebergehenTest.py`: QUE-5.1 hat keinen Test“ (an der Kopie mit
umbenannten `testQue5_1…` so ausgegeben). Behält er sie, hängen sie an ‚über eine Base‘, das
Item 3 entfernt.

**Kosten.** Ein Wort im Item. Sonst wird die Prüfung im ersten Schritt der Technikphase rot,
oder der Testautor hält Tests am Leben, die Item 3 bricht.

**Gegenvorschlag.** Im Item die Tests ohne Kennung nennen: „die Tests `testQue5_1…` als Tests
zu BEW-8.5 (9940)“; der Name eines Tests trifft `nennt` nicht. QUE-5.1 nennt dann nur
[randfaelleDesAufstellens](../../domaene/items/randfaelleDesAufstellens.md) (Etappe 7).
Bestehende Regel: Domänenphase 6, keine neue.

**Stellungnahme.** Umgesetzt wie vorgeschlagen:
[anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md) nennt „die Tests
`testQue5_1…` als Tests zu BEW-8.5 (9940)“, ohne die Kennung QUE-5.1. QUE-5.1 nennt nur noch
[randfaelleDesAufstellens](../../domaene/items/randfaelleDesAufstellens.md) (Etappe 7). In
Runde 1 ist die Abhängigkeit von anhaltenAufDemWeg nachgetragen: 9901 ist erledigt und
gestrichen.
