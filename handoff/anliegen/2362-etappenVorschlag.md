# Vorschlag: Etappen vor Plan 7

Form: Fragen
Von: Planer
An: Stakeholder
Runde: 1/3
Status: offen

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
Antwort: .

**Stellungnahme.**
