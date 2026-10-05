# Push nur nach dev, einmal je Zyklus

273 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Entscheidung des Stakeholders im Chat: „Wir sollten hier auf dev bleiben. Am Ende
eines vollen Zyklus pushen wir einmal nach dev.“ Die Regel steht in
[koordinator.md](../../.claude/agents/koordinator.md), den Zeitpunkt nennt
[Ablauf, Prozessphase 6](../../prozess/ablauf.md#prozessphase). Heute:
1. Der lokale Branch heißt `main` und folgt `origin/main`; `origin/dev` und `origin/main`
   stehen auf 97ce17d. Ein bloßes `git push` ginge nach `main`.
2. `rollenregeln/bashPositivliste.py` erlaubt dem Koordinator `git push` mit jedem Ziel und
   jeder Option, aber weder `git switch` noch `git branch`: Den Branch wechselt er nicht.
3. Der Koordinator liest `ablauf.md` nicht (Lesegrenze 4.000 Zeichen); das Zyklusende sieht
   er nur, wenn der Stand es nennt.

**Kosten.** Ein Push nach `main` oder mitten im Zyklus widerspricht der Entscheidung; ein
vergessener Push lässt den Zyklus nur lokal.

**Gegenvorschlag.** Erledigt, wenn, je mit Scheiter-Test:
1. `bashPositivliste.py` lässt `git push` nur als `git push origin dev` oder
   `git push origin HEAD:dev` zu, ohne `--force`, `--delete`, `--all`, `--mirror`, `--tags`.
2. Der Stand nennt „Push nach dev“ als nächsten Schritt, wenn nach `Freigabe Retro <n>` jedes
   Prozess-Item seinen Commit `P<k>:` hat und `HEAD` Commits enthält, die `origin/dev`
   (letzter bekannter Stand, ohne Fetch) nicht hat.
3. Heißt der lokale Branch nicht `dev`, meldet der Stand das mit dem Befehl, den der
   Stakeholder selbst ausführt: `git branch -m main dev && git branch -u origin/dev`.
Den Push außerhalb des Zyklusendes sperre ich nicht: Der Stand nennt den Zeitpunkt, eine
Sperre daran hinge an derselben Herleitung. Danach ersetze ich „nur Text“ in Prozessphase 6.

**Stellungnahme.**
