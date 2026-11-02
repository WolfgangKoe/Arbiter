# BEW-23: Kohärenz nach dem Übergehen und die Zeile unter dem Grund

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [BEW-23](../../domaene/anforderungen/phasen/bewegung/sperreNichtAmZug.md) ist
klein und baut auf Vorhandenem; zwei Punkte, bevor der Planer es einplant (Lücken abseits des
Happy Path, darum wartend; BEW-23 steht in keinem Plan):
1. Ein Weg an ‚keine Kohärenz‘ vorbei. BEW-23.2 lässt die *Spieler* ein *Modell* des anderen
   *Spielers* ziehen. [BEW-4.1](../../domaene/anforderungen/phasen/bewegung/beenden.md) sperrt
   „Phase beenden“ aber nur, wenn eine *Einheit* des *Spielers* *am Zug* nicht in *Kohärenz*
   ist. Beispiel: Spieler 1 ist *am Zug*, ihr übergeht ‚nicht am Zug‘ und zieht einen
   Necron Warrior 6" von seiner *Einheit* weg; „Phase beenden“ geht durch. Damit übergeht ihr
   ‚keine Kohärenz‘ mittelbar, was das Ziel und QUE-5.5 ausschließen
   (`core_rules.txt:730`, `:434`).
2. Nicht prüfbar: „wie AUF-22.1“ in BEW-23.1. Das Eigene an
   [AUF-22.1](../../domaene/anforderungen/phasen/aufstellen/ausserDerReihe.md) ist die Zeile
   unter dem *Grund* („Spieler 1 ist an der Reihe“). Ob BEW-23.1 eine Zeile „Spieler 1 ist am
   Zug“ verlangt, kann der Testautor nicht entscheiden; er prüfte sie oder nicht und
   erfände so das eine oder das andere.

**Kosten.** Gering, und keine neue Komponente: *Sperre* mit „gemeinsam übergehen“ gibt es in
der *Bewegungsphase* schon (Antwort 409 mit `übergehbar`, Knopf im Frontend). Der Code braucht
einen *Grund* mehr in `technik/arbiter/domaene/sperre.py`, und
`Schlachtrunden._stellenMitGründen` sperrt beim fremden *Modell*, statt leer zurückzugeben;
nach dem Übergehen rechnet es mit dem *Spieler* der *Einheit*. Das *Protokoll* trägt heute
den *Spieler* *am Zug* ein; QUE-5.1 verlangt den der *Einheit*, das zieht BEW-23 in der
Technikphase mit. Die drei Tests in `fremdeModelleTest.py` (BEW-10.1) fallen weg. Zu 1:
BEW-4.1 auf beide *Spieler* auszudehnen kostet einen Aufruf mit allen *Einheiten* statt
denen des *Spielers* *am Zug*. Bleibt 1 offen, stehen nach einem Übergehen *Einheiten* ohne
*Kohärenz* auf der *Karte*; bleibt 2 offen, entscheidet der Testautor an deiner Stelle.

**Gegenvorschlag.** 1: ein Kriterium, nach dem „Phase beenden“ auch sperrt, wenn eine
*Einheit* des anderen *Spielers* nicht in *Kohärenz* ist (Ziel, QUE-5.5). In Etappe 2 steht
sie nur nach BEW-23.2 außerhalb, denn die *Aufstellung* sperrt ‚keine Kohärenz‘ ohne
Übergehen. 2: „wie AUF-22.1“ ersetzen durch, was gleich sein soll: entweder die Zeile
„Spieler 1 ist am Zug“ oder „Spieler 2 ist am Zug“ als eigenes Kriterium oder ausdrücklich
nur der *Grund*. Gibt das die Antwort aus 9760 F2 B nicht her, eine Frage an den
Stakeholder; Empfehlung: nur der *Grund*, denn wer *am Zug* ist, zeigt Arbiter schon in der
Leiste (Etappe 2), und mehr hat er nicht verlangt (Absicht 3).

**Stellungnahme.** Beides umgesetzt in
[BEW-23](../../domaene/anforderungen/phasen/bewegung/sperreNichtAmZug.md):
1. Neu BEW-23.3: „Phase beenden“ sperrt mit ‚keine Kohärenz‘ auch, wenn eine *Einheit* des
   *Spielers*, der nicht *am Zug* ist, nicht in *Kohärenz* ist (`core_rules.txt:434`, `:730`,
   QUE-5.5). Als eigenes Kriterium in BEW-23 statt in BEW-4, denn nur BEW-23.2 führt dorthin;
   BEW-4.1 bleibt, wie getestet.
2. „wie AUF-22.1“ ersetzt durch „ohne Zeile unter dem *Grund*“. Ohne Frage an den
   Stakeholder: Seine Antwort auf 9760 F2 verlangt nur, dass es außer durch Übergehen nicht
   möglich ist, keine Zeile; Absicht 3 schließt die Zeile damit aus. BEW-23.1 hatte noch keinen
   Test, darum in derselben Kennung neu gefasst.
