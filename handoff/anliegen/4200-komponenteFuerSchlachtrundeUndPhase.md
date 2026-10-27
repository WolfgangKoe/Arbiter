# Komponente für Schlachtrunde und Phase fehlt

Form: Fragen
Von: Ux
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** QUE-10.1 verlangt, dass Arbiter Schlachtrunde, Spieler am Zug und Phase zeigt,
und die Schlacht-Ende-Anzeige nach QUE-10.4. Die Komponentenseite hat dafür nichts. Die
Mockups [que-9](../../domaene/mockups/que-9.html), [que-10](../../domaene/mockups/que-10.html),
[bew-1](../../domaene/mockups/bew-1.html) und [bew-2](../../domaene/mockups/bew-2.html)
setzen „Schlachtrunde 1 · Bewegungsphase“ in `kopfzeileAnDerReihe` unter den Namen des
Spielers am Zug; „Erster Zug“ und „Phase beenden“ sind `knopf` in `knopfGruppe`. „Schlacht
beendet“ ist nicht gezeichnet: Dafür gibt es keinen Platz in den vorhandenen Komponenten.
Die Mockups verlinken `komponenten.css`, nicht `vorschlag.css`.

**Kosten.** Ohne Antwort baut der Implementierer die Anzeige ohne Vorgabe, oder der Text
„an der Reihe“ aus AUF-Mockups verschwindet unbemerkt.

**Gegenvorschlag.** Die Wiederverwendung von `kopfzeileAnDerReihe` gilt für Runde und
Phase; für „Schlacht beendet“ entscheidet der Architekt (neue Klasse oder bestehende).

**Stellungnahme.** Entschieden (DoR 5), Aussehen wie bisher, aber zwei Namen sind neu.
1. Schlachtrunde und Phase stehen unter dem *Spieler* *am Zug*, wie du sie gezeichnet hast,
   aber mit eigenen Klassen: `kopfzeileSpieler amZug` und `<span class="kopfzeileAmZug">`.
   Grund: *an der Reihe* gilt nur in der *Aufstellung*, in der *Schlacht* heißt es *am Zug*
   (Glossar, [Wir 2](../../prozess/praemissen/wir.md)). Auch die Bildschirmtests finden das Feld
   über die Klasse (`bildschirm.py:98`); ein Test zu QUE-10.1 hieße sonst „an der Reihe“.
2. „Schlacht beendet“ (QUE-10.4) steht als zweite Zeile unter „ARBITER“ in der Mitte der
   Kopfzeile, wie das zentrierte „Battle Over“ in Arbiter-old (`gameHeader.py:342`, `:301`):
   `<div class="kopfzeileTitel">ARBITER<span class="kopfzeileSchlachtBeendet">Schlacht beendet</span></div>`.
   Kein *Spieler* ist dann *am Zug*, beide `kopfzeileSpieler` ohne `amZug`.

Regeln für `vorschlag.css`, wörtlich; sie ersetzen die beiden Regeln zu `anDerReihe` und
`.kopfzeileAnDerReihe` und ergänzen `.kopfzeileTitel`:
```css
.kopfzeileTitel {
  text-align: center;
}

.kopfzeileSpieler.anDerReihe,
.kopfzeileSpieler.amZug {
  border-bottom-color: var(--akzentHell);
}

.kopfzeileAnDerReihe,
.kopfzeileAmZug,
.kopfzeileSchlachtBeendet {
  display: block;
  color: var(--akzentHell);
  font-size: 0.75rem;
  font-weight: 400;
}
```
`text-align` gehört zur vorhandenen Regel `.kopfzeileTitel` (dort ergänzen, keine zweite).
Bitte in que-9 bis bew-2 `anDerReihe`/`kopfzeileAnDerReihe` durch `amZug`/`kopfzeileAmZug`
ersetzen und in que-10 einen Zustand nach QUE-10.4 mit `kopfzeileSchlachtBeendet` zeichnen.
„Erster Zug“ und „Phase beenden“ als `knopf` in `knopfGruppe`: passt (O5, eine Zeile in der
Tabelle der Knöpfe).
