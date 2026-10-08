# Backend-Tests am Vertrag: Testautor oder Implementierer

327 · Kritik · von Testautor (Technik) → Architekt · Runde 1/3 · offen

## Runde 1
**Befund.** [Ablauf, Technikphase 1](../../prozess/ablauf.md#technikphase) lässt den Testautor das
Backend mit dem Flask-Testclient testen. [Vertrag](../../technik/architektur/vertrag.md) legt diese
Tests als `tests/einheit/web/anwendungTest.py` fest; `tests/einheit/` schreibt der Implementierer,
der Testautor schreibt dort nichts (Kein Produktcode, keine Unit-Tests).

**Kosten.** Beide Rollen können sich auf die Quelle berufen; der Test zu V1 und V2 bleibt
ungeschrieben oder entsteht doppelt.

**Gegenvorschlag.** Eine Seite angleichen: Entweder schreibt der Testautor die Tests gegen V1 und V2
als Akzeptanztests unter `technik/tests/akzeptanz/` (Ablauf bleibt, Vertrag nennt den Ort), oder der
Ablauf nennt den Implementierer für `tests/einheit/web/`.

Erledigt, wenn Ablauf und Vertrag dieselbe Rolle und denselben Ort nennen.

**Stellungnahme.**
