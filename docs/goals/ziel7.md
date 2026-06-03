# Ziel 7 — Crusade-Erweiterung ⬜

**Voraussetzung:** Ziel 6 abgeschlossen.

Crusade erfordert persistente Aufzeichnungen während und nach dem Spiel. Das `gameProtocoll` wird vom reinen Log zum strukturierten Tracking-System erweitert.

**Vorbedingung aus Ziel 6:** Das Game-Log-Format (strukturierte JSON mit `attacker_unit`, `target_unit`, `target_destroyed` pro Event) wird bereits in Ziel 6 etabliert. Ziel 7 baut darauf auf — kein separates Kill-Tracking mehr nötig.

---

- [ ] `gameProtocoll.py` Refactoring: Tabs für Battle Log / Agendas / Order of Battle
- [ ] Agenda-Auswahl vor Spielbeginn (3 Agendas pro Spieler, aus `agendas.yaml`)
- [ ] Agenda-Tracking während des Spiels (Fortschritt + Punkte)
- [ ] XP-Spalte pro Einheit im Protokoll (earned this battle)
- [ ] Battle Honours / Battle Scars (Post-Game-Eingabe)
