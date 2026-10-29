# Fraktion und Modellarten der Boyz

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Für Item 1 von [Plan 9](../plan.md) stehen die *Datenblätter* jetzt je
*Fraktion* in [katalog](../../domaene/daten/katalog/), die
[Ausgangslage](../../domaene/daten/ausgangslage.yaml) nennt je *Einheit* *Fraktion*,
*Datenblatt* und je *Modellart* die Zahl der *Modelle*
([MIV-1.5](../../domaene/anforderungen/missionsvorbereitung/ausgangslage.md)). Am Bildschirm
ändert sich nichts.

Neuer Begriff, Freigabe mit Plan 9: *Fraktion* (faction, `core_rules.txt:2484`), bisher Orks
und Necrons; die Architektur verlangt den Schlüssel `fraktion` (`technik/architektur/katalog.md`, K1).

**Kosten.** Ohne Antwort bleibt es bei der Annahme unten; ein Umbau später trifft Daten,
`katalog/` und seine Tests.

**Gegenvorschlag.** „.“ heißt, die Empfehlung gilt.

**F1 · Welche Modellarten haben die Boyz?** A: zwei, 9 Ork Boy und 1 Boss Nob, wie
`Arbiter-old/data/wh40k_9e/orks/units.yaml:515`, `:543` (Arbiter-old). B: eine, 10 Boyz, wie
`ArbiterMap/data/poc/units/orks_boyz.yaml:19` (ArbiterMap). Empfehlung: A. Die 9. Edition hat
ein *Profil* je *Modellart* (`core_rules.txt:561`), der Boss Nob ein eigenes (A 3, S 5, WS 2+,
`units.yaml:545`); mit B wird die *Einheit* umgebaut, sobald eine Etappe diese Werte liest.
Heute haben beide dieselbe *Bewegungsweite* und denselben *Durchmesser*. Warboss, Necron
Warriors und Overlord haben in beiden Quellen nur eine Modellart.
Annahme: A.
Antwort: Noch keine Antwort

**Stellungnahme.**
Kommentar: Diese Fragen sollten über eine Regelrecherche beantwortet werden können. Es ist etwas komplizierter, als du es hier darstellst. Die vollständigen Regeln der 9. Edition sollten in Arbiter-old enthalten sein.
