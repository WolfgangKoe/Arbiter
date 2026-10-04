# Domäne: QUE-1.2 liegt in der Aufstellung statt in `querschnitt.py`

149 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: Review 2, Änderungen seit `Freigabe Plan 2` (`1553538`) unter `technik/`.

**Befund.** [Architektur, Grundschnitt](../../technik/architektur.md#grundschnitt-der-domäne)
legt fest: „`querschnitt.py`: was nach `querschnitt.md` in jeder Phase gilt, zuerst
QUE-1.2.“ Die Prüfung von QUE-1.2 steht als Schleifenzweig in
`Aufstellung._gründeGegenDieStelle` (`technik/arbiter/domaene/phasen/aufstellen.py`),
`technik/arbiter/domaene/querschnitt.py` gibt es nicht. QUE-1 gilt nach seinem Zweck
„wo immer ein *Modell* aufs *Spielfeld* kommt“, nicht nur in der Aufstellung.

**Kosten.** Die nächste Phase, die *setzt* (Ablage und Zurücklegen nach Plan 2, „Danach“;
später Reinforcements), findet die Regel in einer privaten Methode der Aufstellung: Sie
baut sie nach oder zieht sie dann um, beides mit Risiko für die Grenzfälle aus S2. Wer die
Architektur liest, sucht QUE-1.2 an einer Stelle, die es nicht gibt.

**Gegenvorschlag.** In `arbiter/domaene/querschnitt.py` eine Funktion, etwa
`baseÜberdeckt(modell, stelle, stellen: Mapping[Modell, Stelle]) -> bool` über
`messen.überdecken`, das Modell selbst ausgenommen (AUF-3.7). `_gründeGegenDieStelle` ruft
sie und behält in der Schleife nur die Nahkampfreichweite. Einheitstest gespiegelt in
`tests/einheit/domaene/querschnittTest.py`. Hältst du den Umzug für verfrüht („bis eine
zweite Phase es braucht“), lehne mit Begründung ab; dann hebe ich die Zeile der Architektur
zum Architekten.

Erledigt, wenn QUE-1.2 in `querschnitt.py` geprüft wird, die Akzeptanztests unverändert grün
sind (`python3 -m pytest technik/tests`) und `python3 -m pytest prozess/pruefungen` grün ist.

**Stellungnahme (Implementierer).** Angenommen. QUE-1.2 gilt nach seinem Zweck in jeder
Phase, die Architektur nennt `querschnitt.py`. Umgesetzt: `baseÜberdeckt(modell, stelle,
stellen)` in `technik/arbiter/domaene/querschnitt.py`, `_gründeGegenDieStelle` ruft sie und
behält in der Schleife nur die Nahkampfreichweite. Einheitstest:
`technik/tests/einheit/domaene/querschnittTest.py`. Akzeptanztests unverändert grün,
`pytest technik/tests` und `pytest prozess/pruefungen` grün.
