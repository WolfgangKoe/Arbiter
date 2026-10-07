# Moderation

Stand bbc4ad9, vor Freigabe Retro 3: 14 Anliegen offen, alle Perspektive Prozess; Domäne und
Technik 0. Kritikrunde der anderen Perspektiven entfällt (Stakeholder).

## Dran
Blockiert die Freigabe: nichts. [Retro 3](retro.md) nennt keine Prozess-Items, Plan 4 hängt an
keinem offenen Anliegen.
- Stakeholder: [296](anliegen/296-prozesslastEindaemmen.md) (F1 bis F3 beantwortet, A; setzt
  `angenommen`, Organisationsentwickler hat umgesetzt).
- Regelumsetzer: [216](anliegen/216-commitHooksWirksamMachen.md),
  [246](anliegen/246-dashboardAlleSessionsMitSeitenzaehler.md),
  [249](anliegen/249-werkzeugFestUndImportvertragDerTests.md),
  [275](anliegen/275-dashboardSichtDerAnliegen.md),
  [304](anliegen/304-sammelfehlerBrechenPrueflaufAb.md); 5 von 5 am Deckel.
- Organisationsentwickler: [150](anliegen/150-sonarlintAbdeckungUndToterCode.md) wartet auf
  216; [289](anliegen/289-pruefungenBrechenAmHookDesNachbarnAb.md) wartet auf 304.
- Alle anderen Rollen: nichts.

## Vorschläge
- Löschen lassen (Kopf `erledigt`, Löschlauf, kein Zug nötig): 202, 203, 228, 229, 232, 302.
  Retro 3 zählt sie noch als offen beim Regelumsetzer; die Dateien sind es nicht mehr.
- Zusammen in einem Lauf des Regelumsetzers (Strang Prüfskript-Werkzeug und Dashboard):
  246 mit 275 (dieselbe Datei `rollenregeln/dashboard.py`).
- Strang Hook-Code, höchstens ein Lauf ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)):
  304 zuerst (`pyproject.toml`), dann 216. 249 ändert `pyproject.toml` und den Importvertrag
  und läuft nach 304, nicht daneben.
- Nach 304 schließt der Organisationsentwickler 289; nach 216 meldet er 150 an den
  Stakeholder. 150 und 289 sind reine Warteposten ohne eigene Arbeit.
- Reihenfolge ohne Wirkung auf Plan 4: Die Kette läuft neben dem Produkt, Vorrang hat Plan 4.

## Fragen an dich
Keine offen. Retro 3 trägt `Freigabe: ja` und `Kommentar: .` schon.
