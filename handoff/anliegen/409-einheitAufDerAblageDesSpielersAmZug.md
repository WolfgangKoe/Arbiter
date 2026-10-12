# AUF-16.5 prüft nur die Einheit des Spielers an der Reihe

409 · Kritik · von Fachkritiker (Domäne) → Testautor (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** [AUF-16.5](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md)
sperrt jede *Einheit*, die auf der *Ablage* des anderen *Spielers* losgelassen wird. Gemeint
ist der *Spieler*, dem die *Einheit* nicht gehört (Gegenstück zu AUF-16.4, „*Ablage* ihres
*Spielers*“). Beide Tests in
[loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
ziehen nur die Boyz von Spieler 1, der an der Reihe ist, auf die *Ablage* von Spieler 2.
Damit ist die *Ablage* des anderen *Spielers* zugleich die des *Spielers*, der nicht an der
Reihe ist. Nicht geprüft ist der Fall, den das Kriterium ebenso regelt: Die Necron Warriors
von Spieler 2 werden auf der *Ablage* von Spieler 1 losgelassen, also auf der des *Spielers*,
der an der Reihe ist. Auch hier gilt *Sperre* ‚nicht wählbar‘ (AUF-16.5, ebenso AUF-12.2:
außer der Reihe).
Nebenbei: Der Bildschirmtest prüft nicht, dass Arbiter *gemeinsam übergehen* nicht anbietet.
Das verlangt AUF-12.3, auf das AUF-16.5 verweist. Beim Loslassen außer der Reihe wird es
geprüft (`testAuf12_3DieSeiteNenntDenGrundNachDemLoslassenAußerDerReiheUndBietetGemeinsamÜbergehenNichtAn`).

**Kosten.** Ein Code, der statt nach dem Besitzer der *Einheit* nach dem *Spieler* an der
Reihe unterscheidet (`ablage is not anDerReihe`), besteht AUF-16.4 und AUF-16.5 grün. Er
lässt aber die Necron Warriors auf der *Ablage* von Spieler 1 still zurückspringen, ohne
*Grund*. Der heutige Code unterscheidet richtig (`einheit not in ablage.armee.einheiten`),
doch kein Test hält ihn dabei. Die fehlende Prüfung auf den Knopf kostet wenig, denn die
Seite zeigt ihn heute nirgends.

**Gegenvorschlag.**
1. Den Domänentest zu AUF-16.5 nach der *Einheit* parametrisieren, wie AUF-16.1 es tut:
   Boyz auf die *Ablage* von `spielerZwei` und Necron Warriors auf die *Ablage* von
   `spielerEins`. Bei beiden gilt `{Grund.nichtWählbar}`, und die *Stellen* bleiben wie davor.
2. Im Bildschirmtest zu AUF-16.5 zusätzlich
   `assert knopfDerSeite(seite, "gemeinsam übergehen").count() == 0`.

**Stellungnahme.** Angenommen. Statt den bestehenden Test umzubauen (er hängt an den gesetzten
Modellen der Boyz), steht der zweite Fall als eigener Domänentest
`testAuf16_5EineEinheitAufDerAblageDesAnderenSpielersAmZugIstNichtWählbar`: Necron Warriors auf
der *Ablage* von `spielerEins`, `{Grund.nichtWählbar}`, *Stellen* wie davor. Der Dienst-Test aus
407 deckt beide Richtungen ab. Der Bildschirmtest prüft nun, dass *gemeinsam übergehen* fehlt.
Alles in [loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py).
