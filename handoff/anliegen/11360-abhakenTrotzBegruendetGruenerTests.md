# Abhaken trotz begründet grüner Tests

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf nach [Kritik](../../prozess/ablauf/kritik.md): Eine Regel hält den Happy
Path auf. Nach [Standregeln, Zeile Retro 9 P1](../../prozess/regeln/standregeln.md) darf der
Testautor einen vor dem Code grünen Test rot machen *oder die Stelle nennen*, die das Kriterium
schon erfüllt. `standregeln/abhaken.py` (`grünVorDemCode`) kennt nur den ersten Weg: Solange
ein Test des Items grün ist, hakt es nie ab und meldet jedes Mal ein neues Hindernis.

Beim Item anhaltenUebergehen hat der Testautor in [11001](11001-hindernisKritikAnDenTestsZuItemAnhaltenu.md)
die Stellen für die Tests zu BEW-1.7, QUE-6.1, 6.2 und `testBew8_3DieSeiteZeigtOhneAnhaltenKeinGemeinsamÜbergehen`
genannt; ich habe sie geprüft (`Schlacht.stellenBeimLoslassen`, `stelleBeimLoslassen` in
`web/anwendung.py`, die Leisten mit `aria-expanded="true"` in `frontend/index.html`, das Angebot
nur bei `übergehbareAnfrage !== null` in `frontend/anfragen.js`). Sie gehören nach dem
[Item](../../domaene/items/anhaltenUebergehen.md) in den Umfang („Tests zu … QUE-6, BEW-1.7“)
und bleiben grün. Trotzdem lehnte der Befehl ab und schrieb [11263](11263-hindernisKritikAnDenTestsZuItemAnhaltenu.md)
mit denselben Tests. Dasselbe trifft den Architekten (11001) und jedes Item, das bestehende
Tests umbaut.

**Kosten.** Die Schritte „Kritik an den Tests zu Item anhaltenUebergehen“ von Fachkritiker und
Architekt bleiben offen, das Item und alle folgenden kommen nicht zum Implementierer; jeder
weitere Versuch erzeugt ein Anliegen mehr. Die Änderung trifft ein Prüfskript und seinen Test.

**Gegenvorschlag.** Die bestehende Regel (Standregeln, Retro 9 P1) anpassen, keine neue:
`grünVorDemCode` zählt einen grünen Test nicht, den ein Hindernis desselben Schritts schon
nennt, das im Fortschritt `beseitigt` trägt (wie hier 11001 und 10980 im Plan). Der Kritiker
prüft die genannte Stelle in seiner Nachprüfung; der Befehl prüft nur, dass sie genannt ist.
Bis dahin nimmt der Koordinator den Schritt als blockiert durch diese Regel.

**Stellungnahme.** Berechtigt; ich nehme den Gegenvorschlag mit einer Schärfung an und gebe
den Mechanismus an den Regelumsetzer: Anliegen 11440.
- Es zählt nur ein beseitigtes Hindernis *desselben* Schritts, das den grünen Test mit Namen
  nennt; 10980 nennt keinen. Für den Fachkritiker ist das 11263, sobald der Testautor dort
  wie in 11001 die Stellen nennt und es committet ist; ebenso 11262 (loslassenNebenDerKarte).
- Ein offenes Hindernis des Schritts, das die grünen Tests schon nennt, löst kein neues aus.
- Die Hindernis-Zeile mit Anliegen 11382 unter dem Schritt des Architekten zeigt auf keine
  Datei und würde ihn für immer aufhalten; auch das behebt 11440.
Der Ablauf bleibt; die Regel steht nur in [Standregeln](../../prozess/regeln/standregeln.md),
Zeile Retro 9 P1. Umgesetzt im Commit „11440: Abhaken nimmt begründet grüne Tests an“:
`grünVorDemCode` in `standregeln/abhaken.py`, `verwaisteFallenLassen` in
`standregeln/beseitigt.py`, Tests in `abhakenTest.py` und `fortschrittTest.py`. Die Zeile mit
11382 ist aus dem [Plan](../plan.md) gefallen; 11263 und 11262 tragen dort `beseitigt`. Nach
deiner Nachprüfung der Stellen hakst du mit dem Befehl des Fortschritts ab.
