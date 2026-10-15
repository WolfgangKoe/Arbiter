# Jede Phase bringt das Produktziel voran

630 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Deine Anweisung: „Sorge dafür, dass der Fokus in jeder Phase darauf liegt, dass wir
mit dem Erreichen des Produktziels weiter kommen.“ Dein Bild und die Zahlen dazu:
[Anliegen 600](600-commitsSchneller.md), Runde 2. Die Ursachen, die ich sehe:
1. Jeder Befund wird ein Anliegen mit eigener Runde ([Ich 3](../../prozess/praemissen/ich.md)),
   auch Feinschliff, der nichts aufhält: wohin eine Hilfsfunktion der Tests gehört (480, 520,
   550, 580), ein Testname (411, 412). Der Reviewer schrieb sieben einzelne Anliegen an den
   Implementierer (396 bis 404).
2. Anliegen an eine Perspektive, deren Phase nicht läuft, sollen warten, außer sie halten das
   Inkrement auf ([Ablauf](../../prozess/ablauf.md#anliegen)). Der Stand nennt Regelumsetzer
   und mich aber in jeder Phase als dran (heute 421, 490, 600, 601), also liefen wir.
3. Stand und Dashboard zeigen Schritte und Anliegen, nicht, wie viel vom Produkt schon geht.
4. Die Probe, ob die Tests den gebauten Code prüfen, verlangt der Ablauf nicht.

**Kosten.** Keine der sieben Etappen ist erreicht; in Zyklus 5 entstand mehr Prüfcode als
Produktcode.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 3, [Kritik am
Code](../../prozess/ablauf.md#kritik-am-code), die Warteregel, der Abschnitt
[Fortschritt](../../prozess/ablauf.md#fortschritt), [Retro](../../prozess/ablauf.md#prozessphase).

**F1 · Ein Anliegen nur, wenn etwas aufhält?**
A: Ja, wenn das Item nicht weitergeht (Kriterium unklar, Test nicht schreibbar oder nicht grün
zu machen), eine Prüfung oder die DoD rot ist, Code gegen [Es](../../prozess/praemissen/es.md)
verstößt oder du fragst. Die Befunde eines Kritiklaufs an einen Autor stehen in einem
Anliegen. Übriger Feinschliff kommt in den [Backlog](../../prozess/backlog.md) der
Perspektive und wird erledigt, wenn die Datei ohnehin geändert wird. So lautet dann Ich 3.
B: Wie bisher.
Empfehlung: A. Die Qualität halten Prüfungen und Es; weg fällt nur, was nichts aufhält.
Antwort: A

**F2 · Prozessarbeit nur in der Prozessphase?**
A: Ja. Davor laufen Regelumsetzer und ich nur zu einem Anliegen, das das Produkt aufhält
(etwa eine Sperre zu Unrecht, Anliegen 650), oder wenn du es „sofort“ nennst; der Stand
nennt die übrigen „wartet auf die Prozessphase“. Die Retro beginnt mit dem Fortschritt des
Produkts und hat höchstens zwei Prozess-Items, je aus einem Befund, der das Produkt
aufgehalten hat.
B: Wie bisher.
Empfehlung: A. Jetzt hieße das: 601 und 650 laufen, weil Warten und Sperren jede Rolle
aufhalten; 490 (Teile 2 und 3) wartet auf die Prozessphase 5.
Antwort: A

**F3 · Wo siehst du den Fortschritt des Produkts?**
A: Die erste Zeile von Stand und Dashboard: erreichte Etappen von sieben und wie viele
Kriterien der laufenden Etappe ein grüner Akzeptanztest belegt; darunter die Schritte der
Phase (490, Teil 3).
B: Nur die Schritte der Phase im Dashboard (490, Teil 3).
C: Nichts Neues; was am Bildschirm geht, zeigt das Review.
Empfehlung: A, gebaut in der Prozessphase 5 als eines der zwei Items. So siehst du in jeder
Phase, ob das Produkt vorankommt, ohne eine Datei zu öffnen.
Antwort: A

**F4 · Prüft der Reviewer in jedem Zyklus, ob die Tests den Code treffen?**
A: Ja, wie in Review 5: Er baut in einer Kopie Fehler einzeln in den neuen Produktcode ein
und nennt, wie viele Tests rot wurden; jede Lücke wird ein Anliegen an den Testautor.
Mechanismus: nur Text.
B: Ein Werkzeug (mutmut) tut es bei der DoD, der Regelumsetzer baut es.
Empfehlung: A. Review 5 zeigt, dass es geht und Lücken findet; B erst, wenn die Probe den
Reviewer über 120.000 Token Belegung bringt.
Antwort: A

Nach deinen Antworten ändere ich Ablauf, Ich 3 (nach F1 A) und Kennzahlen.

**Stellungnahme.**
Kommentar: Bitte vormerken, dass wir rechtzeitig mit Testmutations arbeiten, um Lüücken im Test bzw. Fehler im Codezu finden.
Stellungnahme: Im Backlog vorgemerkt (Retro 5).
