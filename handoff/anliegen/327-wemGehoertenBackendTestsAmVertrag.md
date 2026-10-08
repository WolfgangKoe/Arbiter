# Backend-Tests am Vertrag: Testautor oder Implementierer

327 · Kritik · von Testautor (Technik) → Architekt · Runde 1/3 · erledigt

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

**Stellungnahme.** Umgesetzt mit der ersten Variante: Der Ablauf bleibt,
[Vertrag](../../technik/architektur/vertrag.md) nennt jetzt dich und die Akzeptanztests der
Anforderung (T1). Die Tests gegen V1 und V2 stehen dort je Kriterium benannt, etwa in
`auf5Test.py` als `testAuf5_3…` mit dem Flask-Testclient; so bleiben Benennung
(`formregeln/benennung.py`) und Spur (`kriterienregeln/rueckverfolgung.py`) ohne Ausnahme.
Grund: Der Test am Vertrag soll vor dem Code und nicht vom Umsetzenden entstehen, sonst
fehlt den gleichzeitigen Läufen von Backend und Frontend der gemeinsame Maßstab. Nur die
Antwort 404 hat kein Kriterium; sie bleibt ein Unit-Test des Implementierers in
`tests/einheit/web/anwendungTest.py`.
