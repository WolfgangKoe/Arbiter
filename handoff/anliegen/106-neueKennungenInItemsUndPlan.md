# Neue Kennungen in Items und Plan 2

106 · Kritik · von Anforderungsautor (Domäne) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach der Antwort des Stakeholders in Anliegen 105 (F1 A, F2 A, git) sind AUF-2
und AUF-3 verallgemeinert, für 97. Es gibt AUF-2.1, AUF-2.2, AUF-2.3, AUF-3.1 und AUF-3.3
nicht mehr, und sie kommen nie wieder. Neu:
- [spielobjekte.md](../../domaene/anforderungen/spielobjekte.md): OBJ-1.1 bis OBJ-1.4, Armeen
  aus Einheiten aus Modellen mit Base, Spielfeld (statt AUF-2.1 bis AUF-2.3).
- [aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md): AUF-2.6 (Armeen und
  Bases aus `ausgangslage.yaml`), AUF-2.7 (Spielfeld aus `onlyWar.yaml`); AUF-2.4, AUF-2.5,
  AUF-3.2, AUF-3.4, AUF-3.6 bleiben. AUF-3.7 bleibt, prüft jetzt nach QUE-1.2, AUF-3.2 und
  AUF-3.4, inhaltlich wie vorher.
- [querschnitt.md](../../domaene/anforderungen/querschnitt.md): QUE-1.1 *Setzen* (statt
  AUF-3.1), QUE-1.2 ‚Base überdeckt‘ (statt AUF-3.3).

Item 1, Item 2 und Plan 2 nennen noch die alten Kennungen; Item 2 und
`nahkampfreichweite-beim-setzen` verlinken nur `aufstellen.md`.

**Kosten.** Ohne Änderung schreibt der Testautor Tests zu Kennungen, die es nicht gibt, und
OBJ-1, QUE-1, AUF-2.6, AUF-2.7 bleiben ohne Item; die Rückverfolgung findet sie nicht.

**Gegenvorschlag.**
1. Item `ausgangslage-only-war`: OBJ-1.1 bis OBJ-1.4, AUF-2.4 bis AUF-2.7, mit Link auf
   beide Dateien.
2. Item `sperren-beim-setzen`: QUE-1.1, QUE-1.2, AUF-3.2, AUF-3.6, AUF-3.7 ohne den Teil zu
   AUF-3.4, mit Link auf beide Dateien.
3. Plan 2 entsprechend, Abschnitte „Items“ und „Empfehlung“.
4. Mit dem Schnitt zu Etappe 2: Der Stakeholder hat in 105 F3 A entschieden, dass Arbiter beim
   Bewegen den gezogenen Weg prüft; überdeckt die *Base* unterwegs eine andere, ist der Zug
   gesperrt (`core_rules.txt:729`). Das Kriterium (QUE-2) schreibe ich mit den Anforderungen zu
   Etappe 2; ob es in `02-bewegen.md` steht, entscheidest du.

**Stellungnahme.** 1 bis 3 sind übernommen. In den Items stehen die Kennungen einzeln, weil die
Rückverfolgung keine Bereiche liest. Zu 4: Etappe 2 bleibt vorerst unausformuliert. Bevor ich
sie ausformuliere, lese ich nach meinem Auftrag `git log -S'Etappe 2'` über die Anliegen und
übernehme dabei 105 F3 A.
