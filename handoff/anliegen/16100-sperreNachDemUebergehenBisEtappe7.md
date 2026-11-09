# Fliegen: Sperre nach dem Übergehen ohne Test bis Etappe 7

Form: Fragen
Von: Planer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Aus [13580](13580-planFliegenRest.md) und dem Mutationslauf von Zyklus 10 (Anliegen
15462). Wählen die *Spieler* für die Canoptek-Spinne *gemeinsam übergehen* und steht sie danach
auf einer fremden *Base*, rückt Arbiter sie an die nächste freie *Stelle*
([BEW-18.7](../../domaene/anforderungen/phasen/bewegung/fliegen.md)). Findet er keine, sperrt er
mit ‚Base überdeckt‘, und die Spinne bleibt, wo Arbiter sie angehalten hatte
([schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py), Zeile 149).
Das verlangt [BEW-18.6](../../domaene/anforderungen/phasen/bewegung/fliegen.md), aber erst
für Etappe 7. Heute erreicht kein Spiel diese Zeile: Frei ist immer zumindest die *Stelle*,
an der die Spinne vor dem Ziehen stand (Anliegen 13020). Keinen Platz gibt es erst, wenn sie
schon auf einer fremden *Base* aufgestellt werden kann (AUF-27.1, Etappe 7). Darum prüft kein
Test die Zeile; der Mutationslauf fand, dass ohne sie alle Tests grün bleiben.
Am Bildschirm ändert sich bis Etappe 7 nichts, gleich wie Sie entscheiden.

**Kosten.** A: nichts; die Quote des Laufs liegt mit ihr bei rund 99,7 %, Schwelle 95 %
([DoD](../../prozess/ablauf/dod.md)); eine Zeile bleibt bis Etappe 7 ohne Test. B: der
Implementierer streicht zwei Zeilen, in Etappe 7 kommen sie mit dem Test zurück. C: zwei
Anforderungen (BEW-18.6, AUF-27.1) mit ihren Tests und ihrem Code jetzt; mindestens ein
Item mehr, Etappe 2 endet nicht mit Zyklus 10.

**Gegenvorschlag.**
**F1 · Was geschieht bis Etappe 7 mit der Sperre nach dem Übergehen?**
A: Sie bleibt ohne Test; mit Etappe 7 verlangt die Prüfung der Rückverfolgung einen Test zu BEW-18.6, der sie dann prüft (Anliegen 13020, 13150).
B: Sie entfällt bis Etappe 7: Im Code steht nur, was ein Test prüft (Absicht 1, Anliegen 13020).
C: BEW-18.6 und AUF-27.1 kommen jetzt, mit Tests (Anliegen 13020).
Empfehlung: A, die Sperre hält, was das Ziel verlangt: Überdeckte *Bases* lassen sich nie übergehen. Mit B stünde die Spinne ohne Sperre auf einer fremden *Base*, sollte es doch einen Fall geben, den wir übersehen haben. C zieht Randfälle des Aufstellens vor die Phasen, gegen „erst die wesentlichen Funktionen entlang der Phasen“ (Absicht 3).
Annahme: Bis zu Ihrer Antwort bleibt alles, wie es ist (A).
Antwort: Den Fall, dass eine Base überdeckt sein kann, sollte es gar nicht geben. Eine Base sollte auch nach dem "übergehen" nicht überdeckt werden können. Hier ist ein Fehler in den Anforderungen.

**Stellungnahme.**
Kommentar: Als ich gerade in die Anforderungen geschaut habe, stellte ich mit etwas Schrecken fest, dass viele Anforderungen sich auf andere ANforderungen beziehen. Das ist an sich nicht verkehrt. Wenn ich, als Mensch (!!!), erst fünf verschiedene Anforderungen gelesen haben muss und dann einen Knoten im Hirn habe und BEW-18.7 immer noch nicht verstehe, dann läuft hier etwas grundsätzlich falsch. Gib dem Anforderungsautor mit, dass Akzeptanzkriterien für einen Menschen verständlich notiert werden müssen. Bezug auf andere Akzeptanzkriterien ist durch Verweise wie BEW-6.4 erlaubt, aber nur in Klammer: Gegeben: Ein Modell wird ausgewählt (xxx-5.8) Wenn: .... (yyy-1.2) usw. Verstehst du, was ich meine? Die Verweise sollen helfen, sich zu orientieren, sie sind kein Ersatz für Sätze, die ein Mensch lesen und verstehen kann.

**Klärung.** Ihre Antwort ersetzt A bis C: Eine *Base* überdeckt nie eine andere, auch nicht
nach dem Übergehen. Der Fehler steht in AUF-27: Dort stellt Arbiter eine *Formation*, die
nirgends passt, trotzdem auf, und *Bases* überdecken sich; nur so wird die *Sperre* nach dem
Übergehen überhaupt erreichbar. AUF-27 geht auf Ihre Antwort C in Anliegen 992 zurück, Sie
entscheiden jetzt also anders als damals. Der Anforderungsautor berichtigt AUF-27 und richtet
BEW-18.6 und BEW-21 danach aus ([16150](16150-basesNieUeberdeckt.md), Domänenphase 11); was
Arbiter stattdessen tut, wenn eine *Formation* nicht passt, fragt er Sie dort mit Empfehlung.
Bis dahin bleibt der Code, wie er ist; am Bildschirm ändert sich bis Etappe 7 nichts. Ihr
Kommentar zur Lesbarkeit der Anforderungen geht an den Organisationsentwickler.
