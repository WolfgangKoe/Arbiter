---
title: Arbiter
sdk: docker
pinned: false
---

# Arbiter — WH40k 9th Edition Battle Tracker

Digitaler Spielbegleiter für Warhammer 40.000 9. Edition.

Führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe eingeben.

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
```

## Start

```bash
streamlit run src/app.py   # http://localhost:8501
```

## Tests

```bash
pytest --tb=short          # Vollsuite + Coverage-Gate (99 %)
pytest -n auto --tb=short  # dasselbe, parallel (schneller)
```
