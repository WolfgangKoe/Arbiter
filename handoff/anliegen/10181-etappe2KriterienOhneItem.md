# Etappe 2: Kriterien ohne Item, Ork-Psioniker im Item Fliegen

Form: Kritik
Von: Fachkritiker
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an [Plan 10](../plan.md), Abschnitt „Danach (Plan 11, schließt Etappe 2)“,
und an den Items. Nichts hält Plan 10 auf. Die Punkte betreffen nur Plan 11, und der Happy
Path von Plan 10 läuft ohne sie ([Kritik](../../prozess/ablauf/kritik.md)).
1. [BEW-9.2](../../domaene/anforderungen/phasen/bewegung/abwaehlen.md) (Etappe 2, ohne Test)
   steht in keinem Item, weder in Plan 10 noch in Plan 11.
2. Plan 11 nennt in Item 1 den Ork-Psioniker,
   [fliegen.md](../../domaene/items/fliegen.md) im Umfang aber nur die Canoptek-Spinne. Der
   Weirdboy hat kein FLY (`Arbiter-old/data/wh40k_9e/orks/units.yaml:254`). Er gehört also in
   die *Armee*, nicht zum *Fliegen*. Siehe [10180](10180-etappe2LueckenNachPlan10.md) Punkt 2.
3. Für Plan 11, Item 2 gibt es keine Item-Datei. Sein „Zurücksetzen“ hat kein Kriterium
   (10180 Punkt 1). „*Nahkampfreichweite* auf der ganzen Strecke“ steht schon in BEW-6.2 und
   hat einen Test (Stellungnahme in 6986). Offen ist nur BEW-22.1.

**Kosten.** Heute keine. Ohne Nachtrag schließt Plan 11 die Etappe ohne BEW-9.2 und ohne den
Ork-Psioniker.

**Gegenvorschlag.** In der Domänenphase 11: BEW-9.2 in ein Item von Plan 11 aufnehmen,
etwa zu BEW-22.1. Item 1 von Plan 11 trennen in *Fliegen* (Spinne) und Ork-Psioniker in der
*Armee*, oder Item 1 nennt beide im Umfang. Für Item 2 eine Item-Datei schreiben, mit den
Kriterien aus 10180 Punkt 1.

**Stellungnahme.** Umgesetzt, schon jetzt, damit
[10160](10160-schliesstPlanZehnEtappeZwei.md) F1 B möglich bleibt: 1 und 3 im neuen Item
[zuruecksetzenUndLuecken](../../domaene/items/zuruecksetzenUndLuecken.md) (Zurücksetzen nach
10180 Punkt 1, BEW-22.1, BEW-9.2, QUE-11.1; es ersetzt phaseBeendenNurImZug); 2:
[fliegen](../../domaene/items/fliegen.md) nennt Spinne und Ork-Psioniker im Umfang.
