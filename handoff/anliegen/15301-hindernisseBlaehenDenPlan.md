# Hindernisse blähen den Plan auf

Form: Kritik
Von: Planer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen
Wartet auf: Prozessphase

## Runde 1
**Befund.** [plan.md](../plan.md) hat 52.207 Zeichen. Davon sind 3.967 der Plan selbst,
innerhalb der 4.000; 48.240 sind `## Fortschritt`, der nach
[Fortschritt](../../prozess/ablauf/fortschritt.md) nicht zum Höchstmaß zählt. Davon sind
40.846 die 45 Zeilen `Hindernis:`; 11 haben über 1.000 Zeichen, die längste 3.597. Der Grund:
`prozess/pruefungen/standregeln/abhaken.py:102` schreibt jeden grünen Testnamen in den Satz
(„Diese Tests sind grün, bevor der Code besteht: …“), obwohl den Satz nach
[Fortschritt](../../prozess/ablauf/fortschritt.md) die Rolle für den Stakeholder schreibt
([Wir 5](../../prozess/praemissen/wir.md)). Die Liste steht schon im Anliegen, auf das die
Zeile verweist. Dazu bleiben beseitigte Hindernisse stehen ([Wir 4](../../prozess/praemissen/wir.md)).
Das betrifft Auftrag 12520 (Hindernisse als eigene Datei), dort ohne die Ursache.

**Kosten.** Du liest im Plan und im Dashboard rund 45.000 Zeichen, die du für die Freigabe
nicht brauchst; jede Rolle, die den Plan liest, zahlt sie in Token ([Absicht 6](../../prozess/praemissen/absicht.md)).
Ohne Änderung wächst es mit jedem Item.

**Gegenvorschlag.** In der Prozessphase zusammen mit 12520: Der Satz der Zeile `Hindernis:`
nennt die Anzahl der grünen Tests („23 Tests sind grün, bevor der Code besteht“), die Namen
stehen nur im Anliegen; ein beseitigtes Hindernis kürzt das Skript auf seine Nummer.

**Stellungnahme.** Zugestimmt, mit 12520 als P2 der [Retro 10](../retro.md): Die Zeile nennt
nur Nummer und Titel, Testnamen stehen im Anliegen. `angenommen`, sobald die Regel steht.

Umgesetzt mit P2 der [Retro 10](../retro.md), `erledigt` folgt dessen Haken: Die Zeile ist
`- [ ] Hindernis <nr> <Titel>`, ohne Testnamen und ohne Anzahl; die Namen stehen nur im
Anliegen, das Abhaken liest sie dort. Ein beseitigtes Hindernis bleibt als abgehakte Zeile
dieser Länge stehen, statt auf die Nummer gekürzt zu werden. Regel:
[Standregeln](../../prozess/regeln/standregeln.md), Zeile Anliegen 490 Teil 2; Ablauf:
[Fortschritt](../../prozess/ablauf/fortschritt.md).
