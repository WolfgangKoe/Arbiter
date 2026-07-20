STATUS: AWAITING-VERIFICATION

# S173 — UI-Verifikation: „Careen!" (B-122) an der Explodes-Kachel

Executor-Brief 2 (S173). Manuelle Prüfung nötig — Render-Code (`_render_pre_explode_stratagem_go`
in `src/uiLayout/_common.py`) ist nicht von der Coverage-Messung erfasst.

## Voraussetzung

- `data/rosters/orks_transport.yaml` enthält einen Gunwagon (`wh40k_9e.orks.unit.gunwagon`,
  Keywords `VEHICLE, TRANSPORT, WAGON, GUNWAGON`) — verifiziert vorhanden.
- Gegnerische Armee mit mindestens einer Einheit (für die Multi-Unit-Ziel-Auswahl nach einem
  positiven Explodes-Wurf, Baustein ④ — nicht Teil dieser Prüfung, aber am selben Roster
  ohnehin vorhanden).

## Klickpfad

1. Gefecht mit den Orks starten, Gunwagon-Einheit auswählen.
2. Gunwagon zerstören (destroyed=True setzen, wie gewohnt über die App).
3. Explodes-Kachel öffnet sich (Baustein ①: „Explodes!" / „Does not explode").
4. Neben Baustein ① erscheint die „Careen!"-GO-Karte (Baustein ②) — Titel „Careen!", CP-Anzeige
   **2 CP** (Gunwagon trägt WAGON), Regeltext im Akkordeon einsehbar.
5. „Careen!" per `[Use]` verwenden.

## Erwartung

- **2 CP werden gebucht** (WAGON-Override) — CP-Anzeige der Orks sinkt um 2.
- Regeltext ist sichtbar (Akkordeon), Log-Eintrag „Careen! used" erscheint im Spiel-Protokoll.
- **Baustein ① („Explodes!" / „Does not explode") bleibt sichtbar und weiterhin manuell
  würfelbar** — Careen! erzwingt die Explosion NICHT und ersetzt den Wurf nicht (anders als
  „Curse of the Phaeron"/`auto_explode`).
- Die Careen!-Karte wechselt in den Zustand „↺ Undo" (§6.1 GoCardState „used").
- **Undo** (`↺ Undo`-Klick) erstattet die 2 CP vollständig; Baustein ① bleibt währenddessen
  unverändert (egal ob der Wurf inzwischen erfolgt ist oder nicht — die beiden Entscheidungen
  sind unabhängig, s. `docs/spec/processes.md` P-16 „vor-Wurf-GO").

Befund: Es ist wie erwartet. Bitte nochmal prüfen, ob bei Explosion des Gunwaggons wirklich D6 Schaden im Umfeld verursacht werden. Falls ja, habe ich nichts gesagt.

## S165-Checkpunkte

- **Regelkonform?** Ja — Wahapedia-Wortlaut (`docs/work/wahapedia_orks/stratagems.txt:312`):
  „…before rolling to see if it explodes… before resolving the explosion. If that VEHICLE is a
  WAGON or TITANIC model, this Stratagem costs 2CP; otherwise, it costs 1CP."
- **Komponente + Anker korrekt?** Ja — Standard-GO-Karte (§6.1), Anker inline neben Baustein ①
  (Baustein ②, `design_system.md` §7.1), kein neuer Container-Typ.
- **Wortlaut-Familie korrekt?** Ja — `Use`/`↺ Undo` (§6.4), kein „Does not explode"-Wortlaut an
  dieser Karte (das gehört ausschließlich zu Baustein ①).
