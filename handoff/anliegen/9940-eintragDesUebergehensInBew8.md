# Eintrag des Übergehens in BEW-8.5, neues BEW-17.3

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (ein Test prüfte sonst nicht sein Kriterium). Nach 9881 und 9901:
1. Den *Eintrag* nach übergangenem Anhalten nennt jetzt
   [BEW-8.5](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md), nicht
   QUE-5.1 (nur *Sperre*). Die Tests aus 9320 zu QUE-5.1, auf das Übergehen eines Anhaltens
   umgebaut, prüfen also BEW-8.5.
2. Nach Item anhaltenAufDemWeg bietet in Etappe 2 keine *Sperre* mehr Übergehen an; QUE-5.1
   bleibt dann nur über AUF-31 (Etappe 7) prüfbar.
3. Neu: [BEW-17.3](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md).

**Kosten.** Je eine Zeile in zwei Items; bei Etappe 7 ein Zusatz an QUE-5.1 von mir.

**Gegenvorschlag.** Item anhaltenUebergehen: Tests aus 9320 zu QUE-5.1 werden Tests zu BEW-8.5;
Item anhaltenAufDemWeg nennt BEW-17.3. QUE-5.1 in Etappe 7 mit AUF-31; sag es, dann setze ich
„(Etappe 7)“.

**Stellungnahme.** Umgesetzt:
1. [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md): Die Tests aus 9320 zu
   QUE-5.1 werden Tests zu BEW-8.5; Abhängigkeit nun BEW-8.4 nach 9941.
2. Ja, QUE-5.1 gehört in Etappe 7 zu AUF-31: setze „(Etappe 7)“. Das Item
   [randfaelleDesAufstellens](../../domaene/items/randfaelleDesAufstellens.md) nennt QUE-5.1.
3. [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md) und der [Plan](../plan.md)
   nennen „BEW-17 (auch BEW-17.3)“; `nennt` trifft BEW-17.3 schon über „BEW-17“.
Der Plan nennt 9941 als Frage an den Stakeholder vor der Freigabe.
