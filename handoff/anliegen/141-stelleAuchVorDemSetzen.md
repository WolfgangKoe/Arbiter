# Stelle auch vor dem Setzen

141 · Kritik · von Fachkritiker (Domäne) → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Das [Glossar](../../domaene/glossar.md) (Zeile *Stelle*) sagt: „Ort eines
*gesetzten* *Modells* auf dem *Spielfeld*: der Mittelpunkt seiner runden *Base*.“ Die Kriterien
und das Gebaute nutzen die *Stelle* aber auch für ein *Modell*, das dort noch nicht *gesetzt*
ist:
- QUE-1.2, AUF-3.2 und AUF-3.4 prüfen die *Base* „an der *Stelle*“, bevor das *Modell* dort
  *gesetzt* ist; AUF-3 (Zweck) sperrt „jede *Stelle*“, also gerade eine, an der danach kein
  *Modell* steht.
- `Aufstellung.modellSetzen(modell, stelle)` nimmt jede `Stelle` an, auch eine mit Mittelpunkt
  außerhalb des *Spielfelds*, und sperrt sie dann mit ‚nicht ganz in der Zone‘.
Die Abnahme der Items aus Plan 2 hängt nicht daran; DoD 3 („die Anforderung beschreibt das
gebaute Verhalten“) ist hier nur im Glossar ungenau.

**Kosten.** Gering, eine Zeile. Mit Ablage, Ziehen und „Beim Loslassen“ (Etappe 1) ist die
*Stelle* gerade der Ort, an den ein *Modell* erst kommen soll; wer dann wörtlich nach dem
Glossar baut, gibt einem ungesetzten *Modell* keine *Stelle* oder lässt nur *Stellen* auf dem
*Spielfeld* zu.

**Gegenvorschlag.** Die Zeile *Stelle* lautet etwa: „Ort, an den ein *Modell* *gesetzt* wird
oder an dem es *gesetzt* ist: der Mittelpunkt seiner runden *Base*.“ Ob eine *Stelle* außerhalb
des *Spielfelds* liegen darf, entscheidest du; das Gebaute lässt das zu und sperrt dann nach
AUF-3.2. Erledigt, wenn das Glossar die *Stelle* vor dem *Setzen* einschließt.

**Stellungnahme.** Angenommen. Die Zeile *Stelle* im [Glossar](../../domaene/glossar.md) lautet
jetzt: „Ort, an den ein *Modell* *gesetzt* werden soll oder an dem es *gesetzt* ist: der
Mittelpunkt seiner runden *Base*. Auch außerhalb des *Spielfelds*; ob dort *gesetzt* werden
darf, sagen die Kriterien.“ „werden soll“ statt „wird“, weil an einer gesperrten *Stelle* kein
*Modell* *gesetzt* wird. Eine *Stelle* außerhalb des *Spielfelds* bleibt erlaubt: In der
*Aufstellung* sperrt sie AUF-3.2, denn die *Aufstellungszone* ist Fläche des *Spielfelds*
(`core_rules.txt:2182`); so beschreibt das Glossar das Gebaute. Kriterien ändern sich nicht.
