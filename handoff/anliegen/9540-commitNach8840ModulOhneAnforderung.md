# Commit nach 8840: ein Modul ohne Anforderung

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Commit der Domäne und der Akzeptanztests zu
[8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md) und 9270 bis 9440 scheitert am
Commit-Hook. Jedes Modul der Domäne gehört zu einer Anforderung
([Grundschnitt der Domäne](../../technik/architektur/domaene.md)), geprüft von
`formregeln/spiegel.py`. `technik/arbiter/domaene/phasen/bewegung/sperrenBeimZiehen.py`
gehörte zu BEW-2 „Sperren beim Ziehen“; die ist nach 8840 gestrichen.

Was das Modul tut: Beim Loslassen in der *Bewegungsphase* sammelt es die *Gründe* einer
*Sperre*, die aus QUE-1 und ‚über eine Base‘. Das Erste verlangt jetzt BEW-1.5 („es sperrt nur
QUE-1“, [Normale Bewegung](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md)).
‚über eine Base‘ entfernt Technikphase 10 mit dem Item
[anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md)
([9440](9440-umbauNach8840HoechstePrioritaet.md)). Bis dahin sperrt Arbiter am Bildschirm
weiter ‚über eine Base‘, bei jeder Option unten. Das Modul behält also die Aufgabe aus BEW-1.5;
sein Name danach ist `normaleBewegung.py`.

**Kosten.** Alle drei erprobt an einer Kopie unter `/tmp/arch9/`, Token geschätzt.
- A, umbenennen: `sperrenBeimZiehen.py` heißt `normaleBewegung.py`, eine Importzeile in
  `phasen/bewegung/__init__.py` folgt. Commit-Hook grün (rot nur `frontendMessung.py` aus dem
  laufenden P7 des Regelumsetzers), 1.230 Produkttests grün. Ein kurzer Lauf des
  Implementierers, etwa 30.000 Token. Der Name stimmt schon für das, was bleibt; Technikphase 10
  streicht darin nur ‚über eine Base‘. Nachteil: Bis dahin steht in `normaleBewegung.py` eine
  Sperre, die BEW-1.5 nicht nennt; das ist die Lücke, die 9440 bewusst offen lässt.
- B, BEW-2 zurückholen: Hook ebenfalls grün, aber die Domäne widerspricht sich: BEW-2.5 sperrt
  ‚über eine Base‘, BEW-17 hält davor an, `domaene/ziel.md` schließt das Übergehen überdeckter
  Bases aus; BEW-2.8 verweist auf BEW-8.2, das es nicht mehr gibt. Ein Akzeptanztest
  dazu fehlt, die Anforderung stünde ungeprüft da. Zwei Läufe des Anforderungsautors
  (zurückholen, wieder streichen), etwa 60.000 Token.
- C, uncommittet lassen: heute keine Token. Die Arbeit aus 8840 und zehn Anliegen bleibt
  ungesichert über Prozessphase 9 und Domänenphase 10; jeder Commit dazwischen muss diese
  Dateien auslassen, die Freigaben der Domänenphase bauen auf Uncommittetem auf. Die
  Umbenennung aus A fällt in Technikphase 10 trotzdem an: organisatorische Schuld
  ([Absicht 2](../../prozess/praemissen/absicht.md)).

Keine Option: eine Ausnahme in `spiegel.py` bräuchte den Regelumsetzer, Ihre Ausnahme und
später deren Entzug ([Absicht 6](../../prozess/praemissen/absicht.md)), für dasselbe Ergebnis
wie A. Nebenbei: `mutationsregeln/gleichwertig.json` nennt `sperrenBeimZiehen` nur in einer
Begründung; der Eintrag fällt mit ‚über eine Base‘ in Technikphase 10.

**Gegenvorschlag.** A, vor dem Commit, im selben Commit wie Domäne und Tests. Rückweg: die
Datei zurück umbenennen und die Importzeile zurücksetzen.

**F1 · Wie wird der Commit grün?**
A: Der Implementierer benennt das Modul jetzt in `normaleBewegung.py` um (Architektur, Grundschnitt der Domäne)
B: Die Anforderungsdatei BEW-2 kommt bis Technikphase 10 zurück (neu)
C: Domäne und Tests bleiben uncommittet bis Technikphase 10 (neu)
Empfehlung: A, sie ist die billigste, lässt die Domäne widerspruchsfrei und gibt dem Modul den Namen, den es nach dem Umbau ohnehin trägt.
Antwort: A

Ihr Schritt: im Dashboard F1 mit dem Buchstaben beantworten; bei A beauftragt der Koordinator
den Implementierer, danach geht der Commit durch.

**Stellungnahme.** Umgesetzt nach A: `sperrenBeimZiehen.py` heißt `normaleBewegung.py`, die
Importzeile in `phasen/bewegung/__init__.py` folgt.
