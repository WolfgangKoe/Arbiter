STATUS: NEEDS-DECISION

# S158 — UI-Verifikation B-111 (Badge-Tooltip statt Truncation-Verlust, Variante C)

Render-Code (`diceCompose.py`) ist nicht von der Coverage-Messung erfasst (CLAUDE.md „Warum
Render-Code aus der Messung ausgeschlossen ist") — manuelle Prüfung in der laufenden App
PFLICHT, bevor B-111 endgültig als visuell bestätigt gilt.

## Testfall 1 — Quantum-Shielding-Badge in der Wound-Zeile (Hover-Tooltip)

**(a) Voraussetzungen:** Roster mit einer Necron-Einheit, die eine `wound_auto_fail`-Ability
mit Auto-fail-Slots trägt (Quantum Shielding, siehe S155-Beispiel); Kampfphase aktiv, eine
Attacke gegen diese Einheit ausgelöst bis zur Wound-Auflösung.

**(b) Klickpfad:** Angriff auflösen → Hit-Würfe bestätigen → Wound-Block öffnet sich; dort
den Badge links neben der Auto-fail-Marker-Zeile mit der Maus anfahren (hovern), ohne zu
klicken.

**(c) Erwartung inkl. Ausgangs-State:** Vorher (Ausgangs-State, B-103-Fix) zeigte der Badge
den auf die Spaltenbreite abgeschnittenen Text „Quantum Sh…" (Ellipsis) — ohne jede
Möglichkeit, das volle Label zu sehen. Jetzt: Der sichtbare Badge-Text bleibt unverändert
abgeschnitten („Quantum Sh…", Spaltenbreite und Zeilenumbruch-Verhalten unverändert), aber
beim Hover erscheint der Browser-Standard-Tooltip mit dem vollen Text „Quantum Shielding".
Kein Layout-Sprung, keine Verbreiterung der Badge-Spalte, kein Zeilenumbruch.
