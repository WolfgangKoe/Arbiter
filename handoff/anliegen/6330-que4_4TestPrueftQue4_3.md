# Test zu QUE-4.4 in der Schlacht prüft QUE-4.3

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: ein Test prüft sein Kriterium nicht). `testQue4_4DieSchlachtNenntEineEinheitMitEinemWeitEntferntenModellNichtInKohärenz` ([kohaerenzTest.py](../../technik/tests/akzeptanz/querschnitt/kohaerenzTest.py)) zieht das letzte der zehn *Modelle* der Boyz 5″ weg. Dieses *Modell* hat dann zu keinem anderen einen *Abstand* von höchstens 2″; das ist schon [QUE-4.3](../../domaene/anforderungen/querschnitt/kohaerenz.md) (sechs oder mehr, eines mit weniger als zwei). Eine *Schlacht*, die QUE-4.4 (zwei Gruppen, in denen jedes *Modell* Nachbarn hat) nicht kennt, besteht den Test. Er wiederholt außerdem wörtlich Aufbau und Prüfung von `testBew1_5FehlendeKohärenzSperrtBeimLoslassenNicht` ([normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py)) und fängt keinen Mutanten, den jener oder `testQue4_5DieSchlachtNenntEineEinheitInReiheInKohärenz` nicht schon fängt (`schlachtrunden.py:112`, Rückgabe `None`: `not None` ist wahr).

Die übrigen Tests aus 6291 treffen ihr Kriterium: BEW-1.5 (Loslassen an der eigenen *Stelle*), BEW-3.1 (ein Hauch über die *Bewegungsweite*; schon an der *Bewegungsweite* bleibt das *Modell* stehen), BEW-2.5 (schräg; nachgeprüft: ohne die fremde *Base* bei (3, 2) geht derselbe Zug ohne *Sperre*, die *Sperre* kommt also aus der Mitte der Strecke), QUE-4.5 in der *Schlacht*.

**Kosten.** QUE-4.4 gilt in der *Schlacht* als belegt, ohne dass ein Test dort die Zwei-Gruppen-Regel verlangt; ein grüner Test, der nichts Eigenes prüft (Absicht 1).

**Gegenvorschlag.** Den Test streichen; QUE-4.4 ist in der *Aufstellung* belegt (`testQue4_4ZweiGruppenOhneModellImAbstandVonZweiZoll…`), die *Schlacht* rechnet nach derselben Regel. Oder ihn so aufbauen, dass nur QUE-4.4 greift (zwei Gruppen zu je fünf Boyz, jede in sich in *Kohärenz*, mehr als 2″ auseinander).

**Stellungnahme.** Angenommen, zweiter Weg des Gegenvorschlags. Der Test heißt jetzt `testQue4_4DieSchlachtNenntEineEinheitInZweiGruppenNichtInKohärenz` ([kohaerenzTest.py](../../technik/tests/akzeptanz/querschnitt/kohaerenzTest.py)): Die letzten fünf der zehn *Modelle* der Boyz gehen je 5″ nach Osten, das letzte zuerst, damit keines auf ein noch nicht bewegtes *Modell* trifft. Es bleiben zwei Gruppen zu je fünf *Modellen*, jede in sich in Reihe, mehr als 2″ auseinander; nur QUE-4.4 greift, QUE-4.3 nicht. Grün, `konfigurationTest.py` und `spiegelTest.py` grün.
