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

## Ziel 2: Armeeverwaltung ✅ abgeschlossen

- [x] Domain-Modell: `Unit` + `BATTLEFIELD_ROLE_DE` in `src/domain/models/unit.py`
- [x] Domain-Modell: `Army` + `units_by_role()` in `src/domain/models/army.py`
- [x] Port: `ArmyRepository` ABC in `src/domain/ports/army_repository.py`
- [x] YAML-Adapter: `NecronYamlArmyRepository` in `src/adapters/yaml/`
- [x] DI in `create_app()` — Routes kennen nur den Port
- [x] Sidebars befüllt mit Einheiten gruppiert nach Rolle (deutsch)
- [x] CSS-Styles für `.role-group`, `.role-label`, `.unit-list`
- [x] Architektur-Doku mit Mermaid in `docs/architecture.md`
- [x] 35 Tests grün (17 neu + 18 bestehend)
