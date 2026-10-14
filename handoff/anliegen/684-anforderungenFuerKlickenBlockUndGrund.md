# Anforderungen fürs Setzen per Klick, den Block und den Grund fehlen

684 · Kritik · von Ux → Anforderungsautor · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder erwartet beim Aufstellen eine andere Bedienung
([683](683-aufstellenKlickenOderZiehen.md), Antwort steht aus) und die Seite nennt keinen
*Grund*, der den *Spieler* *an der Reihe* zeigt ([681](681-zeigenWasDerSpielerTunKann.md),
Punkt 3). Kein Kriterium regelt das. Was fehlt, je nach seiner Antwort; beginne erst damit,
sonst schreibst du Kriterien für eine Bedienung, die er nicht will:
1. Bei A oder B, **Setzen per Klick:** *Gegeben* eine *ausgewählte* *Einheit* des *Spielers*
   *an der Reihe* in einer *Ablage* ohne *gesetztes* *Modell*, *wenn* jemand auf die *Karte*
   klickt, *dann* *setzt* Arbiter ihre *Formation* wie AUF-8.5, AUF-8.6 gilt. Dein Vorbild ist
   AUF-8.5 mit dem Klick als Auslöser (Ich 4). Offen für dich, nicht erfunden von mir: Welche
   *Einheit*, wenn zwei *ausgewählt* sind (AUF-5.5)? Was geschieht mit der *Auswahl* danach
   (AUF-5.10 nennt nur das *Aufstellen*)? Ein Klick einer *Einheit* des anderen *Spielers*:
   AUF-7.2 deckt es mit ‚nicht wählbar‘ ab.
2. Bei A, B oder C, **Block verschieben:** Ziehen verschiebt alle *Modelle* der *Einheit in
   Aufstellung* gemeinsam, die *Formation* bleibt; Zone nach AUF-8.6, *Sperren* wie beim
   Loslassen ([AUF-3](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md)).
   Fundstelle: ArbiterMap `interaction_map.md:360`, Plan 5 („Komfort“). Offen für dich: Gilt es
   auch für eine *aufgestellte* *Einheit* (AUF-8.4 sperrt dort schon das einzelne *Modell*)?
3. Nach F2 in 683: Wie der *Spieler* zwischen Block und *Modell* wählt (ArbiterMap
   `interaction_map.md:189`, Umschalter); AUF-8.2 und AUF-8.3 sagen heute nur „ein *Modell*“.
4. Bei A: AUF-8.5 neu fassen, AUF-16.1, 16.4, 16.5 prüfen (kein Ziehen der Karte mehr). Bei C:
   ein Kriterium für den Hinweis zum Ziehen; den Wortlaut der Seite lege ich nicht fest.
5. Unabhängig von 683, jetzt: ein *Grund* ‚Spieler 2 ist an der Reihe‘ statt ‚nicht wählbar‘,
   wenn die *Sperre* daran liegt (AUF-7.2, AUF-16.5); ob eine deutlichere Anzeige *an der
   Reihe* ein neues Kriterium braucht oder AUF-4.4 sie abdeckt (Ich 4), entscheidest du.

**Kosten.** Ohne Kriterien baut die Technik nach eigener Auslegung, und der Testautor hat nichts,
woran er prüft. Der Stakeholder blieb vor dem ersten Schritt von
[Review 5](../review.md) stehen; jede weitere Phase (Bewegen, Schießen) hat dieselben Fragen
„wer ist dran, wie greife ich“.

**Gegenvorschlag.** Punkt 5 jetzt; 1 bis 4 erst nach seiner Antwort in 683, davon nur das, was die
gewählte Option verlangt. Kein Kriterium löst eine Antwort aus, die er nicht gegeben hat (Ich
1). Erledigt, wenn die Kriterien in `domaene/anforderungen/phasen/aufstellen/` stehen oder du
begründest, warum eines nicht gebraucht wird; danach zeige ich die Oberfläche als Mockup.

**Stellungnahme.**
