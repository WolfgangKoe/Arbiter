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
| Ziel 1A — uiLayout/ Struktursplit | ✅ fertig |
| Ziel 1B — gameObjects/ Foundation | ✅ fertig |
| Ziel 2 — Command Phase | ✅ fertig |
| Ziel 3 — Combat Foundation | ✅ fertig |
| Ziel A — Architektur-Review | ✅ fertig |
| Ziel 4a — Badges & Einheitenzustand | ✅ fertig |
| Ziel 4b — armyCard + unitCard Redesign | ✅ fertig |
| Ziel 4c — Ability Engine Refactoring | ✅ fertig |
| Ziel 4d — Befehlsphase vollständig | ✅ fertig |
| Ziel 4e — Bewegungsphase vollständig | ✅ fertig |
| Ziel 4f — Psychic Phase | ✅ fertig |
| Ziel 4f.1 — Psychic Phase Nachbesserungen | ✅ fertig (4f.1.c offen) |
| Ziel 4g — Angriffsphase (Charge Phase) | ✅ fertig |
| Ziel 4h — Moralphase | ✅ fertig |
| **Ziel 5 — Setup & Datenlage** | 🔄 in Arbeit |
| Ziel 5a — Datenstruktur & Spec | ✅ fertig |
| Ziel 5b — Necrons Katalog | ✅ fertig |
| Ziel 5c — Loader-Refactoring | ✅ fertig |
| Ziel 5d — BattleScribe Importer | ✅ fertig |
| Ziel 5e — Setup-Screen Redesign | ✅ fertig |
| Ziel 5f — Stratagems PoC | ✅ fertig (2026-06-03) |
| Ziel 5g — Regelkonformer Setup-Flow | ✅ Spec fertig |
| Ziel 5h — Orks-Katalog | ✅ fertig |
| Ziel 5i — Abschluss: Offene Punkte | ⬜ nächster Schritt |
| **Ziel 6 — [folgt nach Ziel 5]** | ⬜ wird definiert |
| Ziel 7 — Crusade-Erweiterung | ⬜ geplant |
| Ziel 8 — Wahapedia Faction Fetcher | ⬜ geplant |
| Design-Block — UI-Theme | ⏳ eigene Session |

Details je Ziel: `ziel1.md` – `ziel8.md` · Doku-Bereinigung: `doku.md`

---

## Design-Block — UI-Theme ⏳ (eigene Session)

- [ ] Farbpalette überarbeiten — Goldtöne, Primärfarbe, Kontraste
- [ ] Badge-Optik und Spacing prüfen
- [ ] Einheitenkarten-Layout verfeinern

---

## Offene Designfragen

Dokumentiert in `docs/spec/architecture.md` — Abschnitt "Open Design Questions".
