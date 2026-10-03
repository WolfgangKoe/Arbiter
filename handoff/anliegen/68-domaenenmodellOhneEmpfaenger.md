# Retro 1, Befund 8: Das Domänenmodell hat keinen Empfänger

68 · Kritik · von Fachkritiker (Domäne) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** [31](31-kritikDesEntwicklersFuerRetro1.md), Gegenvorschlag 4: „Domänenmodell:
Anliegen an den Anforderungsautor, sobald ein Befund es zeigt.“ Die Stellungnahme sagt, er
„zeigt sich an 43, 58, 63 und liegt bei der Domäne“; [Retro 1](../retro.md), Befund 8,
wiederholt das. Ein Anliegen an den Anforderungsautor gibt es nicht, 31 steht auf
`angenommen`. Nach der Regel, die die Retro selbst einführt
([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)), stünde dort „wartet auf <nr>“. Offen ist
die Frage aus 31: ein Domänenmodell „über das Glossar hinaus (Beziehungen,
Verantwortlichkeiten)“. In 58 trug das Glossar die Beziehung (*Aufstellungszone* →
*Aufstellungskarte* → *Mission*); ob das als Regel reicht, hat niemand entschieden.

**Kosten.** Prüft der Stakeholder 31 nach und setzt `erledigt`, löscht `erledigteLoeschen.py`
die Datei und Punkt 4 steht nur noch in git. Mit 64 und den nächsten Etappen kommen weitere
Objekte (*Spielfeld*, *Spielfeldkante*, Armeen der Ausgangslage); fehlt ein Ort für ihre
Beziehungen, erfindet der Code sie wie `nord`/`süd` (43 → 58 → 63: vier Anliegen, zwei Runden
beim Stakeholder).

**Gegenvorschlag.** Eins von beiden, in der Retro unter „Geändert“:
A: Du schreibst das Anliegen an den Anforderungsautor mit der Frage aus 31 und dem Befund aus
43, 58, 63; 31 endet mit „wartet auf <nr>“.
B: Die Retro hält fest, dass Beziehungen in der Definition im Glossar stehen (wie in 58) und
Punkt 4 damit geschlossen ist; dann braucht es die Zustimmung des Stakeholders als Frage in 65.

**Stellungnahme.**
