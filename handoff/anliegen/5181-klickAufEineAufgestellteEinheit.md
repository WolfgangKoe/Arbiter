# Klick auf ein Modell einer aufgestellten Einheit in der Aufstellung

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 2/3
Status: angenommen

## Runde 1
**Befund.** Wartet (Ich 3: Randfall abseits des Happy Path). In der *Aufstellung* klickt
jemand ein *Modell* einer schon *aufgestellten* *Einheit* an. AUF-20.6 sagt: Sie ist danach
*ausgewählt*. AUF-5.10 sagt: Wird eine *Einheit* *aufgestellt*, ist sie nicht mehr
*ausgewählt*; nach dem [Vertrag, V3](../../technik/architektur/vertrag/aufstellen.md) prüft die
*Aufstellung* vor dem Auswählen, dass die *Einheit* nicht *aufgestellt* ist. Kein Test prüft
den Fall; der Klick auf ein *Modell* der *Einheit in Aufstellung* läuft.

**Kosten.** Bleibt es offen, entscheidet der Code nebenbei, und am Bildschirm kann es mal so,
mal so aussehen. Beide Antworten sind wenige Zeilen und ein Test.

**F1 · Wählt der Klick eine aufgestellte Einheit aus?** A: Nein, es geschieht nichts
(AUF-5.10, V3). B: Ja, die *Karte* kennzeichnet ihre
*Modelle*; ziehen lässt sie sich weiter nicht (AUF-20.6 wörtlich, AUF-16.8). Empfehlung: A.
Eine *aufgestellte* *Einheit* kann man in der *Aufstellung* nicht mehr bewegen, die
Kennzeichnung brächte nichts. Bei A ergänzt der Anforderungsautor AUF-20.6 um „nicht
*aufgestellt*“.
Annahme: A, der Klick ändert nichts.
Antwort: Die Antwort hierauf ist obsulet.

**Gegenvorschlag.** Beantworte F1 in der Domänenphase 9; „.“ heißt, die Empfehlung gilt.

**Stellungnahme.**
Kommentar: An sich stimme ich dir zu. Es sollte im Zweifelsfall möglich sein, eine bereits aufgestellte Einheit zu verschieben, damit die neu aufzustellende Einheit ggf. Platz hat. Dazu muss es möglich sein, die betreffende bereits aufgestellte Einheit auszuwählen und zu verschieben. Ein Zurücklegen dieser bereits aufgestellten Einheit sollte dagegen nicht möglich sein. Ist das abbildbar?

## Runde 2
**Befund.** Zu deinem Kommentar: Ja, das lässt sich abbilden, und *zurücklegen* bleibt
ausgeschlossen, das ist schon so: „Einheit zurücklegen“ gibt es nur für die *Einheit in
Aufstellung* (AUF-23.4), und ein *Modell* einer *aufgestellten* *Einheit*, das jemand neben der
*Karte* loslässt, springt zurück (AUF-16.8). Der Regeltext kennt kein Umstellen: Die *Spieler*
stellen abwechselnd *Einheiten* auf, bis alle stehen oder kein Platz mehr ist
(`core_rules.txt:2322`). Verschieben ist also ein Regelbruch, und dafür hat das
[Ziel](../../domaene/ziel.md) schon einen Weg: Arbiter sperrt, die *Spieler* können die *Sperre*
*gemeinsam übergehen*, das *Protokoll* hält es fest (QUE-5). Heute sperrt Arbiter das Ziehen mit
‚nicht wählbar‘ und bietet das Übergehen dort nicht an (AUF-7.2, 12.6). ArbiterMap ließ frei
verschieben, nur die eigene Zone hielt die *Modelle*, ausdrücklich „keine Regelfolge“
(`ArbiterMap/docs/spec/interaction_map.md:684`).

**Kosten.** B ändert jetzt nichts: AUF-20.6 gilt wie geschrieben. Das Übergehen beim
Verschieben kostet später zwei, drei Kriterien mit Tests (AUF-12.6 und 21.1 erweitern) und
setzt QUE-5 voraus. Ich schlage Etappe 7 vor, zu den Randfällen des Aufstellens: Erst kommen die
wesentlichen Funktionen entlang der Phasen (Absicht 3), und für Orks gegen Necrons ist Platz in
der Zone kein Engpass. In Etappe 2 vorgezogen ist es ein Item mehr in Plan 9. C kostet am
wenigsten Code, aber das *Protokoll* verliert die Spur, und AUF-7.2 fällt.

**Gegenvorschlag.** F2 ersetzt F1; die Zeile `Antwort` unter F1 gilt nicht mehr. Nach deiner
Antwort schreibe ich dem Anforderungsautor ein Anliegen mit den Änderungen an AUF-12 und AUF-21.

**F2 · Was kann man in der Aufstellung mit einer aufgestellten Einheit tun?**
A: Nichts; ein Klick auf ihr *Modell* ändert nichts, sie bleibt, wo sie steht, ohne Übergehen
(Regeltext, AUF-12.6).
B: Ein Klick wählt sie aus, die *Karte* kennzeichnet ihre *Modelle*. Ziehen sperrt ‚nicht
wählbar‘; die *Spieler* können *gemeinsam übergehen*, dann steht sie, wo losgelassen, die
eigene *Aufstellungszone* hält sie fest (AUF-26), und das *Protokoll* nennt es. Zurücklegen geht
nicht (Ziel, AUF-20.6, AUF-23.4).
C: Ein Klick wählt sie aus, Ziehen verschiebt sie ohne *Sperre*, die eigene *Aufstellungszone*
hält sie fest (ArbiterMap).
Empfehlung: B. Regelkonform von sich aus, dein Fall geht trotzdem, und jeder sieht im
*Protokoll*, dass umgestellt wurde. Ein einzeln gezogenes *Modell*, nach dem die *Einheit* nicht
in *Kohärenz* ist, springt zurück; ‚keine Kohärenz‘ ist nie zu übergehen (QUE-5.5).
Annahme: B; bis Etappe 7 wählt der Klick sie aus, Ziehen bleibt gesperrt ohne Übergehen.
Antwort: B

**Stellungnahme.**
