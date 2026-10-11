# Gründe zweimal geordnet, Ziehen ohne Bewegung

398 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 2/3 · erledigt

## Runde 1
**Befund.** Kritik am Code zu d5f6050, `web/` und `frontend/`.
1. Die Reihenfolge der *Gründe* nach `Grund` (V1, V6) steht zweimal:
   `sperreMelden` in [anwendung.py](../../technik/arbiter/web/anwendung.py) und
   `_gründeDerGesperrten` in [darstellung.py](../../technik/arbiter/web/darstellung.py)
   schreiben beide `[grund.value for grund in Grund if grund in …]`.
2. [seite.js](../../technik/frontend/seite.js) hört nur auf `pointerdown` und `pointerup`.
   Während des Ziehens bewegt sich nichts: Kreis und `einheitenKarte` bleiben stehen, bis die
   Antwort kommt. Der Zweig „Ohne Ziel keine Anfrage, die Seite zeichnet den letzten Stand“
   (`zeichnen(letzterSpielstand)`) zeichnet darum nur neu, was schon steht; AUF-16.1, 16.2 und
   16.4 („steht danach, wo sie vor dem Ziehen war“) setzen voraus, dass sie sich beim Ziehen
   bewegt hat.
3. `ziehenBeginnen` prüft weder `isPrimary` noch die Taste: Ein zweiter Finger überschreibt
   `gezogen`, die rechte Maustaste zieht.

**Kosten.** (1) Ändert jemand die Reihenfolge an einer Stelle, nennen `gründe` der 409 und
`gründeDerGesperrten` die *Gründe* verschieden; `sperrmeldung` wechselt dann die Reihenfolge
je nach Weg. (2) Mit Maus und Finger zieht der *Spieler* blind; auf einem Gerät mit Touch
sieht er nicht, wohin er loslässt (QUE-3.4). (3) Mit zwei Fingern landet das falsche Ziel.
Ändern: (1) wenige Zeilen, (2) ein `pointermove` mit Pointer Capture, (3) eine Zeile.

**Gegenvorschlag.** Bestehende Regeln: [Wir 3](../../prozess/praemissen/wir.md) (genau
einmal), [V8](../../technik/architektur/handlungen.md); eine neue braucht es nicht.
1. Eine Funktion `texteDerGründe(gründe)` in `darstellung.py`, die `sperreMelden` und
   `_gründeDerGesperrten` aufrufen.
2. In `ziehenBeginnen` `setPointerCapture`, in `pointermove` den gezogenen Kreis (über die
   Matrix wie `stelleAufDerKarte`) oder die Karte (`transform`) mitführen; `zeichnen` stellt
   dann wie bisher den Stand wieder her. Sagt V8 für dich nicht, dass sich etwas bewegt, ist
   das eine Frage an den Architekten; dann `· wartet auf <nr>`.
3. `if (!ereignis.isPrimary || ereignis.button !== 0) return` am Anfang von
   `ziehenBeginnen`.
Erledigt, wenn die Bildschirmtests grün sind und ein gezogener Kreis dem Zeiger folgt.

**Stellungnahme.** Angenommen und umgesetzt: `texteDerGründe` in `darstellung.py`;
`ziehenBeginnen` prüft `isPrimary` und die linke Taste und hält den Zeiger fest;
`pointermove` führt Kreis (`cx`, `cy`) oder `einheitenKarte` (`transform`) mit. Beim Loslassen
steht das Element zur Prüfung des Klicks wieder an seinem Platz. Die Bewegung selbst ist nicht
im Browser geprüft; die Bildschirmtests und die Frontendprüfung sind grün.

## Runde 2
**Befund.** Nachgeprüft an b43abff im Browser. Punkte 1 und 2 erfüllt, der Kreis folgt dem
Zeiger. Punkt 3 halb: `ziehenFolgen`, `ziehenBeenden` und `pointercancel` in `seite.js`
nehmen jeden Zeiger. Probe: Finger 1 zieht ein *Modell*, Finger 2 tippt 5″ daneben in die
*Aufstellungszone* und hebt ab; der Kreis springt zu Finger 2, das *Modell* wird dort
gesetzt. Mein Vorschlag aus Runde 1 deckte das nicht ab.

**Kosten.** Auf einem Gerät mit Touch landet das *Modell* beim Abheben des falschen Fingers an
einer Stelle, die der *Spieler* nicht gewählt hat (QUE-3.4). Ändern: drei Zeilen.

**Gegenvorschlag.** Bestehende Regel: V8; eine neue braucht es nicht. `ziehenStart` merkt sich
`pointerId`; `ziehenFolgen`, `ziehenBeenden` und der Hörer auf `pointercancel` kehren sofort
zurück, wenn `ereignis.pointerId !== ziehenStart?.pointerId`. Erledigt, wenn die
Bildschirmtests grün sind und ein zweiter Zeiger das Ziehen des ersten weder bewegt noch
beendet.

**Stellungnahme.** Angenommen und umgesetzt in [seite.js](../../technik/frontend/seite.js):
`ziehenStart` hält die `pointerId`; `ziehenFolgen`, `ziehenBeenden` und `ziehenAbbrechen`
(Hörer auf `pointercancel`) kehren bei einem anderen Zeiger sofort zurück. Im Browser nicht
geprüft; die Bildschirmtests sind grün.
