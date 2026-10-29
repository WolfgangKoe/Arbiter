# Fraktion und Modellarten der Boyz

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 2/3
Status: erledigt

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

## Runde 2
**Befund.** Recherche im Datenblatt der Boyz aus Arbiter-old
(`Arbiter-old/docs/work/wahapedia_orks/units_all.txt:506`) und in den Grundregeln:
- Zwei *Modellarten*: Die Ausrüstung nennt „Ork Boy“ und „Boss Nob“ getrennt (`units_all.txt:525`).
  Der Export hat nur eine Zeile Werte (`:509`); das eigene *Profil* des Boss Nob steht nur in
  `Arbiter-old/data/wh40k_9e/orks/units.yaml:545`. Die *Bewegungsweite* ist bei beiden 5″.
- Die Größe ist offen: „For every 10 models this unit contains“ (`units_all.txt:525`),
  `units.yaml:498` nennt 10 bis 30. Die Grundregeln: No. nennt Mindest- und Höchstzahl
  (`core_rules.txt:563`), sonst die Zusammenstellung (`:584`); weniger geht als Understrength
  (`:587`). Die *Ausgangslage* nimmt 10; Größe wählen gehört zum Armeebau (Etappe 9).
- Ausrüstung teilt eine *Modellart* weiter: Shoota statt Slugga und Choppa, je 10 *Modelle* ein
  Big Shoota oder Rokkit (`units_all.txt:525`). Die Armeeliste in Arbiter-old führt sie als
  eigene Zeilen, etwa „Ork Boy w/ Shoota“ (`Arbiter-old/docs/work/orks.md:30`).
Damit bleibt A aus Runde 1 (9 Ork Boy, 1 Boss Nob,
[Ausgangslage](../../domaene/daten/ausgangslage.yaml)); offen ist nur, ob eine Ausrüstung eine
eigene *Modellart* macht.

**Kosten.** Bis Etappe 5 liest kein Kriterium Waffen; B baut die Daten jetzt um.

**Gegenvorschlag.** „.“ heißt, die Empfehlung gilt.

**F2 · Ist eine anders ausgerüstete Ork Boy eine eigene Modellart?** A: Nein, die *Modellart*
ist eine Zeile der Profile (`core_rules.txt:561`); Waffen trägt dann je *Modell*, ab Etappe 5
(Regeltext). B: Ja, je Ausrüstung eine, wie die Armeeliste (Arbiter-old `orks.md:30`).
Empfehlung: A; das *Profil* ist bei allen Ork Boy gleich, B vervielfacht die *Modellarten* ohne
neuen Wert.
Annahme: A.
Antwort: .

**Stellungnahme.**
