# Startet Arbiter immer unter derselben Adresse?

1650 · Fragen · von Architekt → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Deine Frage: „Wäre es möglich, dass die App immer unter derselben Browseradresse
startet?“ Ja, das geht mit wenig Aufwand. Heute sucht sich Arbiter bei jedem Start eine freie
Nummer hinter dem Doppelpunkt, etwa `http://127.0.0.1:41873/`, und nennt sie in der ersten
Zeile ([W5](../../technik/architektur/web.md)). Ein Lesezeichen gilt deshalb nur bis zum
nächsten Start. Mit fester Nummer hieße es immer etwa `http://127.0.0.1:8040/`.

Was sich ändert:
1. **Die Nummer ist schon belegt.** Ein zweiter Start findet die Nummer belegt, wenn Arbiter
   schon läuft oder ein anderes Programm sie nutzt. Arbiter bricht dann ab und schreibt, was
   los ist: „Die Adresse … ist belegt. Läuft Arbiter schon? Dann spielt dort weiter oder beendet
   das andere Fenster mit Strg+C.“ Ein Ausweichen auf eine andere Nummer wäre gefährlich: Euer
   Lesezeichen zeigte dann still auf die alte Partie.
2. **Nach einem Neustart.** Ein Tab, der vom letzten Start noch offen ist, spricht mit der neuen,
   leeren Partie. Er zeigt den alten Stand, bis ihr die Seite neu ladet (F5). Heute antwortet
   dort gar nichts mehr. Sofort nach Strg+C neu starten geht weiterhin.
3. **Tests.** Die Bildschirmtests starten Arbiter selbst und nehmen weiter eine freie Nummer. Sonst
   stießen sie mit deiner laufenden Partie zusammen, und zwei Rollen, die gleichzeitig testen,
   auch untereinander. Der Befehl bekommt dafür eine Angabe der Nummer, die der Test nutzt. Die
   feste Adresse prüft ein Test, ohne sie zu belegen.

**Kosten.** Klein, weniger als ein halbes Item: Die Nummer kommt als Angabe in den Server, der
Befehl bekommt eine feste Nummer und eine Meldung für den Fall einer belegten Nummer, dazu W5
und etwa drei Tests. Zuerst schreibt der Anforderungsautor die Anforderung QUE-2.1 um („immer
dieselbe Adresse“, belegte Nummer). Das gehört in die nächste Domänenphase, danach baut es die
Technikphase.

**Gegenvorschlag.**

**F1 · Soll Arbiter immer unter derselben Adresse starten?** Empfehlung: ja, unter
`http://127.0.0.1:8040/`. Gängige Programme für Entwickler belegen diese Nummer selten, anders
als 5000, 8000 oder 8080. Die genaue Zahl ist frei wählbar, nenne gern eine andere.
Antwort: .

**F2 · Was geschieht, wenn die Nummer belegt ist?** Empfehlung: abbrechen mit der Meldung aus
Punkt 1, nicht ausweichen.
Antwort: .

**Stellungnahme.**
Kommentar: Ich folge deinen Empfehlungen
Stellungnahme: Weitergeführt in 1653 (QUE-2.1, Domänenphase) und 1654 (Item, danach Technikphase).
