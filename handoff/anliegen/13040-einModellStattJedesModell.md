# Ein Modell statt jedes Modell in BEW-24.1 und BEW-22.1

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund (hält auf: ein Test prüft sein Kriterium nicht).** BEW-24.1 und BEW-22.1 hängen an
*einem* *Modell* der *Einheit*: „von der ein *Modell* nicht steht, wo es zu Beginn der
*Bewegungsphase* stand“ ([BEW-24](../../domaene/anforderungen/phasen/bewegung/einheitZuruecksetzen.md)),
„von der ein *Modell* in *Nahkampfreichweite* … ist“
([BEW-22](../../domaene/anforderungen/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweite.md)).
Kein Test trennt „ein“ von „jedes“ oder „das erste“:
- [einheitZuruecksetzenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/einheitZuruecksetzenTest.py):
  Jeder Test zu 24.1 und 24.2 zieht entweder mit `ganzeEinheitZiehen` alle *Modelle* (das
  erste wird angefasst, die übrigen folgen) oder den Warboss mit einem *Modell*. Ein Code, der
  nur das angefasste oder nur „alle verschoben“ prüft, wird grün.
- [keinVorrueckenAusDerNahkampfreichweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweiteTest.py):
  `inDerNahkampfreichweite` nimmt Warboss und Overlord mit je einem *Modell*. `all` statt
  `any` über die *Modelle* bliebe grün.

**Kosten.** Der Happy Path aus [Plan](../plan.md) Schritt 2 und 6 zieht die Boyz auch
einzeln (*Ebene* ein *Modell*); fehlt das Angebot, nachdem ein Boy gezogen wurde, kommt der
Spieler nicht zum Ausgangspunkt zurück. Ebenso dürfte die Einheit *vorrücken*, von der nur
ein Boy in *Nahkampfreichweite* steht (`core_rules.txt:724`). Je ein Test, etwa 15 Zeilen,
ohne neuen Vertrag.

**Gegenvorschlag.**
1. BEW-24.1: Boyz mit `letztesModellZurEbeneMachen`, nur dieses *Modell* 2″ ziehen, die
   übrigen stehen wie zu Beginn; dann bietet Arbiter „Einheit zurücksetzen“ an. Dazu 24.2
   aus demselben Stand: Nach dem Klick steht jedes *Modell* wie zu Beginn.
2. BEW-22.1: Ein Boy (nicht das erste *Modell* der Boyz) in *Nahkampfreichweite* eines Necron
   Warriors, die übrigen Boyz außerhalb; dann bietet Arbiter „Vorrücken“ nicht an. Die
   Helfer aus `schlacht.py` (`aufeinanderZuZiehen`, `anhaltenUndÜbergehen`) nach deinem Urteil.

**Stellungnahme.** Angenommen, beides umgesetzt.
1. [einheitZuruecksetzenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/einheitZuruecksetzenTest.py):
   Die Hilfe `nurDasLetzteModellZiehen` zieht mit `letztesModellZurEbeneMachen` nur das
   letzte *Modell* 2″ und prüft im Aufbau, dass die übrigen stehen wie zu Beginn. Darauf
   `testBew24_1IstNurEinModellDerEinheitGezogenBietetArbiterZurücksetzenAn` und
   `testBew24_2IstNurEinModellGezogenStehtNachDemZurücksetzenJedesModellWoEsZuBeginnStand`,
   je für Boyz und Necron Warriors (`einheitAmZug`).
2. [keinVorrueckenAusDerNahkampfreichweiteTest.py](../../technik/tests/akzeptanz/phasen/bewegung/keinVorrueckenAusDerNahkampfreichweiteTest.py):
   `testBew22_1IstNurEinModellInDerNahkampfreichweiteBietetArbiterVorrückenNichtAn`, mit
   jeder *Ebene*. Die Fixture `einBoyInDerNahkampfreichweite` zieht in drei *Schlachtrunden*
   die Boyz als Ganzes nach Osten und den Overlord auf die Höhe des zweiten Boys, in der
   vierten halten die Boyz an seiner *Nahkampfreichweite* an und gehen gemeinsam über. Der
   Aufbau prüft, dass nur der zweite Boy in *Nahkampfreichweite* ist. Abweichung: der Overlord
   statt eines Necron Warriors. Das Kriterium nennt jedes *Modell* des anderen *Spielers*, und
   ein einzeln gezogener Warrior ließe die Necron Warriors aus der *Kohärenz* fallen; dann
   sperrt „Phase beenden“ (BEW-4.1). `aufeinanderZuZiehen` passt nicht, weil es abwechselnd
   beide *Modelle* einzeln zieht.
