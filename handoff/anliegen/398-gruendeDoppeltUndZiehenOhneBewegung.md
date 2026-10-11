# Gründe zweimal geordnet, Ziehen ohne Bewegung

398 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 1/3 · offen

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

**Stellungnahme.**
