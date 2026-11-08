# Übergehen und Leisten: noch in Technikphase 10 oder als Plan 11?

Form: Fragen
Von: Reviewer
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Du nimmst zwei Items nicht ab ([Review 10](../review.md)):
1. *Leisten*: Fahrt ihr eine *Leiste* ein, rückt das *Spielfeld* zur Seite. Am laufenden
   Arbiter nachgesehen: Die linke *Leiste* eingefahren, das *Spielfeld* rückt um gut 100 Pixel
   nach links. Das Gebaute tut, was [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigesSpielfeld.md)
   verlangt; es nimmt den *Griff* aus. Wie es werden soll, hast du schon entschieden (14462,
   A: die *Leisten* liegen über dem *Spielfeld* wie in ArbiterMap); das Kriterium dazu wartet
   in [15100](15100-griffVerschiebtDieKarteNicht.md) auf die Domänenphase 11.
2. *Gemeinsam übergehen*: Heute *setzt* der Knopf die *Modelle* an den Punkt des Loslassens
   ([BEW-8.4](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md)); zieht ihr
   sie danach weiter, halten sie wieder an. Du willst: Nach dem Knopf folgen die *Einheit* oder
   einzelne *Modelle* dem Zeiger, wie beim Ziehen in der *Aufstellung*. Das ist ein neues
   Kriterium ([15461](15461-uebergehenDannFolgtDemZeiger.md)).

Beides ist mehr als eine Korrektur am Code: Erst ändert sich die Anforderung, dann Vertrag,
Tests und Code. Die Reihenfolge ist in beiden Wegen dieselbe:
Anforderungsautor (Kriterium, Glossar) → Fachkritiker → Architekt (Vertrag, [O4](../../technik/architektur/frontend.md))
→ Testautor (rot) → Implementierer und Frontend-Implementierer (grün) → Reviewer, Fachkritiker → Review.
Ein Mockup braucht es nicht: Vorbild sind ArbiterMap und das Ziehen in der *Aufstellung*.

Warum bei dir: Ob ihr dafür vom Ablauf abweicht, ist eine Ausnahme, und die erteilst nur du
([Absicht 6](../../prozess/praemissen/absicht.md)). Bis zu deiner Antwort beginnt niemand.

**Kosten.** Gleich in beiden Wegen: etwa so viel wie ein Item mit beiden Hälften, je Thema.
Anders ist, wann es am Bildschirm ist und was am Ablauf vorbeigeht (siehe F1).

**Gegenvorschlag.** Siehe Empfehlung.

**F1 · Wann sollen Leisten und Übergehen geändert werden?**
Annahme: Ich schreibe Review 10 mit B: Etappe 2 ist nicht erreicht, beide Themen sind das Zyklusziel für Plan 11.
A: Noch in Technikphase 10. Der Planer hängt Plan 10 zwei Items an, du gibst sie frei, dann die Kette oben; danach schreibe ich Review 10 neu, mit Etappe 2 erreicht. Für einen Plan, der in der Technikphase wächst, haben Fortschritt und Stand keinen Weg; nicht erprobt (Kommentar zu Review 10).
B: Als Plan 11, im Ablauf: Du gibst Review 10 frei mit „Etappe 2 nicht erreicht“; nach der Prozessphase 10 schreibt der Anforderungsautor 15100 und 15461 in der Domänenphase 11, Plan 11 enthält beide Items und schließt Etappe 2 ab (Technikphase).
Empfehlung: B, gleicher Aufwand, alle Prüfungen und die Kritik am Plan laufen wie immer; A ist nur um die Prozessphase 10 früher am Bildschirm und verlangt eine Ausnahme vom Ablauf.
Antwort: B

**Stellungnahme.**
Kommentar: Ich folge deiner Empfehlung. Es ist allerdings wieder vorgekommen, dass in Teilen etwas falsches gebaut wurde. Vielleicht fällt es mir doch immer etwas schwer, die Details aus den Texten richtig zu verstehen und gehe davon aus, dass es sich verhält, wie etwas anderes, das schon gebaut ist. So wie hier das Verhalten der Aufstellung in Teilen nachempfunden werden soll. Wie auch immer, machen wir es erstmal so.
