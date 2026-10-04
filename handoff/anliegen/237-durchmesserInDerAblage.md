# Ablage zeigt den Durchmesser, kein Kriterium verlangt ihn

237 · Kritik · von Architekt (Technik) → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Mockups [Ausgangslage](../../domaene/mockups/auf-4-ausgangslage.html) und
[Spieler 1 an der Reihe](../../domaene/mockups/auf-4.html) zeigen jedes nicht *gesetzte*
*Modell* der *Ablage* mit dem *Durchmesser* seiner *Base*: „32 mm“, beim Warboss „40 mm“.
AUF-4.3 verlangt nur, dass die *Ablage* die *Modelle* zeigt, nicht womit. Der Testautor prüft
also die Zahl der Einträge je *Einheit*; welcher Text darin steht, prüft kein Test. Der
Implementierer übernimmt das Markup und setzt den Wert aus den Daten ein (Anliegen 151).
Dieselbe Lage hatte 223 Befund 3: sichtbares Verhalten ohne Kriterium seines Items.

**Kosten.** Heute eine Zeile im Frontend ohne Test: Zeigt sie Zoll statt mm oder den
*Durchmesser* eines anderen *Modells*, bleibt alles grün, auch die Rückverfolgung. Mit
gemischten *Einheiten* und dem Ziehen aus der *Ablage* (Etappe 1, „Danach“ in
[Plan 3](../plan.md)) wird der Wert der Anhalt, welches *Modell* der Spieler greift; dann
fehlt das Kriterium an einer Stelle, auf die sich Spieler verlassen.

**Gegenvorschlag.** Ein neues Kriterium, AUF-4.3 bleibt wie es ist (Kennungen, domaene/CLAUDE.md):
- A: AUF-4.8 „Die *Ablage* nennt jedes *Modell* mit dem *Durchmesser* seiner *Base* in mm.“
  Ins Item Anzeige der Aufstellung, ein Test mehr.
- B: Kein Kriterium; UX zeigt jedes *Modell* als Eintrag ohne Text.

Empfehlung: A, die Mockups zeigen es schon, und es kostet nur einen Test. Ob der Stakeholder
den Wert sehen will, fragst du ihn, falls es keine Entscheidung dazu gibt.

**Stellungnahme.** Befund geteilt: Regeln und Ziel sagen nichts dazu, eine Entscheidung des
Stakeholders gibt es nicht (gesucht in 145, 199, `Arbiter-old/`, `ArbiterMap/`). Nach meiner
Rolle bleibt das Kriterium draußen, bis er antwortet; die Frage steht mit A als Empfehlung
und dem Wortlaut von AUF-4.8 in [239](239-durchmesserInDerAblageZeigen.md). Nach der Antwort
schreibe ich AUF-4.8 nach [AUF-4](../../domaene/anforderungen/phasen/aufstellen.md) (bei A)
oder bitte UX um die Mockups ohne Text (bei B).
Umgesetzt nach 239 F1 B: kein Durchmesser, kein AUF-4.8. Der Stakeholder will je *Einheit*
eine Zahl; UX hat beide Mockups so geändert. Damit auch diese Zahl ein Kriterium hat, verlangt
AUF-4.3 jetzt die Anzahl der nicht *gesetzten* *Modelle* je *Einheit*, keine Zahl, wenn alle
*gesetzt* sind. Kein Test hängt an AUF-4.3, die Kennung bleibt, Item 2 bleibt unverändert.
