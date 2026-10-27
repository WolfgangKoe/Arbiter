# Anhalten am B: Stelle im Block und Quelle der Distanz

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wartet (Ich 3: Lücke abseits des Happy Path).
1. [BEW-3.1](../../domaene/anforderungen/phasen/bewegung/anhaltenAmB.md) prüft jedes gezogene
   *Modell* „an seiner *Stelle* nach AUF-8.2“. AUF-8.2 *setzt* aber nur das *Modell* unter dem
   Finger. Die anderen *Modelle* des Blocks bekommen ihre *Stelle* aus BEW-1.5 („um dieselbe
   Strecke“). Das zählt, wenn vorher ein *Modell* des Blocks allein gezogen wurde: Es
   erreicht sein *B* zuerst, und dann muss der ganze Block anhalten.
2. Im [Glossar](../../domaene/glossar.md) steht unter *Distanz* „5400 F1 A als Annahme“.
   [5400](5400-wieWeitEinKorrigiertesModellStehenDarf.md) ist beantwortet, es ist keine
   Annahme mehr.

**Kosten.** Ein Satzteil und zwei Wörter. Bis dahin lesen Testautor und Implementierer
BEW-3.1 nach dem [Vertrag](../../technik/architektur/vertrag/bewegung.md), V16 („jedes
*Modell* der *Ebene*“).

**Gegenvorschlag.**
1. BEW-3.1: „an der *Stelle*, an die BEW-1.5 es ohne BEW-3 *setzen* würde“.
2. Im Glossar „als Annahme“ streichen.

**Stellungnahme.** Punkt 2 ist umgesetzt (siehe [5560](5560-distanzEntschieden.md)). Punkt 1
stimmt in der Sache. Ich frage den Stakeholder, ob er jetzt in die Anforderung kommt oder
erst in Domänenphase 9.

Worum es am Bildschirm geht: Du ziehst erst einen Boy deiner *Einheit* allein 4″ vor (*B*
5″). Dann wählst du die ganze *Einheit* als *Ebene* und ziehst einen anderen Boy 3″ vor.
Alle Boyz rücken mit. Der vorgezogene Boy wäre dann 7″ von seiner *Stelle* zu Beginn der
*Bewegungsphase* entfernt. Darum hält Arbiter den ganzen Block nach 1″ an, denn jedes
*Modell* darf höchstens sein *B* ziehen (`core_rules.txt:745`). BEW-3.1 nennt bisher nur
den Boy unter deinem Finger. Der [Vertrag](../../technik/architektur/vertrag/bewegung.md)
V16 prüft schon jedes *Modell* der *Ebene*. Am Bildschirm ändert sich also nichts. Es geht
darum, ob ein Test das jetzt zeigt.

**F1 · Soll BEW-3.1 jetzt sagen, dass jedes Modell des Blocks den Block anhalten kann?**
A: ja, jetzt, bevor der Testautor BEW-3.1 schreibt (Gegenvorschlag 5541, Regeltext). Ich
ändere einen Satzteil in BEW-3.1, und der Testautor prüft den Fall oben mit. Neuer Code ist
nicht zu erwarten, weil V16 schon so rechnet.
B: erst in Domänenphase 9 (Ich 3). Bis dahin prüft kein Test, ob der vorgezogene Boy den
Block anhält. Ein Fehler darin bliebe bis zur Partie unbemerkt. In Phase 9 hat BEW-3.1
dann schon einen Test, also wird es durch ein neues Kriterium ersetzt und der Test neu
geschrieben.
Empfehlung: A. Das kostet jetzt einen Satzteil statt später ein Kriterium und einen Test
doppelt, und es prüft, was die Regel verlangt.
Antwort: .
Kommentar: Antwort auf F1: Für mich klingt das sinnig.
Stellungnahme: Nach F1 A umgesetzt. [BEW-3.1](../../domaene/anforderungen/phasen/bewegung/anhaltenAmB.md)
prüft jedes gezogene *Modell* „an der *Stelle*, an die BEW-1.5 es ohne BEW-3 *setzen*
würde“. Damit hält auch der vorgezogene Boy den Block an. Zu BEW-3.1 gab es noch keinen
Test, darum bleibt die Kennung. Punkt 2 ist erledigt (siehe 5560).
