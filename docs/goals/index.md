# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

Zielarchitektur: `app.py` + `uiLayout/` + `gameObjects/` + `gameMechanic/`
Details: `docs/spec/architecture.md` · UI-Spec: `docs/spec/ui_layout.md`

---

## Aktueller Stand

| Ziel | Status |
|------|--------|
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig (archiviert) |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig (archiviert) |
| Ziel 2 — Command Phase | ✅ fertig (archiviert) |
| Ziel 3 — Combat Foundation | ✅ fertig (archiviert) |
| Ziel A — Architektur-Review | ✅ fertig (archiviert) |
| Ziel 4a — Badges & Einheitenzustand | ✅ fertig (archiviert) |
| Ziel 4b — armyCard + unitCard Redesign | ✅ fertig (archiviert) |
| Ziel 4c — Ability Engine Refactoring | ✅ fertig (archiviert) |
| Ziel 4d — Befehlsphase vollständig | ✅ fertig (archiviert) |
| Ziel 4e — Bewegungsphase vollständig | ✅ fertig (archiviert) |
| Ziel 4f — Psychic Phase | ✅ fertig (archiviert) |
| Ziel 4f.1 — Psychic Phase Nachbesserungen | ✅ fertig (archiviert) |
| Ziel 4g — Angriffsphase (Charge Phase) | ✅ fertig (archiviert) |
| Ziel 4h — Moralphase | ✅ fertig (archiviert) |
| **Ziel 5 — Setup & Datenlage** | ✅ fertig (2026-06-03, archiviert) |
| Ziel 5a — Datenstruktur & Spec | ✅ fertig (archiviert) |
| Ziel 5b — Necrons Katalog | ✅ fertig (archiviert) |
| Ziel 5c — Loader-Refactoring | ✅ fertig (archiviert) |
| Ziel 5d — BattleScribe Importer | ✅ fertig (archiviert) |
| Ziel 5e — Setup-Screen Redesign | ✅ fertig (archiviert) |
| Ziel 5f — Stratagems PoC | ✅ fertig (2026-06-03, archiviert) |
| Ziel 5g — Regelkonformer Setup-Flow | ✅ fertig (archiviert) |
| Ziel 5h — Orks-Katalog | ✅ fertig (archiviert) |
| Ziel 5i — Abschluss: Offene Punkte | ✅ fertig (2026-06-03, archiviert) |
| Ziel 5j — FW Necrons + Ork Datenqualität | ✅ fertig (2026-06-03, archiviert) |
| **Ziel 6 — UI-Overhaul, ArmyCard, Attackensequenz** | ✅ erreicht (S119, 2026-07-03) |
| Ziel 7 — Gefechtsoptionen + subfaction-Mechanik | ⬜ geplant |
| Ziel 8 — Crusade-Erweiterung | ⬜ geplant |
| Ziel 9 — Wahapedia Faction Fetcher | ⬜ geplant |
| Design-Block — UI-Theme | ⏳ eigene Session |

Details je Ziel: `archive/ziel1.md` – `archive/ziel5.md` (erledigt, archiviert) · `ziel6.md` – `ziel9.md` · Doku-Bereinigung: `archive/doku.md`

---

## Design-Block — UI-Theme ⏳ (eigene Session)

- [ ] Farbpalette überarbeiten — Goldtöne, Primärfarbe, Kontraste
- [ ] Badge-Optik und Spacing prüfen
- [ ] Einheitenkarten-Layout verfeinern

---

## Offene Designfragen

Dokumentiert in `docs/spec/architecture.md` — Abschnitt "Open Design Questions".
