# Vorschlag: Etappen vor Plan 7

Form: Fragen
Von: Planer
An: Stakeholder
Runde: 1/3
Status: angenommen
Wartet auf: 2363

## Runde 1
**Befund.** Deine Vorgaben zu Etappe 1 bis 3, umgesetzt als Schnitt in sechs Etappen.
Annahme bis zu deiner Bestätigung: Eine *Sperre* einvernehmlich übergehen und protokollieren
([Ziel](../../domaene/ziel.md)) gilt weiter, nur nicht für ‚keine Kohärenz‘ beim Aufstellen
(F1 in [2361](2361-schnittDerEtappen.md)). Quelle: die Zustände einer *Einheit* über einen
Zug in [Arbiter-old](../../Arbiter-old/docs/spec/unit_states.md) und die Phasenfolge
(`core_rules.txt:639`).

1. **Aufstellen.** Wie gebaut, dazu „Einheit zurücklegen“: Die *Einheit* verschwindet von der
   *Karte*, ein Klick stellt sie neu auf. Ohne *Kohärenz* sperrt „Aufstellen der Einheit
   beenden“, nichts zum Übergehen; ihr setzt *Modelle* um oder legt die *Einheit* zurück.
   Arbiter läuft immer unter derselben Adresse.
2. **Phasen und Bewegungsphase.** Wer am Tisch den Roll-off gewinnt, wählt am Bildschirm den
   ersten Zug (`:2329`, F3 in 2361). Arbiter zeigt Schlachtrunde, Spieler am Zug und Phase:
   Kommando-, Bewegungs-, Psi-, Schuss-, Angriffs-, Nahkampf-, Moralphase; eine noch nicht
   begleitete ist leer, ihr beendet sie ohne Spielhandlung (Anliegen 07). In der
   Bewegungsphase macht jede eigene *Einheit* einmal einen Normal Move bis M oder bleibt
   stehen (`:738`); Arbiter sperrt über M, über eine fremde *Base*, über die Kante, in
   Engagement Range, am Ende ohne *Kohärenz*. Hier kommt „gemeinsam übergehen“ mit dem
   *Protokoll*. Nach der fünften Schlachtrunde endet die Schlacht (`:2337`).
3. **Vorrücken, Schießen, Moral.** Advance mit eingegebenem Wurf, danach nur Assault-Waffen;
   Reichweite je *Modell*, Würfe am Tisch, Verluste entfernen, Befehlspunkte; Moralphase mit
   Moraltest und Kohärenzprüfung (Anliegen 09 F13 A).
4. **Angriff und Nahkampf.** Charge mit eingegebenem Wurf, Heroische Intervention, Pile In,
   Kämpfen der Reihe nach, Consolidate; Fall Back, wer in Engagement Range steht, kann nur das
   oder stehen bleiben (`:739`). Hier zieht ihr dieselbe *Einheit* mehrmals: Anhalten nach
   mehrfachem Weiterrücken, Entlanggleiten an fremden *Bases*.
5. **Jede Baseform.** Unverändert.
6. **Vollständige Partie.** Wie bisher, dazu aus Arbiter-old: Regeln der Befehlsphase,
   Verstärkungen aus der Reserve, Abwehrfeuer als Stratagem.

Was Etappe 1 verlässt (F2 in 2361): nach 2 Ziehen und Loslassen (AUF-28.1, 16.8, 8.7, 12.8,
16.7), ruhige *Karte* (QUE-7), *Leisten* (QUE-6); nach 4 Anhalten auf dem Weg (AUF-29, 28.2);
nach 6 die Randfälle nur des Aufstellens (AUF-18.7, 27, 22, 20.6, 3.9, 8.8). AUF-11 bleibt
nach 990.

AUF-13 entfällt, seine Kennung kommt nicht wieder; mit ihm AUF-17 („zurück“ ohne *Sperre*).
QUE-5 bleibt, zuerst bei den *Sperren* des Normal Move. Item gemeinsamUebergehen wandert nach
Etappe 2 mit QUE-5 und QUE-6, ohne AUF-13; Ux zeichnet auf-13 und que-5 für die Bewegung neu.

Der Anforderungsautor streicht AUF-13 und 17; hält in AUF-10 fest, dass ‚keine Kohärenz‘
nicht zu übergehen ist; nimmt AUF-13 und „zurück“ aus QUE-5, QUE-7.1, AUF-12.6, AUF-26 und
dem Glossar (*gemeinsam übergehen*, *Protokoll*, *Sperre*, *zurück*); schreibt neu für Etappe 2
Phasenfolge, ersten Zug, Normal Move, Übergehen beim Bewegen.

