# Item für die feste Adresse

1654 · Kritik · von Architekt → Planer · Runde 1/3 · offen · wartet auf 1653

## Runde 1
**Befund.** Der Stakeholder hat in 1650 entschieden: Arbiter startet immer unter
`http://127.0.0.1:8040/`. Ist die Nummer belegt, bricht Arbiter mit einer Meldung ab. Die
Anforderung schreibt der Anforderungsautor in [1653](1653-que21ImmerDieselbeAdresse.md). Ein
Item dafür fehlt noch.

**Kosten.** Klein, weniger als ein halbes Item: Der Server bekommt die Nummer als Angabe, der
Befehl eine feste Nummer, eine Angabe für Tests und die Meldung für eine belegte Nummer. Dazu
kommen W5 und etwa drei Tests. Es passt neben ein fachliches Item in einen Zyklus. Ohne Item
bleibt die Entscheidung liegen.

**Gegenvorschlag.** Ein Item zu den Kriterien aus 1653, im nächsten Plan, sobald 1653 erledigt
ist. Technisch zu beachten, damit Testautor und Implementierer nicht raten:
1. Die Bildschirmtests starten den Server weiter selbst mit einer freien Nummer. Sonst stoßen
   sie mit einer laufenden Partie des Stakeholders zusammen oder mit Rollen, die gleichzeitig
   testen.
2. Der Akzeptanztest zu QUE-2.1 prüft die feste Adresse, ohne die Nummer 8040 zu belegen.
   Den Fall „belegt“ prüft er mit einer Nummer, die der Test selbst belegt.
3. W5 in [web.md](../../technik/architektur/web.md) ziehe ich in der Technikphase vor den Tests
   nach.

**Stellungnahme.**
