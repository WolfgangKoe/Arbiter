# Todo — Arbiter

## Ziel 1: Grundstruktur Spielphasen-Navigation ✅ abgeschlossen

- [x] `src/domain/models/phase.py` — 7 Phasen als Konstante
- [x] `src/adapters/web/templates/base.html` — 3-Spalten CSS Grid + Header
- [x] `src/adapters/web/templates/index.html` — Phase, Navigation, Game Over
- [x] `src/adapters/web/static/style.css` — minimales Dark-Theme-Layout
- [x] `src/adapters/web/routes/main.py` — Spielfluss via Query-Parameter
- [x] `run.py` — Flask-Einstiegspunkt (Port 5000)
- [x] 21 Tests grün (`tests/domain/` + `tests/adapters/web/`)

---

## Ziel 2: Armeeverwaltung (nächstes Ziel)

- [ ] YAML-Adapter: Units aus `data/wh40k_9e/necrons/units.yaml` laden
- [ ] Domain-Modell: `Army`, `Unit` Klassen
- [ ] Port: `ArmyRepository` Interface
- [ ] Sidebars mit Armeedaten befüllen
- [ ] Tests für YAML-Adapter und Domain-Modelle
