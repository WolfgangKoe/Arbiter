# Todo — Ziel 1: Grundstruktur Spielphasen-Navigation

## Implementierung

- [ ] `src/adapters/web/templates/base.html` — Basis-Layout (3-Spalten CSS Grid)
- [ ] `src/adapters/web/templates/index.html` — erweitern: erbt von base.html, zeigt Phase + Navigation
- [ ] `src/adapters/web/static/style.css` — minimales CSS für 3-Spalten-Layout
- [ ] `src/adapters/web/routes/main.py` — Route `/` mit Phase-State via Query-Parameter (`?phase=0`)
- [ ] Phase-Daten als Konstante in `src/domain/models/phase.py` (Name + Index)

## Verifikation

- [ ] Flask-Server starten, `localhost:5000` im Browser öffnen
- [ ] Vorwärts durch alle 7 Phasen klicken
- [ ] Rückwärts klicken — bei Phase 1 kein Zurück-Button
- [ ] Bei Phase 7 kein Weiter-Button
