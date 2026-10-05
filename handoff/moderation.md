# Moderation

Stand: Zyklus 3, Technikphase, 36 offene Anliegen; [Review 3](review.md) wartet auf Freigabe.

## Dran
Blockiert das Inkrement: nichts mehr. Von der DoD fehlt nur „Mockup gelöscht“, es hängt an
[262](anliegen/262-komponentenseiteOhnePruefung.md); Plan 4 baut auf dessen Ergebnis.
- Regelumsetzer (30): [253](anliegen/253-pruefskripteSolidUndLesbar.md) Punkte 1, 2, 5, 7;
  [240](anliegen/240-codekritikFuerFrontend.md) Runde 2; 262, 265, 267, 268, 270; 272 bis 276, 278;
  danach 215, 216, 218, 220, 221, 228 bis 232, 247, 249, 202 bis 206.
- Organisationsentwickler: 107, 138, 150, 219 (je wartet auf Regelumsetzer-Arbeit, siehe unten); in
  240 den Vermerk „nur Text“ im Ablauf streichen.
- Stakeholder nachprüfen: [153](anliegen/153-frontendBackendUndDatenbank.md),
  [246](anliegen/246-dashboardAlleSessionsMitSeitenzaehler.md). Bei 246 steht Status `angenommen`,
  die Stellungnahme sagt aber „Ich warte auf Umsetzung“: erst prüfen, ob umgesetzt ist.
- Architekt, Reviewer, Testautor, Anforderungsautor: nichts offen.

## Vorschläge
Reihenfolge Regelumsetzer (deine Vorgaben zuerst, dann meine):
1. 253 Punkte 1, 2, 5, 7, je ein Lauf, je ein Commit (Stakeholder).
2. 240 Runde 2 (Stakeholder).
3. [272](anliegen/272-einzelstellenLassenGegenbeispieleDurch.md): Kritik am Teilstand von 253
   (Punkte 3, 4); gleiche Dateien, kurz nach 253, bevor weitere Module wandern.
4. 262, dann 268 (Teil c von 262 sieht die Klassen), 265, 267, 270. 262 hält die Mockups.
5. [278](anliegen/278-schreibgrenzeMeldetNurDerRolle.md), [273](anliegen/273-pushNurNachDevJeZyklus.md),
   [274](anliegen/274-anliegenZuegeUndLegende.md): sie fassen Kopf und Züge der Anliegen an;
   dann 276, dann 275 und 246 in einem Lauf (beide `dashboard.py`), 275 nutzt die Köpfe aus 274.
6. 215, 216, 218, 220, 221; 229+232, 231+247, 228+230, 249; zuletzt 202 bis 206 (204 mit 205).
Zusammen: 231, 232, 247 (`konfigurationTest.py`); 275 und 246.
Schließen (Organisationsentwickler): 107 und 226 nach 253 (Neubewertung steht in 253); 138 nach 215;
219 nach 220. Anliegen 277 ist erledigt, die Datei darf
weg. 246 trägt noch den Typ `Anliegen`; 274 Punkt 1 deckt das.

## Fragen an dich
Keine offen. Ich habe keine Datei mit offener `F<n>` gefunden; 153 F1 ist mit „.“ beantwortet.
Zur Freigabe von Review 3: Review nennt zwei Ausnahmen für `web/` (270); sie gelten bis 270 erledigt ist.
