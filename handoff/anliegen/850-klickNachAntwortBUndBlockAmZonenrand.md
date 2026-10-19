# Setzen per Klick nach Antwort B, Block am Zonenrand

850 · Kritik · von Fachkritiker → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.**
1. **AUF-18.1 folgt nicht der Antwort.** In [800](800-setzenPerKlickWelcheEinheitUndAuswahl.md)
   hat der Stakeholder auf F1 mit B geantwortet: Ein Klick *setzt* nur, wenn genau eine
   *Einheit* *ausgewählt* ist, sonst *Sperre*.
   [AUF-18.1](../../domaene/anforderungen/phasen/aufstellen/setzenPerKlick.md) steht noch auf A
   (die zuletzt *ausgewählte*, sonst die des anderen) und nennt keine *Sperre*. Für B sagen
   weder Antwort noch Regeln: (a) zählen die *Auswahlen* beider *Spieler* oder nur die des
   *Spielers* *an der Reihe*? (b) Sperrt Arbiter auch ohne *Auswahl*? Heute ändert sich dann
   nichts. (c) Welchen *Grund* nennt er? Zu F3 steht „Antwort: S“. Das ist keine der Optionen,
   *Ebene* steht aber schon im Glossar und in AUF-20 und 21.
2. **Am Zonenrand zerreißt der Block.** In der *Ebene* „Ganze Einheit“ *setzt* AUF-21.1 nur
   „jedes andere“ *Modell* um denselben Weg. Das gezogene *setzt* AUF-8.2 an die *Stelle* des
   Loslassens, und [AUF-3.7](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md)
   prüft es dort auch nach AUF-3.2. Zieht ein *Spieler* den Block über den Rand seiner
   *Aufstellungszone*, schiebt AUF-21.2 die anderen hinein, und das gezogene steht draußen,
   *gesperrt* mit ‚nicht ganz in der Zone‘. ArbiterMap, auf das sich AUF-21.2 beruft, kürzt
   den gemeinsamen Weg für jedes *Modell*, auch für das gegriffene
   (`ArbiterMap/docs/spec/interaction_map.md:381`, `:384`). Nach AUF-20.2 und 20.5 hat die
   *Einheit in Aufstellung* nach dem Klick die *Ebene* „Ganze Einheit“. Jedes Ziehen auf dem
   Happy Path ist also ein solcher Zug.

Einordnung nach Ich 3: beide halten auf. Zu 1: Das Setzen per Klick ist der erste Schritt des
Happy Path, und die *Sperre*, die die Antwort verlangt, fehlt. Zu 2: Die *Sperre* greift
dort, wo AUF-21.2 die *Modelle* hineinschieben will.

**Kosten.** Zu 1: Der Testautor schreibt Tests für AUF-18.1 in Fassung A, gegen die
Entscheidung des Stakeholders. Das Mockup [auf-22](../../domaene/mockups/auf-22.html) passt
zu beiden Fassungen. Zu 2: Wer seine *Einheit* an den Zonenrand schiebt, der häufigste Zug
beim Aufstellen, bekommt eine zerrissene *Formation* und eine *Sperre*, statt dass sie
anschlägt wie in ArbiterMap. Die Technik müsste sich zwischen zwei Kriterien entscheiden.

**Gegenvorschlag.**
1. AUF-18.1 neu fassen nach B. Die Fragen (a) bis (c) stellst du dem Stakeholder mit
   Empfehlung (Ich 1), etwa: (a) beide *Auswahlen*, wie die Antwort es wörtlich sagt, (b) ohne
   *Auswahl* ändert sich nichts wie bisher, (c) einen *Grund*, den er wählt. Die Antwort „S“
   lässt du ihn in derselben Datei bestätigen.
2. AUF-21.1 „jedes ihrer *gesetzten* *Modelle*“, also auch das gezogene. AUF-21.2 rückt alle
   gemeinsam hinein. AUF-3.7 bekommt den Zusatz „außer nach AUF-21.1“ oder AUF-21.3 ersetzt
   für diesen Zug die Prüfung nach AUF-3.7 (Ich 4: bestehendes Kriterium anpassen statt
   eines neuen).

Erledigt, wenn AUF-18.1 der Antwort folgt, die Fragen (a) bis (c) mit Annahme beim
Stakeholder liegen und nach AUF-21 kein *Modell* eines Blocks allein draußen gesperrt steht,
oder wenn du begründest, warum es anders sein soll.

**Stellungnahme.** Beides umgesetzt.
1. AUF-18.1 nach B mit deinen Empfehlungen (a) und (b), die *Sperre* als neues
   AUF-19.5 ‚mehrere ausgewählt‘. (a) bis (c) und „S“ stehen als F4 bis F7 in 800, Runde 2.
2. AUF-21.1 *setzt* statt nach AUF-8.2 jedes *gesetzte* *Modell* um denselben Weg, 21.2
   rückt alle gemeinsam hinein. AUF-3.7 (mit Tests) bleibt: Es prüft die *Stelle*, an die
   das *Modell* *gesetzt* wird, nun die gerückte.
