# Projektziele — Arbiter

## Vision

Arbiter ist ein digitaler Spielbegleiter für WH40k 9. Edition (Streamlit).  
Er führt zwei Spieler durch eine Partie: Phasen anzeigen, Einheitenstatus verwalten, Würfe berechnen.

---

## UI Refactoring & Layout

Ziel: Eine lesbare, übersichtliche Oberfläche, in der alle spielrelevanten Informationen zur richtigen Zeit am richtigen Ort erkennbar sind — so dass zwei Spieler eine Partie WH40k flüssig begleiten können, ohne in der App zu suchen.

**Voraussetzung:** Layout-Bilder vom Nutzer für folgende Komponenten:

- [ ] Einheitenkachel — Normalzustand
- [ ] Einheitenkachel — Zustände (zerstört / Reserve / Nahkampf / Charged)
- [ ] Top-Bar (Rundenanzeiger, Phasen-Stepper, VP/CP)
- [ ] Zentralbereich — Befehlsphase (einfachste Phase)
- [ ] Zentralbereich — Bewegungsphase mit ausgewählter Einheit
- [ ] Zentralbereich — Fernkampf mit Schütze + Ziel

**Umsetzung (nach Lieferung der Bilder):**

- [ ] `ui.py` in Komponenten aufsplitten (`ui/unit_card.py`, `ui/header.py`, `ui/central/`, …) — kein Behavior-Change, nur Struktur
- [ ] UX-Anpassungen anhand der Layout-Bilder
- [ ] `docs/architecture.md` aktualisieren

---

## Army Abstraction

Ziel: Armeen werden aus dem bestehenden YAML-Katalog (`data/wh40k_9e/<faction>/`) geladen. Im App-UI wählt der Spieler, welche Einheiten er in eine Partie mitbringt. Die Engine-Logik kennt keine hardcodierten Fraktionen mehr.

Keywords aus dem Katalog steuern direkt das Verhalten in der App: welche Phasen eine Einheit nutzen kann, welche Aktionen sichtbar sind, welche Einschränkungen gelten. Neue Regelelemente (Relikte, Warlord-Traits) fügen sich in dieselbe Struktur ein.

- [ ] YAML-Loader: liest `units.yaml` + `weapons.yaml`, löst Referenzen auf
- [ ] In-App Army Builder: Einheiten aus Katalog wählen, Roster für eine Partie zusammenstellen
- [ ] Engine-Logik armeeneutral: keine hardcodierten `"necron_units"`/`"ork_units"`-Keys mehr
- [ ] Keyword-Dispatcher: zentrale Stelle, die Keywords auf Phasenverhalten mappt (`PSYKER` → Psiphase aktiv, `FLY` → Bewegungsregeln, …)
- [ ] Necrons und Orks als erste vollständige Armeen im neuen System

---

## Phase Logic

Ziel: Der Zentralbereich wird von einer reinen Regelanzeige zu echter Spiellogik. Werte beider Armeen fließen in Berechnungen ein, Zustände werden automatisch gesetzt, die App führt aktiv durch die Kampfsequenz.

**Voraussetzung:** Army Abstraction abgeschlossen.

- [ ] Treffersequenz im Zentralbereich vollständig geführt (Treffer → Verwundung → Rettung → Schaden)
- [ ] Automatisches Setzen von Zuständen (z.B. `in_melee` nach Charge, `acted_this_phase` nach Aktion)
- [ ] Spielende: Siegbedingungen prüfen, Abschluss-Screen
- [ ] Spielprotokoll aus `data/log/` im UI anzeigen
