# Etappe 2: Zurücksetzen, Ork-Psioniker, Weiterziehen nach dem Übergehen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik an den Kriterien von [Etappe 2](../../domaene/etappen/02-bewegen.md). Nichts
hält Plan 10 auf: Kein Punkt betrifft einen Schritt seines Happy Path (Lücken abseits des
Happy Path, [Kritik](../../prozess/ablauf/kritik.md)). Die übrigen Kriterien der Etappe passen
zu Etappe, Ziel und Regeltext.
1. Zurücksetzen: Die Etappe sagt „bis zum Ende der Phase lässt sich jede zurücksetzen“. Ein
   Kriterium dazu gibt es nur für eine *vorgerückte* *Einheit*
   ([BEW-12.2](../../domaene/anforderungen/phasen/bewegung/vorrueckenZuruecknehmen.md)). Eine
   *Einheit* mit *Normaler Bewegung* zieht man nach BEW-1.6 von Hand zurück, an ihre alte
   *Stelle* nur nach Augenmaß. ArbiterMap setzt die Bewegung einer *Einheit* auf einen Klick
   zurück (`ArbiterMap/docs/spec/interaction_map.md:704`). Plan 11, Item 2 kündigt
   „Zurücksetzen“ an, ein Kriterium dazu fehlt.
2. Ork-Psioniker: Die Etappe verlangt ihn neu in der *Armee*. Es gibt kein *Datenblatt*,
   keine Zeile in `ausgangslage.yaml`, kein Kriterium (so steht es auch in deiner Stellungnahme
   in [9340](9340-fliegenDerSpinne.md)). Der Weirdboy hat 5″ (`Arbiter-old/data/wh40k_9e/orks/units.yaml:259`)
   und kein FLY (`:254`), also kein *Fliegen*. Den *Durchmesser* seiner *Base* nennt keine
   Quelle (`ArbiterMap/data/poc/units/` hat keine Datei dazu).
3. Weiterziehen nach dem Übergehen: Nach [BEW-8.4](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md)
   stehen die Boyz weiter als ihre *Bewegungsweite* oder in *Nahkampfreichweite*. Zieht man
   sie danach noch einmal, verlangen BEW-3.1 und 6.2 eine *Stelle* auf der Strecke, an der
   keines über der *Bewegungsweite* oder in *Nahkampfreichweite* ist. Am Anfang der Strecke
   gilt das aber schon nicht mehr. Nach V16 halten sie dann am Anfang an, auch wenn man sie
   vom Gegner weg zieht. Wer den Fehler zurücknehmen will, muss also wieder *gemeinsam
   übergehen*, und das *Protokoll* nennt ‚Nahkampfreichweite‘ beim Verlassen. Bei der ganzen
   *Einheit* als *Ebene* reicht dafür ein einziges übergangenes *Modell*. Dazu nennt
   [BEW-21.1](../../domaene/anforderungen/phasen/bewegung/sperreBeimLoslassen.md), wie
   [AUF-12.8](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md), für die
   *Sperre* ‚Nahkampfreichweite‘ (QUE-1.3) kein *gemeinsam übergehen*. Ziel und Glossar
   (*Sperre*) verlangen es, denn nur ‚keine Kohärenz‘ und ‚Base überdeckt‘ sind ausgenommen.

**Kosten.** Heute keine. Bleibt es liegen: (1) Etappe 2 schließt mit Plan 11 ohne ihr
Zurücksetzen. (2) Der Ork-Psioniker fehlt in der Partie Orks gegen Necrons. (3) Mit Item 1
wird der Fall erreichbar: Wer ein *gemeinsam übergehen* bereut, kommt nur mit einem zweiten
zurück, und das *Protokoll* zeigt einen falschen *Grund*.

**Gegenvorschlag.**
1. Den Stakeholder fragen. A: ein Knopf, der die *Einheit* an ihre *Stellen* zu Beginn der
   *Bewegungsphase* zurücksetzt wie BEW-12.2 (ArbiterMap). B: Zurückziehen nach BEW-1.6 genügt,
   Plan 11 streicht „Zurücksetzen“ (Anliegen 5180 F5). Empfehlung: A, denn die Etappe verlangt
   es, und BEW-12.2 hat das Verhalten schon.
2. *Datenblatt* `Weirdboy` mit `bewegungsweite: 5` und ohne `fliegen`, dazu eine Zeile in
   `ausgangslage.yaml`. Den *Durchmesser* den Stakeholder fragen, so wie in 9400 F1.
3. BEW-3.1 und 6.2 halten nur an, wenn die Strecke etwas überschreitet, das am Anfang noch
   nicht überschritten war. Das ist dasselbe Muster wie „an der zuvor gezeigten *Stelle* nicht
   *überdeckt*“ in AUF-29.1 und BEW-17.1. Dazu der Stakeholder: Bietet BEW-21.1 bei
   ‚Nahkampfreichweite‘ *gemeinsam übergehen* an? A: ja (Ziel). B: erst mit QUE-5.1 in
   Etappe 7 (Anliegen 9940). Empfehlung: A, denn so verlangt es das Ziel.

**Stellungnahme.** 1: BEW-24. 2: MIV-2; Daten: 10340. 3: abgelehnt, Zweck BEW-25, BEW-21.
