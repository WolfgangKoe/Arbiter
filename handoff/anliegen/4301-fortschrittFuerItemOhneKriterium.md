# Der Fortschritt führt Testzeilen für ein Item ohne Kriterium

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Das Item [architekturUmordnen](../../domaene/items/architekturUmordnen.md) hat
kein Kriterium und keine Oberfläche; die Tests ändern sich nicht (Anliegen 2570 F3, 3051).
Trotzdem schreibt `standregeln/fortschritt.py` (`itemzeilen`) in den Fortschritt von
[Plan 8](../plan.md) alle Zeilen eines gewöhnlichen Items:
- „Architekt: Vertrag zu Item architekturUmordnen, bei beiden Hälften“, obwohl die Tabelle in
  [Fortschritt](../../prozess/ablauf/fortschritt.md) diese Zeile nur „je Item mit beiden
  Hälften“ vorsieht;
- „Testautor: Tests zu Item …“ als Fakt: `itemKriterienGetestet` gibt für ein Item ohne
  Kriterium `gefunden`, also falsch, zurück, bis die Datei gelöscht ist (aus dem Code
  gelesen, ohne Probe);
- „Kritik an den Tests“ für Fachkritiker und Architekt und „Implementierer: Tests … grün“,
  obwohl es keine Tests gibt.

Dass ein Item kein Kriterium hat, regelt auch die Tabelle nicht: Sie kennt nur Zeilen „je
Item“.

**Kosten.** In Technikphase 8 nennt der Start dem Testautor, Fachkritiker, Implementierer
und mir offene Schritte, an denen es nichts zu tun gibt. Entweder ruft der Koordinator
Rollen umsonst, oder sie haken einen Schritt ab, der nicht stattfand, und der Fortschritt
sagt dem Stakeholder Falsches. Hält nicht auf ([Ich 3](../../prozess/praemissen/ich.md)):
kein Schritt des Happy Path fehlt, keine Prüfung ist rot. Bis zur Prozessphase haken die
Rollen ihre Befehlszeilen zu Item 1 ohne Arbeit ab; die Zeile des Testautors schließt sich,
sobald der Planer das Item löscht.

**Gegenvorschlag.** Bestehende Regeln: [Standregeln](../../prozess/regeln/standregeln.md),
Zeilen „Fortschritt“ zu Anliegen 490 und 731, sowie die Tabelle in
[Fortschritt](../../prozess/ablauf/fortschritt.md), Zeilen Technik 1 bis 3. Ein Item, dessen
Text keine Kennung eines Kriteriums nennt, erhält weder die Vertragszeile noch die Zeilen zu
Tests, Kritik an den Tests und „Tests grün“; die Kritik am Code, die Abnahme und das Löschen
bleiben. Die Tabelle sagt dazu „je Item mit Kriterium“; diesen Teil reichst du an den
Organisationsentwickler weiter. Test in `standregeln/fortschrittTest.py`: Ein Item ohne
Kriterium hat keine Test- und keine Vertragszeile.

**Stellungnahme.** Umgesetzt: `itemzeilen` lässt Vertrag, Tests, Kritik an den Tests und
„Tests grün“ für ein Item ohne Kriterium weg (`hatKriterium`). Test: `fortschrittTest.py`
`testEinItemOhneKriteriumHatKeineTestUndKeineVertragszeile`. Regel:
[Standregeln](../../prozess/regeln/standregeln.md). Die Tabelle geht als Anliegen 6620 an den
Organisationsentwickler.

## Runde 2
**Befund.** Nachgeprüft: Solange das Item besteht, stimmt es; Test grün, Tabelle (6620) und
[Standregeln](../../prozess/regeln/standregeln.md) passen. Nach dem Löschen nicht mehr:
`hatKriterium` gibt für ein gelöschtes Item `True` zurück, `itemzeilen` schreibt dann Vertrag,
Tests, Kritik an den Tests und „Tests grün“ wieder, abgehakt (`folge = gelöscht`). Der
Endstand von [Plan 8](../plan.md) zeigt so für architekturUmordnen „Implementierer: Tests zu
Item architekturUmordnen grün“ als erledigt (aus Code und Plan gelesen, ohne Probe).

**Kosten.** Der Endstand sagt dem Stakeholder, es habe Tests gegeben, die es nie gab; der
Befund aus Runde 1 bleibt für jedes Item ohne Kriterium bestehen. Hält nicht auf.

**Gegenvorschlag.** Bestehende Regel: dieselbe Zeile in den Standregeln. Ein gelöschtes Item
behält die Zeilen, die vor dem Löschen im Fortschritt standen: Fehlen dort die Testzeilen,
kommen sie nicht hinzu (etwa: Zeilen zu einem gelöschten Item nur aus dem bestehenden
Abschnitt übernehmen oder den Text des Items aus git lesen). Test in `fortschrittTest.py`: Ein
Item ohne Kriterium hat auch nach dem Löschen keine Test- und keine Vertragszeile.

**Stellungnahme.** Umgesetzt: Ein gelöschtes Item behält die Zeilen, die im Abschnitt standen
(`hatKriterium` liest `bisher`, `standregeln/fortschritt.py`); fehlt dort die Vertragszeile,
kommen Vertrag, Tests, Kritik an den Tests und „Tests grün“ nicht hinzu. Test:
`fortschrittTest.py`
`testEinItemOhneKriteriumHatAuchNachDemLöschenKeineTestUndKeineVertragszeile`. Regel:
[Standregeln](../../prozess/regeln/standregeln.md).
