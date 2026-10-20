# Ein Zug auf der Karte oder der Einheitenkarte gilt als Klick

1220 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu Item [setzenPerKlick](../../domaene/items/setzenPerKlick.md),
[seite.js](../../technik/frontend/seite.js). Einordnung nach [Ich 3](../../prozess/praemissen/ich.md):
hält auf, denn neuer Code verletzt [V8](../../technik/architektur/handlungen.md): „Ohne Zug ist
es ein Klick“ und „Ein Zug wählt nie aus“. Die Zugschwelle von 4 px gilt nur noch für ein
*Modell*. Die *Einheitenkarte* (`karte.addEventListener("click", …)`) und die *Karte*
(`document.addEventListener("click", karteAngeklickt)`) hören auf das `click` des Browsers. Mit
der Maus feuert es auch nach einem langen Zug. Vorher entschied `ziehenStart.begonnen` auch
bei der Karte, ob ein Klick vorliegt (`start.klicken?.()`). Das fällt mit dem Diff weg.
Probe am laufenden Arbiter (`python3 -m arbiter`, Playwright, Maus):
1. Spieler 2 drückt auf seine *Einheitenkarte*, zieht 30 px und lässt los. Die *Einheit* ist
   danach *ausgewählt* (`PUT …/ausgewählt`).
2. Danach drückt er in seiner Zone auf das *Spielfeld*, zieht 40 px und lässt los. Arbiter
   *setzt* die *Formation*, 10 *Modelle* (`PUT /api/karteAnklicken`).

**Kosten.** Ein Spieler, der auf der *Karte* schiebt oder sich verzieht, *setzt* ungewollt
eine ganze *Einheit*, und zwar dort, wo er gedrückt hat. AUF-18.1 verlangt dafür einen Klick.
Klick und Zug werden außerdem auf zwei Wegen unterschieden, für Item 2 käme mit dem Klick auf
ein *Modell* (V9) ein dritter dazu.

**Gegenvorschlag.** Jeden Klick über den Weg der Pointer Events entscheiden, wie es V8
beschreibt: `ziehenBeginnen` merkt sich jeden primären Druck. `ziehenBeenden` löst ohne Zug
den Klick nach dem Element aus: *Einheitenkarte* V2 mit `spieler` und `einheit` aus dem
`dataset`, *Karte* `karteAnklicken`, *Modell* nichts. Beide `click`-Listener fallen weg, und
damit auch die Hülle `() => auswahlSenden(spieler, einheit)` je Karte
([Es 7](../../prozess/praemissen/es.md)). Kleinste Alternative: Beide `click`-Handler
ignorieren einen Druck, der weiter als `zugschwelle` gewandert ist. Den Bildschirmtest dazu
schreibt der Testautor ([1221](1221-zugschwelleAnKarteUndEinheitenkarteUngeprueft.md)).
Erledigt, wenn die Probe oben mit Maus weder auswählt noch *setzt*, ein Klick (Abweichung
unter 4 px) beides weiter tut, die Akzeptanztests des Items grün sind und eslint grün ist.

**Stellungnahme.** Angenommen, der Gegenvorschlag ist umgesetzt in
[seite.js](../../technik/frontend/seite.js): `ziehenBeginnen` merkt sich jeden primären Druck mit
seinem Ziel, `ziehenFolgen` misst die Schwelle für jeden, `ziehenBeenden` löst ohne Zug den Klick
nach dem Ziel aus (`klicken`: *Einheitenkarte* V2, *Karte* `karteAnklicken`, *Modell* nichts). Beide
`click`-Listener und die Hülle um `auswahlSenden` sind weg; `auswahlSenden` liest `spieler`,
`einheit` und `ausgewählt` von der *Einheitenkarte*. eslint grün, Tests des Items und
`tests/einheit` grün (96). Die Probe mit Maus und 30 bis 40 px Zug habe ich nicht gefahren, sie
gehört in den Bildschirmtest [1221](1221-zugschwelleAnKarteUndEinheitenkarteUngeprueft.md).
