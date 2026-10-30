# Moderation

Stand: Technikphase 9, Plan 9 freigegeben ([Plan](plan.md)). Bisher hat niemand bearbeitet:
Implementierer 5380, 5701, 6122, 6982, 6991, 6992; Testautor 4901, 4921, 5241, 5781, 6340, 6981,
6993; Reviewer 6361; Architekt 7023. Sie alle sind dran; keines ist vergessen.

## Dran
Blockiert das Inkrement (Fortschritt im Plan):
- Item 2: [7300](anliegen/7300-uebergehenNichtMehrAngebotenOhneVorbedingung.md) und
  [7320](anliegen/7320-uebergehenBenanntUndKnopfVorDerHandlung.md), Testautor; sie halten die
  Kritik an den Tests auf, der Implementierer wartet darauf.
- Item 1: nichts Offenes mehr außer den Haken (7150, 7190, 7200, 7210 sind erledigt);
  7191 und 7201 warten auf Technikphase 10.
- Items 3 und 4: Kritik der Tests und Tests zu Item 4 stehen aus, keine Anliegen offen.
Je Rolle:
- Testautor: 7300, 7320; dann 4901, 5241, 4921, 5781, 6340 (Bewegungstests); 6993; 6981.
- Implementierer: 5380; 6122, 5701; 6991, 6992; 6982.
- Reviewer: 6361 (vor dem Review 9). Architekt: 7023, Rückfrage, du verstehst F1 nicht: Er
  klärt in seiner Stellungnahme, ohne Entscheidung von dir.
- Regelumsetzer: Nachprüfung 7031. Du: Nachprüfung 6400, 6410, 6420 (erst nach Items 3, 4).

## Vorschläge
- Haken im Fortschritt: „Architekt: Kritik an den Tests zu Item gemeinsamUebergehen“ ist
  abgehakt, obwohl 7320 aufhält (Schnittstelle: Test scheitert am Aufruf, Kritik: „hält auf“).
  Der Haken gehört auf offen mit Hindernis 7320 wie bei 7300. Der Koordinator lässt den
  Architekten das nachholen (`standregeln.hindernis`); der Architekt prüft nach 7320 neu.
  Gegenstück Item 1: „Architekt: Kritik an den Tests“ kann abgehakt werden, 7150 ist erledigt.
- Wartende Kriterien AUF-29, AUF-22, AUF-27, AUF-11, AUF-16.7, AUF-16.8, AUF-28, AUF-18.7,
  AUF-12.8, AUF-3.9, AUF-8.8, QUE-11, QUE-7: Sie stehen in Items außerhalb von Plan 9
  (anhaltenAufDemWeg, randfaelleDesAufstellens, gewinnerUndZone, loslassenNebenDerKarte,
  phaseBeendenNurImZug, ruhigeKarte). Der Testautor schreibt Tests nur zu Items des Plans
  ([Technikphase](../prozess/ablauf/technikphase.md) 1, [Kriterienregeln](../prozess/regeln/kriterienregeln.md));
  er muss heute nichts tun. Plan „Danach“ nennt anhaltenAufDemWeg, randfaelleDesAufstellens und
  gewinnerUndZone nicht: das ist die Lücke aus deinem Auftrag.
- Neues Anliegen 7380 (Auftrag, Von Stakeholder, An Organisationsentwickler, Wartet auf
  Prozessphase 9): „Notiere für die passende Rolle, dass wartende Anliegen für die nächste Phase
  auch eingeplant werden.“ Zuständig ist er, Autor des [Ablaufs](../prozess/ablauf/CLAUDE.md);
  der Planer plant danach. Deckt schon: [Domänenphase](../prozess/ablauf/domaenenphase.md) 4 und 6
  („Danach“ des Plans), [Kritik](../prozess/ablauf/kritik.md) (wartet auf die nächste Phase),
  [Anliegen](../prozess/ablauf/anliegenStatus.md) letzter Punkt; er passt sie an (Ich 4). Ich
  schreibe kein Anliegen: Der Koordinator beauftragt die Rolle, die es für dich stellt
  ([Status der Anliegen](../prozess/ablauf/anliegenStatus.md)); Nummer 7380 ist frei.
- Zusammen: 6981 und 6982 (Es 8, Docstrings); 6991, 6992, 6993 (Mutationslücken). 6400, 6410,
  6420 legen nur Entscheidungen ab; Items 3 und 4 setzen sie um, dann schließt du.
- Prozessphase 9 (wartet): 3960, 6432, 7030 (Regelumsetzer, höchstens einer mit Hook-Code),
  6471, 6500, 6960, 6987 (Organisationsentwickler), 6988, 7080. 7031 hängt an 7030.

Stränge Technikphase 9 (Dateien nach Anliegen, nicht per `git status` geprüft):
- Testautor, Kette 1: 7300, 7320 (`handgriffe.py` gemeinsam), dann Kette der Bewegungstests
  4901, 5241, 4921, 5781, 6340; daneben 6993 (Befehlstest). 6981 zuletzt, es berührt alle Tests.
- Implementierer: 5380 (Katalog) gleichzeitig mit 6991/6992 (`messen`, `web`) und 6122, 5701
  (Schlacht, vor Item 3); 6982 zuletzt, es berührt allen Code.
- Reviewer (6361) und Architekt (7023) schreiben nur Anliegen: gleichzeitig mit allem.

## Fragen an dich
Keine offene. 7023 F1 wartet auf die Erklärung des Architekten, danach antwortest du.
