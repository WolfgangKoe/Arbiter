# Test zu BEW-8.1 „nicht mehr angeboten“ ist ohne Code grün

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item gemeinsamUebergehen. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md) („ein Test prüft sein Kriterium nicht“) und
[Technikphase](../../prozess/ablauf/technikphase.md) Schritt 1 („rot“):
`testBew8_1NachDerNächstenHandlungOhneSperreBietetDieSeiteGemeinsamÜbergehenNichtMehrAn` in
[uebergehenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py)
ist heute grün, obwohl es „gemeinsam übergehen“ noch nicht gibt. Der Aufbau wartet nur auf die
*Sperrmeldung*, nicht darauf, dass der Knopf erscheint; „nicht mehr“ setzt aber voraus, dass
Arbiter ihn vor der nächsten Handlung anbietet (BEW-8.1 „solange er ihren *Grund* nennt“). Für
sich allein unterscheidet der Test nicht zwischen „verschwindet nach der Handlung“ und „gab es
nie“ (Absicht 1, Anliegen 692). Die übrigen Tests der drei Dateien treffen ihr Kriterium;
die QUE-5.5-Tests sind zu Recht schon grün, sie prüfen eine Abwesenheit und stellen die
*Sperre* ‚keine Kohärenz‘ vorher fest.

**Kosten.** Am Bildschirm nichts. Ohne Änderung geht ein grüner Test in die Umsetzung, der
die Hälfte „solange“ nur zusammen mit dem Nachbartest prüft. Eine Zeile.

**Gegenvorschlag.** Im Aufbau nach `sperrmeldungWarten(seite, {Grund.überEineBase})`:
`expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()`. Erledigt: der Test ist rot,
bis der Knopf erscheint.

**Stellungnahme.** Angenommen und umgesetzt wie vorgeschlagen: Der Aufbau von
`testBew8_1NachDerNächstenHandlungOhneSperreBietetDieSeiteGemeinsamÜbergehenNichtMehrAn`
prüft nach der *Sperrmeldung*, dass der Knopf sichtbar ist. Ohne Code ist der Test jetzt rot,
weil der Knopf fehlt.
