# Kriterien für Plan 2: Ausgangslage und Sperren beim Setzen

94 · Kritik · von Planer (Domäne) → Anforderungsautor · Runde 1/3 · offen

## Runde 1
**Befund.** [AUF-1](../../domaene/anforderungen/phasen/aufstellen.md) ist gebaut und
abgenommen; zu [Etappe 1](../../domaene/etappen/01-aufstellen.md) gibt es kein Kriterium
ohne Test. [Plan 2](../plan.md) schneidet zwei Items, deren Kriterien fehlen:

1. [Ausgangslage von Only War](../../domaene/items/ausgangslage-only-war.md): die Armeen nach
   Etappe 1 (Stakeholder in Anliegen 09, F1 A, git), je einem *Spieler*: Boyz (10 *Modelle*)
   und Warboss gegen Necron Warriors (10 *Modelle*) und Overlord, jedes *Modell* mit runder
   Base; Durchmesser in `ArbiterMap/data/poc/units/` (`orks_boyz.yaml:21`,
   `orks_warboss.yaml:17`, `necrons_necron_warriors.yaml:15`, `necrons_overlord.yaml:17`, dort
   vom Stakeholder auf 32 mm festgelegt). Dazu *Spielfeld* und *Aufstellungszonen* aus
   [onlyWar.yaml](../../domaene/daten/onlyWar.yaml) als Flächen, an gegenüberliegenden langen
   *Spielfeldkanten*. Zu Beginn ist kein *Modell* *gesetzt*.
2. [Sperren beim Setzen](../../domaene/items/sperren-beim-setzen.md): *setzen* bringt ein
   *Modell* der *Einheit in Aufstellung* an eine *Stelle* auf dem *Spielfeld*. *Sperre* mit
   *Grund*, wenn seine Base nicht ganz in der eigenen *Aufstellungszone* liegt
   (`core_rules.txt:2322`, „wholly within“), eine andere Base überdeckt (Etappe 1, Anliegen 09
   F12 A) oder es in *Engagement Range* eines gegnerischen *Modells* ist (`:450`, 1″
   waagrecht `:447`); gemessen wird zwischen den nächsten Punkten der Bases (`:464`).

**Kosten.** Ohne Kriterien-IDs ist kein Item bereit (DoR 1), Plan 2 kann nicht freigegeben
werden, Zyklus 2 steht. Erfundene Kriterien im Item wären Umfang ohne Anforderung.

**Gegenvorschlag.** Je Item eine Anforderung, Bereich und Kürzel wählst du. Danach trägt der
Planer die Kriterien-IDs in die Items ein. Was nach dem Setzen geschieht (Ablage, Umsetzen,
Zurück, Übergehen, Protokoll, Sperren beim Beenden), bleibt außerhalb; Grenzen im Plan.
Fehlt dir dafür eine Entscheidung, frag den Stakeholder; welcher *Spieler* welche *Armee*
führt, ist aus meiner Sicht gleichgültig.

**Stellungnahme.**
