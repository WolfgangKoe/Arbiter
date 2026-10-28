# Voller Mutationslauf: früher starten, Fortschritt zeigen

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Dein Wortlaut: „Der Mutationstest muss früher starten. Mir scheint es so, dass er
mal unterbrochen wurde.“ Unterbrochen wurde er nicht: Nach `Freigabe Review 8` (19:24) startete
der Koordinator den vollen Lauf um 19:32; um 22:18 lief er laut `ps` seit 2:46 h ohne Pause, je
Mutant ein Testlauf samt Bildschirmtests. Es sieht nach einem Abbruch aus, weil das Werkzeug
erst am Ende schreibt: `/tmp/mutationVoll8.log` bleibt bis dahin leer. Die normale Dauer ist
unbelegt; frühere volle Läufe haben kein Protokoll hinterlassen. Die letzte Änderung am Produkt
in Zyklus 8 war der Commit „DoD über das Inkrement erfüllt, Review 8 nachgebessert“ um 17:58.
Bestehende Regel: [Prozessphase](../../prozess/ablauf/prozessphase.md) Punkt 1 („Mit Beginn der
Phase startet der Koordinator den vollen Mutationslauf“) und [DoD](../../prozess/ablauf/dod.md)
(„läuft nur in der Prozessphase und hält nichts auf“), beide nur Text.

**Kosten.** Am Bildschirm: nichts. Deine Arbeit: Das Ergebnis kommt früher, du wartest kürzer.
Unsere Arbeit: Der Lauf rechnet, während Reviewer und Fachkritiker ihre Tests laufen lassen;
die werden langsamer. Ändert sich `technik/` danach, gilt das Ergebnis nicht mehr und der Lauf
startet neu. Er liest die Module unterwegs aus dem Projektordner, ein Ergebnis über eine
Änderung hinweg wäre gemischt. Token: keine, der Lauf rechnet ohne Agent.

**Gegenvorschlag.** Der Koordinator startet den vollen Lauf, sobald der Reviewer die DoD über
das Inkrement erfüllt meldet ([Technikphase](../../prozess/ablauf/technikphase.md) Schritt 4);
der Satz zieht aus Prozessphase und DoD dorthin. Der Reviewer schreibt die Lücken weiter in der
Prozessphase als Anliegen. Dazu schreibt der Lauf je Modul eine Zeile, sobald es fertig ist.

**Stellungnahme.**

**F1 · Wann startet der volle Lauf?**
A: Nach der DoD über das Inkrement (Technikphase Schritt 4); ändert sich `technik/` danach,
startet der Koordinator ihn neu (neu, Grund: [Absicht 2](../../prozess/praemissen/absicht.md),
„Arbeitet parallel, wo nichts voneinander abhängt“). In Zyklus 8 wäre das 17:58 gewesen statt
19:32. Nachteil: parallele Tests langsamer, Neustart bei späten Änderungen am Produkt.
B: Mit dem Commit `Freigabe Review <n>`, ohne auf die Retro zu warten (Prozessphase 1). Gewinn
in Zyklus 8: 8 Minuten. Nichts läuft parallel, kein Neustart.
Empfehlung: A. Nach der DoD ändert sich das Produkt selten, der Lauf hat dann Stunden Vorsprung.
Antwort: .

**F2 · Soll der Lauf unterwegs zeigen, wie weit er ist?**
A: Ja, je fertigem Modul eine Zeile ins Protokoll: Modul, Zahl der Mutanten, Überlebende (neu,
Grund: [Absicht 5](../../prozess/praemissen/absicht.md), verstehen ohne nachzufragen). Arbeit:
Regelumsetzer, einige Zeilen in `mutationsregeln/mutation.py` mit Scheiter-Test. Nachteil: mehr
Prüfcode, der in [Retro 8](../retro.md) Befund 3 schon über der Schwelle liegt; darum nur auf
deinen Wunsch. Rückweg: die Zeile wieder streichen. Nicht an einer Kopie erprobt; das tut der
Regelumsetzer mit seinem Scheiter-Test.
B: Nein, wie bisher: Das Protokoll füllt sich erst am Ende (`mutation.py`); fragst du nach,
nennt der Koordinator die Laufzeit aus `ps`.
Empfehlung: A. Ein leeres Protokoll sieht wie ein Abbruch aus, das hat dich hier getäuscht.
Antwort: .

**F3 · Ab wann gilt die Änderung?**
A: Jetzt: `Freigabe Retro 8` ist erteilt, also darf ich Prozessregeln in dieser Prozessphase
ändern (Prozessphase, Auslöser). Ich trage sie in der Nachkorrektur als Auftrag in Retro 8 ein;
sie wirkt ab Technikphase 9.
B: Erst in Prozessphase 9 über den [Backlog](../../prozess/backlog.md) (Prozessphase 1); sie
wirkt dann ab Technikphase 10.
Empfehlung: A. Sonst wartest du auch im nächsten Zyklus drei Stunden.
Antwort: .
