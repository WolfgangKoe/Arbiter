# Tests zu Item einheitVerschieben: Stand der Umsetzung, Rundungsfall und offene Prüfungen

1370 · Kritik · von Implementierer → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die Belegungsschwelle kam vor dem Ende. Umgesetzt (Domäne, Dienst, Seite):
- [auswahl.py](../../technik/arbiter/domaene/phasen/aufstellen/auswahl.py): *Ebene* (`ebene`, `ebeneWählen`, `ebeneAbwählen`, `modellAusgewählt`), AUF-20.2, 25.
- [einheitVerschieben.py](../../technik/arbiter/domaene/phasen/aufstellen/einheitVerschieben.py) (neu): Block um den Weg des gezogenen, gemeinsames Hineinrücken (AUF-21.1, 21.2, 26.1).
- [`__init__.py`](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py): `modellLoslassen` verschiebt den Block, wenn die *Ebene* die *Einheit* ist, sonst nur das gezogene *Modell* (AUF-20.4); `_loslassen` prüft gegen die *Modelle* außerhalb des Loslassens (AUF-24.2); [gesperrtesModell.py](../../technik/arbiter/domaene/phasen/aufstellen/gesperrtesModell.py) merkt die Stellen vor dem Loslassen, „zurück“ stellt den ganzen Block wieder her.
- [darstellung.py](../../technik/arbiter/web/darstellung.py), [anwendung.py](../../technik/arbiter/web/anwendung.py): `ausgewählt` je *Modell*, `ebene`, Route V9 (404 ohne *gesetztes* *Modell* der *ausgewählten* *Einheit*).
- [seite.js](../../technik/frontend/seite.js): alle `ausgewählt`en Kreise folgen dem Zeiger, Klick auf ein *Modell* sendet V9.

Letzter Lauf (Domäne und Dienst, ohne Bildschirm): 386 grün, 86 rot; alle roten außer zwei gehören zu anhaltenAnBases (AUF-24.1, 26.2 bis 26.4). Nicht gelaufen nach den letzten Änderungen: Bildschirmtests, `ruff` über alles, `prozess/pruefungen`, Unit-Tests zu `einheitVerschieben.py` und `auswahl.py`, Unit-Tests 404 der Route V9.

Zwei Tests bleiben rot: `testAuf24_2DerDienstAntwortetOhneSperreUndSetztBeideModelleAnDieNeueStelle[zweitesGezogen-umEinenRadiusVor]` und `[zweitesGezogen-vor2]`. Grund: `web/` liest die Zahl wie gesendet (S2), der Weg des gezogenen ist so um 1e-16 ungenau, das mitgezogene *Modell* steht einen Float-Schritt neben `float(exakte Stelle)`. Das ist kein Fehler der Domäne.

**Kosten.** Ohne Änderung bleiben zwei Tests rot, die der Code nicht grün machen kann, ohne S2 zu brechen.

**Gegenvorschlag.** Der Testautor vergleicht den Dienst-Test zu AUF-24.2 mit Toleranz von einem Float-Schritt (`pytest.approx`) oder wählt Ziele, die als Dezimalzahl exakt sind; oder der Architekt entscheidet, dass der Dienst den Weg aus dem Spielstand rechnet.

**Stellungnahme.** Angenommen, kein Vertragsfall: Der Dienst-Test zu AUF-24.2 vergleicht die
Stellen je Nummer mit `pytest.approx(abs=1e-9)`; die Schlüssel (Nummern) bleiben exakt gleich.
Die Seiten- und Domänentests bleiben exakt. In
[blockAlsGanzesTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/blockAlsGanzesTest.py)
sind beide Fälle grün. Der Architekt bestätigt in
[1410](1410-kritikAmCodeEinheitVerschieben.md): Die Toleranz im Dienst-Test ist richtig, der
Dienst rechnet den Weg nicht aus dem Spielstand.
