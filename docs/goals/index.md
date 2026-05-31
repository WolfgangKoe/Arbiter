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
| Ziel 5b — Necrons Katalog (Grunddaten) | 🔄 46/51 Einheiten, kein PL/Punkte |
| Ziel 5b.1 — Necrons vervollständigen | ⬜ nächster Schritt |
| Ziel 6 — Crusade-Erweiterung | ⬜ geplant |
| Ziel 7 — Wahapedia Faction Fetcher | ⬜ geplant |
| Design-Block — UI-Theme | ⏳ eigene Session |

Details je Ziel: `ziel1.md` – `ziel7.md` · Doku-Bereinigung: `doku.md`

---

## Design-Block — UI-Theme ⏳ (eigene Session)

- [ ] Farbpalette überarbeiten — Goldtöne, Primärfarbe, Kontraste
- [ ] Badge-Optik und Spacing prüfen
- [ ] Einheitenkarten-Layout verfeinern

---

## Offene Designfragen

Dokumentiert in `docs/spec/architecture.md` — Abschnitt "Open Design Questions".
