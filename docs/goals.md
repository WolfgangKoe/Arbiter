# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).  
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

---

## Ziel 3 — Durchstich

> **Regelgrundlage:** [`docs/rules/schlachtrunde.md`](rules/schlachtrunde.md) ist bindend.

Kein Würfeln — nur Struktur, Zustandsanzeigen und Ablauf als Orientierung für den Spieler.

**Befehlsphase**
- [ ] Dynamische Karte: Layout-Diskussion ausstehend — wartet auf Einheitenkarte-Vorlage

**Psiphase**
- [ ] Dynamische Karte: Psikräfte + Warpenergiewert anzeigen (Daten fehlen noch im Modell)
- [ ] Status pro Kraft: manifestiert / nicht manifestiert / gebannt

---

## Nächste Schritte (nach Ziel 3)

**Armeelisten aus Daten laden** — Einheiten und Werte werden aus YAML geladen statt hart im Code verdrahtet. Ziel: beliebige Armeen spielen können.

- [ ] `data/wh40k_9e/necrons/units.yaml` und `data/wh40k_9e/orks/units.yaml`
- [ ] Generischer YAML-Loader in `src/`
- [ ] Hardcodierte Listen aus `models.py` entfernen
- [ ] Einheitenlogik so abstrahieren, dass sie armeenunabhängig funktioniert

**Spielende & Auswertung**

- [ ] VP-Bedingungen konfigurierbar
- [ ] Siegbedingungen prüfen (nach Runde 5 oder bei Vernichtung)
- [ ] Abschluss-Screen mit Zusammenfassung
- [ ] Fortlaufendes Log aus `data/log/` anzeigen
