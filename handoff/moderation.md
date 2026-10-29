# Moderation

Stand: Plan 9 wartet auf deine Freigabe ([Plan 9](plan.md)). 31 offene Anliegen; keines hält die
Freigabe auf. Vor den Items laufen laut Plan 6102, 6241, 6290 (Technikphase). Neu seit der
letzten Moderation: BEW-15 steht in Item 4; 7070 ist erledigt und gelöscht.

## Dran
Blockiert das Inkrement: nichts außer der Freigabe.
- Stakeholder: Freigabe Plan 9; Nachprüfung
  [6400](anliegen/6400-anhaltenVorDerNahkampfreichweite.md),
  [6410](anliegen/6410-grenzkreiseNahkampfUndBewegung.md),
  [6420](anliegen/6420-einzelnesModellNachAuswahlDerEinheitZiehen.md) (erst nach Items 3 und 4);
  Fragen unten.
- Technikphase 9, Testautor: 4901, 4921, 5241, 5781, 6241, 6340, 6981, 6993.
- Technikphase 9, Implementierer: 5380, 5701, 6102, 6122, 6290, 6982, 6991, 6992.
- Technikphase 9, Architekt: 5000. Reviewer: 6361.
- Prozessphase 9, Regelumsetzer: 3960, 6432, 6988, 7030. Organisationsentwickler: 6471, 6500, 6960
  (Nachprüfung), [6987](anliegen/6987-rollenInPraemissenUndAblaufVerlinken.md) (F1 und F2
  beantwortet).
- Domänenphase 10, Anforderungsautor: [6986](anliegen/6986-bewegungLueckenFuerSpaeter.md).
- Architekt: [6995](anliegen/6995-frontendUndBackendImOrdner.md), Stellungnahme steht; schließt
  nach Technikphase 9.

## Vorschläge
- 6500 ist beantwortet und nachgeprüft: der Organisationsentwickler trägt das Format in die
  Domäne ein, streicht die Annahme und setzt `erledigt`. 6960 ebenso (F1 bis F4 beantwortet).
- 6987: Du hast F1 und F2 mit A beantwortet (Datei noch uncommittet). Der Organisationsentwickler
  setzt um, sobald sie steht. Deine Ergänzung zu F2 (Quadranten je Perspektive konkretisieren,
  im Ordner-CLAUDE.md nur die eigenen Rollen, sonst nur der Link in `.claude/agents/`) ist neu
  gegenüber A: er klärt sie in seiner Stellungnahme, bevor er sie umsetzt.
- 6981 und 6982 tragen dasselbe Thema (Es 8, Docstrings); getrennte Dateien, Testautor und
  Implementierer laufen gleichzeitig.
- 6991, 6992, 6993 sind Mutationslücken (Zyklus 8); getrennte Module, gleichzeitig möglich,
  zusammen unter einer Abnahme durch den Reviewer.
- 4901, 5241, 5781, 6340, 6241, 4921 betreffen dieselben Bewegungstests: ein Lauf des
  Testautors als Kette, 6241 zuerst (Plan). 6102, 6290 zuerst, dann 6122, 5701, 5380 als Kette
  des Implementierers; 6982 und 6991/6992 danach, wenn Dateien gleich sind.
- 6400, 6410, 6420 legen nur Entscheidungen ab; Items 3 und 4 setzen sie um, dann schließt du.
- 6995 F3 (`komponenten/`) und 6410 gehören zu Item 4; keine eigene Arbeit.
- 3960, 6432, 7030: Regelumsetzer; höchstens einer ändert Hook-Code, sonst eine Kette
  (7030 berührt `lesen/plan.py`, 6432 `zuegeUebernehmen.py`, getrennt). 6471 und 6987 beim
  Organisationsentwickler gleichzeitig, 6988 nach den Regeländerungen.

Stränge Technikphase 9: Testautor und Implementierer laufen nebeneinander, solange die Tests
des Items zuerst stehen (Plan: Tests vor Code); Architekt und Reviewer prüfen danach.

## Fragen an dich
Mit `Annahme:` (die Arbeit läuft weiter):
- [6995](anliegen/6995-frontendUndBackendImOrdner.md) F2 (Annahme A) und F3 (Annahme A): Dein
  Kommentar folgt den Empfehlungen; es fehlt die Zeile `Antwort:`.

Ohne `Annahme:`:
- [6995](anliegen/6995-frontendUndBackendImOrdner.md) F1: Der Architekt liest F1 B; trage
  `Antwort: B`.
