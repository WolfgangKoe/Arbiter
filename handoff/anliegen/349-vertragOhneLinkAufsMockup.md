# Vertrag ohne Link aufs Mockup

349 · Kritik · von Reviewer (Technik) → Architekt (Technik) · Runde 1/3 · erledigt

## Runde 1
**Befund.** [vertrag.md](../../technik/architektur/vertrag.md) V1 nennt
`spielstand.json` „der Stand des [Mockups](../../domaene/mockups/auf-5.html)“. Nach dem
Einbau löscht UX das Mockup ([348](348-mockupsNachDemEinbauLoeschen.md), Ablauf DoD); der
Link zeigt dann ins Leere.

**Kosten.** Ein toter Link im Vertrag, den Testautor und Implementierer zuerst lesen.
Eine Zeile.

**Gegenvorschlag.** Erledigt, wenn V1 den Stand von `spielstand.json` ohne Mockup beschreibt,
etwa über die Komponentenseite `technik/frontend/komponenten.html` oder die Kriterien
(AUF-5.6, AUF-5.7), und kein Link nach `domaene/mockups/` außer `vorschlag.css` in
`technik/architektur/` bleibt.

**Stellungnahme.** Angenommen und umgesetzt. V1 in `technik/architektur/vertrag.md` beschreibt
den Stand von `spielstand.json` jetzt selbst: wer *an der Reihe* ist, die *Einheit in
Aufstellung* mit ihren *gesetzten* *Modellen* und die *ausgewählten* *Einheiten*. In
`technik/architektur.md` und `technik/architektur/` gibt es keinen Link nach
`domaene/mockups/` mehr, nur noch den Pfad `vorschlag.css` in `web.md`.
