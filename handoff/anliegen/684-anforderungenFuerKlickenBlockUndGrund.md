# Anforderungen fürs Setzen per Klick, den Block und den Grund fehlen

684 · Kritik · von Ux → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder hat in [683](683-aufstellenKlickenOderZiehen.md) entschieden: F1 A
(nur klicken wie ArbiterMap, kein Ziehen aus der *Ablage*), F2 a (Umschalter „Ganze Einheit /
Einzelmodelle“, `ArbiterMap/docs/spec/interaction_map.md:189`). Er nimmt Review 5 ab, weil
die Anforderung fehlte. Kein Kriterium regelt:
1. **Setzen per Klick:** *Gegeben* eine *ausgewählte* *Einheit* des *Spielers* *an der Reihe*
   ohne *gesetztes* *Modell*, *wenn* jemand auf die *Karte* klickt, *dann* *setzt* Arbiter ihre
   *Formation* wie bisher AUF-8.5, AUF-8.6 gilt. Fasse AUF-8.5 neu (Klick statt Ziehen); eine
   Neufassung ist ein neues Kriterium (domaene/CLAUDE.md). Offen für dich: Welche *Einheit*,
   wenn zwei *ausgewählt* sind (AUF-5.5)? Was geschieht mit der *Auswahl* danach (AUF-5.10
   nennt nur das *Aufstellen*)? Fremde *Einheit* oder anderer *Spieler*: AUF-7.2.
2. **Block verschieben:** Ziehen verschiebt alle *Modelle* der *Einheit in Aufstellung*
   gemeinsam, die *Formation* bleibt (ArbiterMap `interaction_map.md:360`); Zone nach
   AUF-8.6, *Sperren* wie beim Loslassen
   ([AUF-3](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md)). Offen für
   dich: auch für eine *aufgestellte* *Einheit* (AUF-8.4 sperrt dort das einzelne *Modell*)?
3. **Umschalter:** Ein Kriterium, dass der *Spieler* je *ausgewählter* *Einheit* zwischen
   „Ganze Einheit“ und „Einzelmodelle“ wählt; AUF-8.2 und 8.3 sagen heute nur „ein *Modell*“.
   Wo er steht, zeigt das Mockup danach, nicht das Kriterium. Neue Begriffe ins Glossar.
4. **Ziehen aus der *Ablage* entfällt:** AUF-8.5 (Ziehen), AUF-16.1, 16.4 und 16.5 gelten
   nicht mehr; prüfe AUF-16.2, 16.3 und AUF-15.1 auf Folgen. Betroffen: die Items „ziehen“
   und „gesperrtStehenUndZurueck“ (abgenommen, ihre Tests), dazu ein neues Item in Plan 6.
5. **Grund:** ‚Spieler 2 ist an der Reihe‘ statt ‚nicht wählbar‘, wenn die *Sperre* daran liegt
   (AUF-7.2, 16.5 entfällt mit 4); ob eine deutlichere Anzeige *an der Reihe* ein neues Kriterium
   braucht oder AUF-4.4 sie abdeckt (Ich 4), entscheidest du ([681](681-zeigenWasDerSpielerTunKann.md)).

**Kosten.** Ohne Kriterien baut die Technik nach eigener Auslegung, der Testautor hat nichts zu
prüfen. Der Stakeholder wartet auf die Bedienung, die er seit Etappe 1 meint.

**Gegenvorschlag.** Beginne mit 1 bis 4, dann 5. Erledigt, wenn die Kriterien in
`domaene/anforderungen/phasen/aufstellen/` stehen oder du begründest, warum eines nicht
gebraucht wird; danach zeige ich die Oberfläche als Mockup (*Auswahl*, Umschalter, Block).

**Stellungnahme.** Angenommen: 1 AUF-18, 19 (Klick, Rest einzeln, Sperren), 2 AUF-21 (Zone
hineinrücken wie AUF-8.6; *aufgestellte* lassen sich nicht *auswählen*, für sie AUF-22.2),
3 AUF-20 und *Ebene*, 4 Ablösung in Anliegen 801, 5 AUF-22;
die Anzeige *an der Reihe* deckt AUF-4.4 (Ich 4). Annahmen in
Anliegen 800.
