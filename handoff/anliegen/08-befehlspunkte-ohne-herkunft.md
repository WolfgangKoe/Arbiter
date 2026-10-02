# Befehlspunkte ohne Herkunft

08 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** [Etappe 5](../../domaene/etappen/05-schiessen.md) lässt Command Re-roll
Befehlspunkte kosten (`core_rules.txt:3124`), mit F11 schon Etappe 3. Woher die Punkte kommen,
sagt keine Etappe, und die Regel macht es abhängig:
- Nur eine Battle-forged-Armee hat Befehlspunkte; Unbound startet mit null (`:2433`, `:3120`).
  Only War verlangt keine Battle-forged-Armee („any models“, `:2257`).
- Der Startwert hängt an der Schlachtgröße nach Power Level (`:2435-2470`), jedes Detachment
  kostet Punkte (`:2532`, Patrol 2 CP `:2604`).
- Je Befehlsphase +1 bei Battle-forged (`:685`), höchstens 1 Punkt Rückgewinn je
  Schlachtrunde (`:2476`), dasselbe Stratagem einmal je Phase (`:3112`).

**Kosten.** Ohne Festlegung erfindet die Umsetzung den Startwert. Voll regelgerecht zieht es
Detachments, Battlefield Roles und Power Level in den Katalog, eine eigene Etappe
Armeeaufbau. Mit einem festen Startwert bleibt es ein Zähler mit drei Regeln.

**Gegenvorschlag.**
- Die Ausgangslage legt fest: Battle-forged ja oder nein, Schlachtgröße, Startwert der
  Befehlspunkte. Frage an den Stakeholder, Wert mit Fundstelle; Detachments rechnet Arbiter
  vorerst nicht.
- Befehlspunkte kommen in die Etappe mit dem ersten Stratagem, dort auch der Bonus je
  Befehlsphase und die Einmal-je-Phase-Regel. F11 (Etappe 3) ist technisch gleich billig wie
  Etappe 5, wenn diese Festlegung mitkommt; ohne sie bleibt Command Re-roll in Etappe 5.
