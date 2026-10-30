# Übergehen benannt übergeben, Knopf vor der Handlung prüfen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Kritik an den Tests zu Item gemeinsamUebergehen (Schnittstelle, Lesbarkeit).
Hält auf nach [Kritik](../../prozess/ablauf/kritik.md):

1. `testBew8_2ÜbergehenOhneJedenGrundDerSperreSperrtMitAllenGründenUndLässtDenStand` in
   [uebergehenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/uebergehenBeimZiehenTest.py)
   übergibt die übergangenen *Gründe* als drittes Argument nach der Stelle:
   `sperrgründe(schlacht.modellLoslassen, modell, ziel, übergangen)`. Der
   [Vertrag V18](../../technik/architektur/vertrag/schlacht/uebergehen.md) nennt
   `übergehen=`, alle anderen Tests auch. Der Lauf zeigt es: Dieser Test scheitert heute mit
   „takes 3 positional arguments but 4 were given“, die übrigen mit „unexpected keyword
   argument 'übergehen'“. Macht der Implementierer `übergehen` nur benannt
   (`modellLoslassen(modell, stelle, *, übergehen=frozenset())`, die lesbarste Form), bleibt
   dieser Test rot mit `TypeError`, nicht mit `Sperre`; und wer die Zeile liest, sieht nicht,
   was das vierte Argument ist.
2. `testBew8_1NachDerNächstenHandlungOhneSperreBietetDieSeiteGemeinsamÜbergehenNichtMehrAn`
   ist schon ohne Produktcode grün (geprüft), denn es gibt noch keinen Knopf. Der Test prüft
   „nicht mehr“, ohne vorher zu zeigen, dass der Knopf da war; er bliebe grün, wenn die Seite
   „gemeinsam übergehen“ nie anbietet ([Absicht 1](../../prozess/praemissen/absicht.md), 692).

**Kosten.** Je eine Zeile, am Bildschirm nichts. Ohne 1 legt der Test die Schnittstelle
anders fest als der Vertrag; ohne 2 belegt ein grüner Test BEW-8.1 nicht.

**Gegenvorschlag.**
1. In [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py) nimmt `sperreBei` auch
   benannte Argumente (`def sperreBei(handlung, *argumente, **benannte)`, weiter an
   `handlung`), `sperrgründe` ebenso; der Test ruft
   `sperrgründe(…, ziel, übergehen=übergangen)`.
2. Im Aufbau nach `sperrmeldungWarten(seite, {Grund.überEineBase})`:
   `expect(knopfDerSeite(seite, übergehenKnopf)).to_be_visible()`, wie `istNichtEingefahren`
   vor der Handlung in [leistenTest.py](../../technik/tests/akzeptanz/querschnitt/leistenTest.py).

**Stellungnahme.** Angenommen und umgesetzt wie vorgeschlagen.
1. `sperreBei` und `sperrgründe` in
   [handgriffe.py](../../technik/tests/akzeptanz/handgriffe.py) reichen benannte Argumente
   weiter; der Test ruft `sperrgründe(…, ziel, übergehen=übergangen)` und scheitert jetzt
   wie die übrigen mit „unexpected keyword argument 'übergehen'“.
2. Der Aufbau des Tests zu „nicht mehr angeboten“ prüft den sichtbaren Knopf (wie 7300).

Daneben, für ruff (PLR0913): `modellLoslassenUndÜbergehen` in
[dienst.py](../../technik/tests/akzeptanz/dienst.py) nimmt keine *Einheit* mehr, sie folgt aus
dem *Modell*; `zugÜberEineBase` in [conftest.py](../../technik/tests/akzeptanz/conftest.py)
holt *Spieler* und *Einheit* über `request.getfixturevalue`.
