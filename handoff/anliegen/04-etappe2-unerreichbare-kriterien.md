# Etappe 2: zwei Kriterien ohne Gegenstück in der Etappe

04 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.**
1. „Die Schlacht endet ... mit einer vernichteten Armee“: In Etappe 2 kann kein Modell
   vernichtet werden, Verluste kommen erst mit dem Schießen in Etappe 3.
2. „Arbiter führt ... Befehlspunkte“: In Etappe 2 gibt es nichts, wofür Befehlspunkte
   ausgegeben werden; Stratagems kommen erst in Etappe 5.

**Kosten.** Beide Kriterien lassen sich in Etappe 2 nur mit einem künstlich hergestellten
Spielstand testen. Der Code dafür hat im Produkt keinen Aufrufer: Die Suche nach totem Code
(E37, vulture nur über den Produktcode) meldet ihn, oder er bleibt nur durch Tests am Leben,
wie `resolve_attack` im Altbestand (VORGEHEN.md, Werkzeugprobe). Später wird er gegen die echte
Verwendung umgebaut.

**Gegenvorschlag.**
1. „Ende mit vernichteter Armee“ nach Etappe 3, dort entstehen die Verluste.
2. Befehlspunkte in die Etappe des ersten Stratagems; ist das Command Re-roll mit eingegebenen
   Würfen gewünscht, passt Etappe 3, sonst Etappe 5.
3. Etappe 2 nennt die Mission, aus der die Aufstellungszonen kommen (Frage 4: Only War aus den
   Grundregeln, `core_rules.txt:2255`); sonst ist „in seiner Aufstellungszone“ ungeregelt.

**Stellungnahme.** Angenommen, umgesetzt: Etappe 2 nennt Only War; vernichtete Armee und Befehlspunkte mit
Command Re-roll stehen beim Schießen (Etappe 4, Frage an den Stakeholder). Nach demselben
Grund wandert Fall Back zu Charge und Nahkampf: Engagement Range entsteht erst durch den Charge.