Plan 7 hat danach zwei Items: Aufräumen und feste Adresse, dazu AUF-17 entfernen; Einheit
zurücklegen, nur AUF-23. Danach ist Etappe 1 erreicht. 2301 und 2311 entfallen, das Mockup zu
AUF-23 zeigt die Spalten von heute (2300), 2310 kommt in den neuen Happy Path.

**Kosten.** Ohne Freigabe stehen Etappen und Plan 7 auf Annahmen.

**Gegenvorschlag.** Nach deinem „.“ schreibe ich Etappen, Items und Plan 7 und bitte den
Anforderungsautor in einem Anliegen um die Änderungen oben.

**F1 · Gibst du den Schnitt frei?** A: Ja. B: Mit deinem Kommentar darunter.
Empfehlung: A. Jede Etappe fügt die Zustände hinzu, die Arbiter-old für einen Zug nennt, in
der Reihenfolge der Phasen.
Antwort: B

**Stellungnahme.**
Kommentar: Grundsätzlich sieht das schon gut aus. Ich würde den Schnitt allerdings so machen, dass wir zunächst alle "Bewegungsformen" entlang der Phasen umsetzen. 1. Wie von dir hier beschrieben. 2. Phasen und Bewegungsphase mit normaler Bewegung und Vorrücken wie in Arbiter-Old angesetzt. Jede dieser Bewegungen sollte zurückgesetzt werden können. Die technische Bewegung sollte aus ArbiterMap entnommen werden können. Zurückziehen ist explizit noch nicht Teil des Ganzen. Das machen wir dann, sobald wir eine neue Runde beginnen. Das ist ja letztendlich eine "normale Bewegung" unter bestimmten Bedingungen und mit bestimmten Folgen auf folgende Phasen. Die sollten erst alle gebaut sein. Hier müssen die bestehenden Armeen etwas erweitert werden: Es bräuchte bei den Orks einen Psioniker und bei den Necrons eine Canoptech-Spinne. Wir brauchen jeweils auch ein passendes Fahrzeug. 3. Psi-Phase und Fernkampfphase bleiben erst mal "leer" bzw. dort kann "markiert" werden, welche Einheit als "hat eine Psi-Kraft versucht zu manifestieren" und "hat geschossen" betrachtet wird, sofern sie das mit ihrer Bewaffnung darf. Wir gehen damit zur Angriffsphase, wo wir eine Logik von Arbiter-old und ArbiterMap aufgreifen sollten. IN diese Etappen kann dann auch die Rückzugsbewegung für die Bewegungsphase implementiert werden. Dafür sollte dann alles wichtige vorhanden sein. 4. Wir implementieren die Attackensequenz aus Arbiter-old. Diese kann dann in die Fernkampfphase und die Nahkampfphase integriert werden. Die Logik, wie viele Modelle und welche Einheiten und wie viele Schuss bei welcher Distanz gegen wen abgegeben werden können, wäre komplett Teil dieser Etappe. 5. Implementierung von Psi- und Moralphase 6. HIer sollten wir dann anfangen, die App etwas mehr mit den Features aus Arbiter-old zu befüllen. GameHeader, armyCards und unitCards, datasheets, gameProtocol 7. Ich denke, dass wir hier die Datenbanken für die Orks und die Necrons anlegen und die "Start"-Seite für die Spielvorbereitung. 8. Armybuilder zum zusammenstellen einer Necron- und Ork-Armee 9. Ergänzung weiterer Armeen. Wichtig wäre, dass diese Etappen alle nicht fixiert sein müssen. Nach jedem ABschluss einer Etappe muss ich neu orüfen, ob dieser Plan hier noch funktionieren kann. Bitte diesen Schnitt prüfen. Lege nicht jedes Wort auf die Goldwaage, sondern sei gerne kritisch. Wichtig wäre mir zunächst, dass wir die wesentlichen FUnktionen zügig bauen, bevor wir die Randfälle angehen. Das Produkt soll eine Art MVP-Status erreichen, um eine Party mit Necrons und Orks spielen zu können. Auf Gefechtsoptionen und Fähigkeiten können wir erstmal noch verzichten.
Stellungnahme: Eingearbeitet als neuer Schnitt in [2363](2363-schnittBewegungsformenZuerst.md), kritische Punkte als Fragen in [2364](2364-fahrzeugMoralSiegpunkte.md). Erledigt setze ich, sobald die Etappen nach deiner Freigabe geschrieben sind.
