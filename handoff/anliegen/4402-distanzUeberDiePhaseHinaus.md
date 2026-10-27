# Distanz zählt über die Bewegungsphase hinaus

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: eine *Sperre* greift zu Unrecht). Die *Distanz* zählt „in der
laufenden *Normalen Bewegung*“ ([Glossar](../../domaene/glossar.md)); sie endet nur mit
*Bewegung der Einheit beenden* (BEW-1.3). „Phase beenden“ (QUE-10.2, 10.3) beendet sie
nicht. Plan 8 geht fünf *Schlachtrunden*: Zieht ein Spieler in Runde 1 eine *Einheit* 4″
und klickt „Phase beenden“, ist sie in seiner nächsten *Bewegungsphase* noch die *Einheit
in Bewegung*; ihre *Distanz* läuft weiter, nach 2″ sperrt ‚weiter als B‘ (BEW-2.1), obwohl
die Regel je *Bewegungsphase* einen Zug erlaubt (`core_rules.txt:734`, `:745`). Offen ist
zudem, ob die *Normale Bewegung* endet, wenn eine andere eigene *Einheit* zur *Einheit in
Bewegung* wird (BEW-1.1); zieht man danach die erste wieder, muss der Testautor erfinden, ob
ihre *Distanz* neu beginnt.

**Kosten.** In Zyklus 8 sieht der Stakeholder beim Durchspielen eine falsche *Sperre*, sobald
er den Klick auf *Bewegung der Einheit beenden* einmal auslässt. Behebung: eine Zeile im
Glossar, ein Test mehr.

**Gegenvorschlag.** *Distanz* je *Bewegungsphase* statt je *Normaler Bewegung*: „Summe der
geraden Strecken zwischen den *Stellen*, an die ein *Modell* in der laufenden
*Bewegungsphase* nacheinander *gesetzt* wurde“ (`core_rules.txt:734`, „No unit can be
selected to move more than once in each Movement phase“; Vorbild Arbiter-old: Zustand einer
*Phase* endet mit ihr, `src/gameMechanic/gameState.py:756`, `:605`). Das klärt beide Fälle,
BEW-2.1 bleibt, wie es ist, und schließt nebenbei Punkt 2 aus
[4261](4261-lueckenImNormalMoveFuerSpaeter.md) für ‚weiter als B‘. Dass ‚keine Kohärenz‘
über „Phase beenden“ umgehbar ist, wartet weiter dort (4261, Punkt 1).

**Stellungnahme.** Angenommen wie vorgeschlagen. *Distanz* im
[Glossar](../../domaene/glossar.md) zählt jetzt in der laufenden *Bewegungsphase*
(`core_rules.txt:734`). Damit beginnt sie in jeder *Bewegungsphase* bei null, auch wenn die
*Einheit* aus der vorigen noch die *Einheit in Bewegung* ist. Zieht man in derselben
*Bewegungsphase* eine *Einheit* nach einer anderen erneut, zählt die *Distanz* ihrer
*Modelle* weiter; ‚weiter als B‘ greift dann regelgerecht. BEW-2.1 bleibt unverändert und
erhält keine neue Kennung, denn es hat noch keinen Test. Den Test über „Phase beenden“ schreibt der Testautor zu
BEW-2.1. Wie ‚keine Kohärenz‘ über „Phase beenden“ umgangen wird, bleibt in
[4261](4261-lueckenImNormalMoveFuerSpaeter.md), Punkt 1; ebenso, ob „Phase beenden“ die
*Einheit in Bewegung* beendet.
