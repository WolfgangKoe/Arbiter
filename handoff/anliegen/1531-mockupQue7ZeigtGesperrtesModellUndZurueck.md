# Mockup que-7 zeigt ein gesperrtes Modell und „zurück“

1531 · Kritik · von Anforderungsautor → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die
Domänenphase, denn es ist ein Bild und kein Kriterium. Nach
[AUF-26](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md) entsteht kein
*gesperrtes* *Modell* mehr. AUF-9 und AUF-12.1 und die Glossarzeile *gesperrt* sind gelöscht
([1430](1430-restDesGesperrtenModellsInDenKriterien.md)). Der Code hat keinen Kreis `gesperrt`
und keinen Knopf „zurück“ mehr ([1443](1443-codeOhneGesperrtesModell.md), Punkt 5). Das
Mockup [que-7](../../domaene/mockups/que-7.html), auf das das Item
[ruhigeKarte](../../domaene/items/ruhigeKarte.md) verlinkt, zeigt beides trotzdem noch:
`<circle class="modell spieler1 gesperrt" …>` und in der `knopfGruppe` den Knopf „zurück“.
[vorschlag.css](../../domaene/mockups/vorschlag.css) hat dazu noch `.modell.gesperrt`.

**Kosten.** Wer QUE-7 nach dem Bild baut oder prüft, sieht einen Zustand, den es nicht mehr
gibt, und einen Knopf, den die Seite nicht mehr hat.

**Gegenvorschlag.** In que-7 den Kreis `gesperrt` und den Knopf „zurück“ entfernen. Was
QUE-7.1 zeigen soll, also eine *Karte*, die ruhig bleibt, während daneben ein *Grund*
erscheint, geht weiter mit `sperrmeldung` und „Aufstellen der Einheit beenden“.
`.modell.gesperrt` aus `vorschlag.css` entfernen, wenn kein anderes Mockup es nutzt. Auch
QUE-7.1 nennt „zurück“ als Beispiel. Das ist mein Artefakt, ich streiche es in derselben
Domänenphase.
Erledigt, wenn `grep -rn "gesperrt\|zurück" domaene/mockups/que-7.html` und
`grep -n "gesperrt" domaene/mockups/vorschlag.css` nichts finden.

**Stellungnahme.**
Umgesetzt: In `que-7.html` sind der Kreis `gesperrt` und der Knopf „zurück“ entfernt, in
`vorschlag.css` ist `.modell.gesperrt` entfernt; `grep -rn gesperrt domaene/mockups` findet
nichts. QUE-7.1 nennt „zurück“ noch; das streicht der Anforderungsautor.

Nachprüfung (Anforderungsautor): Beide grep finden nichts, erledigt. QUE-7.1 bleibt, wie es
ist; mein Satz oben, ich striche „zurück“, war falsch: Der Knopf kommt mit AUF-13.1 nach einer
*Sperre* nach AUF-10.3 wieder ([gesperrtesBeenden](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md),
[V7](../../technik/architektur/handlungen.md), Plan 6: „bis AUF-13.1 (Plan 7)“) und erscheint
dann neben der *Karte*, wie QUE-7.1 sagt.
