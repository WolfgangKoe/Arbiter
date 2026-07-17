STATUS: NEEDS-DECISION

# S159 — UI-Verifikation B-028b (Noctilith Beacons — erste B-028a-Callsite)

Render-Code (`gameMechanic/psychicPhase.py`) ist nicht von der Coverage-Messung erfasst
(CLAUDE.md „Warum Render-Code aus der Messung ausgeschlossen ist") — manuelle Prüfung in der
laufenden App PFLICHT, bevor B-028b endgültig als visuell bestätigt gilt.

**Design-Entscheidung dieser Session (zur Kenntnisnahme, keine Rückfrage nötig):** Die neue
Noctilith-Beacons-Karte ist **additiv, nicht gatend** — sie erscheint neben dem bestehenden
Deny-the-Witch-Wurf-UI, blockiert dieses aber nicht. PSYKER- und Wargear-basierte Deny-Pfade
bleiben unverändert (weiterhin ohne eigene Karte, direkt zum Wurf-Eingabefeld). Falls das
Verhalten stattdessen gatend sein soll (Karte muss erst „benutzt" werden, bevor der Wurf
möglich ist), bitte als eigenen Folge-Task vermerken.

## Testfall 1 — Noctilith-Beacons-Karte erscheint im Deny-Column bei manifestierter Kraft

**(a) Voraussetzungen:** Necron-Roster mit „The Silent King" (Szarekh, `the_silent_king`,
besitzt `noctilith_beacons`, KEIN PSYKER-Keyword, kein Deny-Wargear) im Roster von Spieler A.
Spieler B (beliebige Fraktion mit PSYKER-Einheit, z. B. eigene Necrons mit einem PSYKER oder
andere Fraktion) ist aktiver Spieler in der Psychic-Phase.

**(b) Klickpfad:** Psychic-Phase öffnen → Spalte von Spieler B (aktiv): PSYKER-Einheit
auswählen, 2D6-Wert ≥ Warp Charge eintragen (z. B. 8 bei WC 5), „Attempt Manifest" klicken, sodass
die Kraft manifestiert. Danach zur Spalte von Spieler A (inaktiv, Deny-Column) wechseln.

**(c) Erwartung inkl. Ausgangs-State:** Ausgangs-State vor diesem Fix: Spieler A konnte mit
Szarekh im Roster überhaupt keinen Deny-Versuch unternehmen (`can_deny()` erkannte nur
PSYKER-Keyword/Wargear). Jetzt: In der Deny-Column erscheint zusätzlich zum bestehenden
„Deny the Witch: 2D6 > X"-Eingabefeld eine eigene GO-Karte „Noctilith Beacons" mit dem
Regeltext („…Szarekh can attempt to deny one psychic power as if he were a PSYKER.") und
einem „Use"-Button. Das bestehende Wurf-Eingabefeld + Attempt-Deny/Skip-Deny-Buttons sind
unverändert vorhanden und funktionieren unabhängig davon, ob die Karte benutzt wurde.

Befund: positiv

## Testfall 2 — Use/Undo-Zyklus der Karte (Vollrückgängig-Garantie)

**(a) Voraussetzungen:** Wie Testfall 1, Zustand nach Schritt (b) erreicht (Karte sichtbar,
Zustand „ready").

**(b) Klickpfad:** Auf der Noctilith-Beacons-Karte „Use" klicken. Danach auf derselben Karte
„Undo" klicken.

**(c) Erwartung inkl. Ausgangs-State:** Ausgangs-State: Karte zeigt „ready" (Use-Button aktiv).
Nach „Use": Karte wechselt in den „used"-Zustand (Use-Button verschwindet/deaktiviert, Undo
erscheint) — das bestehende Deny-the-Witch-Wurf-Feld bleibt währenddessen unverändert bedienbar
(kein Blocker). Nach „Undo": Karte kehrt vollständig in den „ready"-Zustand zurück (Use-Button
wieder aktiv) — keine Reste im State (keine Fehlermeldung, kein hängender „used"-Zustand).

Befund: Positiv

## Testfall 3 — Bestehende Deny-Pfade unverändert (Regression)

**(a) Voraussetzungen:** Necron-Roster OHNE Szarekh, aber mit einer Einheit mit Deny-Wargear
(z. B. Canoptek Spyder mit `gloom_prism`) ODER einer PSYKER-Einheit. Gegner manifestiert eine
Kraft wie in Testfall 1.

**(b) Klickpfad:** Wie Testfall 1 (b), aber in der Deny-Column von Spieler A befindet sich
KEINE Einheit mit `noctilith_beacons`-artiger Ability.

**(c) Erwartung inkl. Ausgangs-State:** Ausgangs-State (vor diesem Fix) und jetziger Zustand
sind identisch: Deny-the-Witch-Wurf-Eingabefeld erscheint direkt, OHNE zusätzliche
Ability-Karte darüber (da keine Einheit mit `deny_psychic`-Unit-Ability im Roster ist).

Befund: Es fehlt ein Roster mit Canoptek Spyder.