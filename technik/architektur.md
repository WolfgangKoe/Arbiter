# Architektur

Jede Regel nennt, was sie prüft. „Nur Text“: ohne Mechanismus; ein Auslöser dabei: Danach
baut ihn der Regelumsetzer auf Anliegen des Architekten.

## Schichten
Hexagonal: Die Domäne kennt keine Technik, Adapter stecken an den Ports von
[`anwendung/`](architektur/anwendung.md).
```
technik/
  frontend/     HTML, CSS, JS; nur über HTTP an web/
  arbiter/
    web/        Flask: Anfrage → Befehl, Spielstand → JSON, Sperre → 409
    anwendung/  je Handlung ein Dienst; Ports, Befehle, Spielstand
    katalog/    Port Katalog: YAML aus domaene/daten/
    speicher/   Port Partien: die Folge der Befehle (P2)
    domaene/    Fachlogik
    __main__.py steckt Adapter und Dienste zusammen (W5)
  tests/        akzeptanz/, einheit/
```
Ordner entstehen mit dem ersten Item, das sie braucht. Je Ordner eine Datei, dazu der
Vertrag zwischen `web/` und `frontend/` je Phase eine; ihre Höchstmaße:
[Kennzahlen](../prozess/kennzahlen.md#höchstmaße).

Ordner | Datei | Regeln
---|---|---
`arbiter/domaene/` | [Domäne](architektur/domaene.md) | Grundschnitt, S1 bis S3, D1 bis D4, M1
`arbiter/anwendung/` | [Anwendung](architektur/anwendung.md) | Dienste, Ports, Umbau
`arbiter/katalog/` | [Katalog](architektur/katalog.md) | A3, K1 bis K6
`arbiter/speicher/` | [Speicher](architektur/speicher.md) | P1 bis P3
`arbiter/web/`, `__main__.py` | [Web](architektur/web.md) | W1 bis W5
`frontend/` | [Frontend](architektur/frontend.md) | O1 bis O5
`tests/` | [Tests](architektur/tests.md) | T1, T2, B1 bis B5
Vertrag, quer über die Phasen | [Querschnitt](architektur/vertrag/querschnitt.md) | V1, V4 bis V8
Vertrag der *Aufstellung* | [Aufstellen](architektur/vertrag/aufstellen.md) | V2, V3, V9, V10
Vertrag der *Schlacht* | [Schlacht](architektur/vertrag/schlacht.md), [Bewegung](architektur/vertrag/bewegung.md) | V11 bis V15

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft:
  `formregeln/importvertrag.py`, auch relative Importe.
- **A2** Außen kennt innen, nie umgekehrt: `anwendung/` und `katalog/` kennen die Domäne,
  `speicher/` nur `anwendung/` (P1); `katalog/` und `speicher/` kennt nur `__main__.py`.
  Prüft: wie A1, `speicher/` nach P1; der Rest nur Text.
- **A4** `web/` kennt von `arbiter` nur `anwendung/`; `anwendung/` nur die Domäne und die
  Standardbibliothek. Prüft: nur Text; Auslöser: Freigabe des Plans mit dem ersten Item zum
  Speicher, dann `formregeln/importvertrag.py` vor dem Umbau.
