# Zeigt die Ablage den Durchmesser jedes Modells?

239 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Die Mockups von Plan 3 ([Ausgangslage](../../domaene/mockups/auf-4-ausgangslage.html),
[Spieler 1 an der Reihe](../../domaene/mockups/auf-4.html)) zeigen in der Ablage jedes noch
nicht gesetzte Modell als Eintrag „32 mm“, beim Warboss „40 mm“. Keine Anforderung verlangt
diese Zahl; AUF-4.3 sagt nur, dass die Ablage die Modelle zeigt. Die Regeln sagen dazu nichts,
eine Entscheidung von dir gibt es nicht (Anliegen 237 des Architekten). Ohne Kriterium prüft
kein Test, ob dort die richtige Zahl in der richtigen Einheit steht.

**Kosten.** A: ein Kriterium und ein Test mehr in Plan 3. B: UX ändert die zwei Mockups.
Später, wenn du Modelle aus der Ablage auf die Karte ziehst und Einheiten verschiedene Bases
haben, ist die Zahl der Anhalt, welches Modell du greifst.

**F1 · Soll die Ablage jedes Modell mit dem Durchmesser seiner Base zeigen?**
- A: Ja, in mm, wie im Mockup. Neues Kriterium AUF-4.8: „Die *Ablage* nennt jedes nicht
  *gesetzte* *Modell* mit dem *Durchmesser* seiner *Base* in mm.“
- B: Nein. Jedes Modell ist ein Eintrag ohne Text; UX passt die Mockups an.

Empfehlung: A. Die Mockups zeigen es schon, es kostet einen Test, und bei gemischten Bases
unterscheidet man die Modelle daran.

Antwort: Es ist dir aufgefallen. Ich habe es wohl schon irgendwo geschrieben. Ich wähle hier B. Denn die einheitenKarte wird später aus Arbiter-old im wesentlichen übernommen. Lass es uns hier einfacher halten.

**Stellungnahme (Stakeholder)**
In Mockup "auf-4-ausgangslage.html" sind Badges, welche den Basedurchmesser aller Modelle in der Einheit anzeigen und zwar so viele Modelle in der Einheit sind. Rückfrage: Sind das Platzhalter oder soll das aus deiner Sicht so bleiben. Die einheitenKarte wird voraussichtlich noch gesondert gebaut. Halte diese daher sehr einfach. Eine einfache Badge mit <anzahlDerModelle> z.B. 10 würde völlig reichen. Es sei denn du widersprichst mir hier.
