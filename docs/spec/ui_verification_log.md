# UI-Verifikations-Log

Dauerhaftes, **append-only** Nachschlagewerk für manuelle UI-Sichtprüfungen (DoD-Punkt 6,
`CLAUDE.md`). Render-Code (`uiLayout/`, `*Phase.py`) ist bewusst von der Coverage-Messung
ausgenommen (Aufwand/Nutzen-Grund, s. `CLAUDE.md` §Testing) — die manuelle Prüfung ist der
Ersatz-Nachweis dafür. Dieses Dokument hält fest, **wer/wann/welches Roster/welcher
Klickpfad/welches Ergebnis** geprüft wurde, damit dieser Nachweis nicht verloren geht, sobald die
zugehörige Handoff-Datei ihren Lebenszyklus beendet.

## Regel: Übergabe aus `docs/handoff/`

Der Handoff-Hygiene-Wächter (`tests/docs/test_handoff_hygiene.py`) bleibt unverändert: eine
`docs/handoff/`-UI-Verifikationsdatei durchläuft weiter `STATUS: AWAITING-VERIFICATION` →
`ANSWERED`/`DONE` und wird danach **gelöscht** — das ist eine funktionierende, bewusst gehärtete
Regel (Durchgangszustand, kein Ablagezustand). Bevor eine solche Datei gelöscht wird, wandert ihr
**Befund** (Datum · Roster · Klickpfad/Ergebnis · Quelle) als neuer Abschnitt hierher. Damit bleibt
`docs/handoff/` klein und transitorisch, während das Prüfergebnis dauerhaft nachschlagbar bleibt
(Stakeholder-Entscheid S179, Option (a) — Begründung: `docs/handoff/S179_planning.md` Abschnitt 3).

**Format je Eintrag:**

```
## S<NN> — <Kurztitel>
Datum: <YYYY-MM-DD> · Roster: <dateiname.yaml>
Ergebnis: <POSITIV/NEGATIV> — <Klickpfad + Beobachtung>.
Quelle: <docs/handoff/…-datei> (gelöscht nach Übernahme)
```

Neue Einträge werden **ans Ende angehängt** (chronologisch), bestehende Einträge werden nicht
rückwirkend verändert.

---

## S178 — B-113 (Reroll-Fähigkeiten, Skorpekh-Hit + Destroyer-Lord-Wound-Aura)

Datum: 2026-07-22 · Roster: necrons_test.yaml

Ergebnis: POSITIV — Reroll-Marker (↺) erscheint im HIT-Block beim Skorpekh-Destroyer-Angriff
(Hardwired for Destruction) und im WOUND-Block bei Destroyer-Cult-Einheiten, solange der Skorpekh
Lord (Aura-Quelle) im Roster/lebt. Gegenprobe: Lord entfernt/zerstört → Reroll-Marker im
WOUND-Block verschwindet, wie erwartet.

Quelle: `docs/handoff/S178_B113_ui_verifikation.md` (gelöscht nach Übernahme)

---

## S179/S180 — B-129 (Skorpekh Lord Hit-Reroll-von-1, `hardwiredForDestruction`)

Datum: 2026-07-23 · Roster: necrons_test.yaml

Ergebnis: POSITIV — HIT-Block zeigt Reroll-Marker-Zeile (↺) unter Slot 1 für Skorpekh Lord. Marker ist grün (Buff-Farbe `#4a9a5a`). Gegenprobe: Einheit ohne `hardwiredForDestruction` (Warrior-Trupp) zeigt **keine** Reroll-Marker-Zeile. Verifiziert Stakeholder S179/S180.

Quelle: `docs/handoff/S179_B129_ui_verifikation.md` (gelöscht nach Übernahme)

---

## S179/S180 — B-130 (Reroll-Marker-Farbe Buff→Grün)

Datum: 2026-07-23 · Roster: necrons_test.yaml

Ergebnis: POSITIV — Reroll-Marker-Zeile (↺) erscheint in HIT- UND WOUND-Block in Buff-Grün (`#4a9a5a`), nicht mehr Orange. Abgrenzungs-Check: Tesla-/Alt.-Fire-Chip (Waffenregel-Badge, `special_die_html`) bleibt **unverändert orange** (`#f59e0b`). Verifiziert Stakeholder S179/S180.

Quelle: `docs/handoff/S179_B130_ui_verifikation.md` (gelöscht nach Übernahme)

---

## S179/S180 — B-131 (Aura-Reichweiten-Hinweis Destroyer-Cult, Klasse B)

Datum: 2026-07-23 · Roster: necrons_test.yaml

Ergebnis: POSITIV MIT 2 FOLLOW-UPS — WOUND-Block zeigt bluen `st.info`-Hinweis wie beschrieben, gated korrekt über `unit_wound_reroll_ones`. 

**Bug**: Hinweis-Kachel erstreckt sich über die ganze gameActionArea statt nur die Player-Area-Spalte (design_system.md §1.9.1).

**Anforderungspräzisierung**: Hinweistext soll konkrete Aura-Spender namentlich listen statt generisch formuliert. Zieltext: „Wound re-roll of 1 (aura ability) applies only while this unit is within 6\" of [unit1], [unit2] or [unitn]." Spender-Liste soll live sein (zerstörte Spender fallen raus). Nachbesserung geplant S180 mit neuem öffentlichen Accessor in `abilityEngine.py`.

Quelle: `docs/handoff/S179_B131_ui_verifikation.md` (gelöscht nach Übernahme)
