# OBJ-1.2 bis OBJ-1.4 haben keinen eigenen Test

111 · Kritik · von Architekt (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund.** Jedes Kriterium bekommt einen eigenen Akzeptanztest (Architektur T1). Für
OBJ-1.2 bis OBJ-1.4 ([spielobjekte.md](../../domaene/anforderungen/spielobjekte.md)) gibt es
kein Verhalten, das nicht schon ein anderes Kriterium prüft:
- OBJ-1.2 (*Einheiten* aus *Modellen*) und OBJ-1.3 (runde *Base* mit *Durchmesser*): Der
  Test kann nur die *Ausgangslage* ansehen. „Die Boyz haben zehn *Modelle* mit 32 mm“ prüft
  schon AUF-2.6.
- OBJ-1.4 (Rechteck mit den Seitenlängen der *Mission*): Mit der einen *Mission* ist der
  Test wörtlich der von AUF-2.7, `spielfeld == 44″ × 60″`.
- „rund“ und „Rechteck“ lassen sich nicht widerlegen, solange es keine andere Form gibt.

Dieselben Aussagen stehen schon im Glossar (*Einheit*: „ein oder mehrere *Modelle*“, *Base*:
„jedes *Modell* hat eine … rund“, *Spielfeld*: „rechteckig; die *Mission* nennt die Größe“).
Nach `domaene/CLAUDE.md` stehen solche Beziehungen dort, und jede Aussage steht genau einmal.
OBJ-1.1 ist in Ordnung: „die zwei *Spieler* führen verschiedene *Armeen*“ ist ein eigener
Test.

**Kosten.** Bleibt es so, schreibt der Testautor drei Tests, die nichts Neues prüfen: Ein
falscher Wert in `ausgangslage.yaml` macht zwei Tests rot, und die Rückverfolgung zeigt zwei
Kriterien für ein Verhalten. Oder er erfindet ein Verhalten, damit der Test etwas prüft, etwa
„eine *Einheit* ohne *Modell* wird abgewiesen“; das hat niemand entschieden.

**Gegenvorschlag.**
- A: OBJ-1.2 bis OBJ-1.4 entfallen als Kriterien, das Glossar trägt die Aussagen schon;
  OBJ-1 behält OBJ-1.1 und den Zweck. Noch hat keins der drei einen Test; die Kennungen
  kommen nie wieder. Kostet drei Zeilen.
- B: Die drei Kriterien sagen, was Arbiter mit einer *Ausgangslage* tut, die sie verletzt
  (etwa: lädt sie nicht und nennt den Fehler). Dann prüft sie ein Test mit fehlerhaften
  Testdaten. Das ist neues Verhalten im Import, und ob es das geben soll, entscheidet der
  Stakeholder.
- C: so lassen und die doppelten Tests hinnehmen.

Empfehlung A: Heute kommen die Daten nur aus unseren eigenen YAML-Dateien, die die Tests zu
AUF-2.6 und AUF-2.7 vollständig prüfen. B lohnt sich erst, wenn jemand anderes Armeen
einspielt. Berührt A die Entscheidung des Stakeholders in 105 F1, fragst du ihn.
