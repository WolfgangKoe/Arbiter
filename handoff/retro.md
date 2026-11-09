# Retro · Zyklus 10

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 2 von 10 (Phasen und Bewegungsphase) ist nicht erreicht ([Review 10](review.md)); 156
von 176 Kriterien belegt, davon Etappe 2: 82 von 82 (Zyklus 9: 132 von 151). Neu am
Bildschirm: Anhalten vor fremden *Bases* mit Gleiten, die Canoptek-Spinne fliegt, „Einheit
zurücksetzen“, Loslassen neben dem *Spielfeld*, der Weirdboy.

## Was geklappt hat
Alle neun Items der Retro 9 umgesetzt. Kennzahlen unter der Schwelle: Prozesslast 24 von 202,
Prüfcode 876 gegen 1.350 Zeilen Produktcode. Dir gefiel, dass die Technikphase ausgedehnter
war; das bleibt (Absicht 2, 2590).

## Was nicht geklappt hat
1. Zwei Items sind nicht, wie du sie meintest; darum fehlt Etappe 2. Nach „gemeinsam
   übergehen“ folgen die *Modelle* nicht dem Zeiger, du dachtest an die *Aufstellung*. Beim
   *Griff* rückt das *Spielfeld*, kein Missverständnis: Eine Kritik in der Technikphase
   passte QUE-7.1 an O4 an, gegen ArbiterMap, ohne dich zu fragen (15560).
2. Die Prüfung „grün vor dem Code“ legte 16 Anliegen an, nur zwei machten einen Test rot; je
   Kritiker ein Doppel, Nummern außerhalb des Bereichs.
3. Läufe zu groß: Implementierer, Testautor und Reviewer brachen an der Tokengrenze ab, das
   Umbenennen der Tests brauchte vier Läufe. Jeder Commit hält alle an.

Der gezielte Mutationslauf fängt 82 % (Anliegen 15462,
Testautor), der volle läuft noch. Keine Neuerung von Claude Code ersetzt Eigenes. Ohne Item
aus 14500: ac, ai bis ak, am, au (Kosten der Kritik), an (Hook fing es), ap (kein
`ruff format`), ar, at (Rechner, Limit).

## Prozess-Items
Einzelheiten in den Anliegen; Rückweg: Commit `P<k>:` zurücknehmen.
- P1 Bedienung wie gemeint (Organisationsentwickler), in DoR 6: Gleicht eine Geste einer
  gebauten, nennt die Anforderung sie als Vorbild am laufenden Arbiter („in der *Aufstellung*
  ziehen“) und worin die neue abweicht. Ändert sich ein Kriterium nach der Freigabe Plan,
  prüft es der Fachkritiker vor dem Test; weicht es von ArbiterMap oder Arbiter-old ab, fragt
  dich der Anforderungsautor.
- P2 Hindernisse kurz (Regelumsetzer), 12520, 15301, 14500: Unter einem Schritt steht nur
  `- [ ] Hindernis <nr> <Titel>`, abgehakt mit `angenommen` oder `erledigt`.
- P3 Grüne Tests einmal je Item (Regelumsetzer), 11500, 12900, 13102, 13420: Die Prüfung
  läuft einmal je Item, mit einem Anliegen für beide Kritiker; sie zählt nur den Umfang und
  misst einen nachgereichten Test am Stand seines Commits.
- P4 Parallel als Regel (Organisationsentwickler, dann Regelumsetzer), 14360 F1 B, 11100,
  14500: Nach jedem Lauf nennt der Hook, was nach `Wartet auf` frei ist, der Koordinator
  startet es oder nennt den Grund; Quelle ist [Absicht 7](../prozess/praemissen/absicht.md). Jeder
  Auftrag passt in einen Lauf: Ein Item teilt er nach Kriterien, je Teil grüne Tests durch
  alle Schichten; das Review in Bildschirm und Rundgang. Je ein Commit läuft in einem eigenen
  Arbeitsbaum, die Rollen arbeiten weiter; am Klon mit echtem Hook erprobt (14360).
- P5 Etappe und Fortschritt (Regelumsetzer), 15361, 9801, 13150: Nach einer erreichten
  Etappe stehen Ausformulieren und Freigabe der nächsten im Fortschritt. Abgehakte Zeilen
  bleiben im Endstand, ein Kriterium einer späteren Etappe verlangt keinen Test.
- P6 Dashboard lädt schneller (Regelumsetzer), 8860: Ursache messen, beheben, Messung
  davor und danach im Anliegen.
- P7 Ein Mutationslauf (Organisationsentwickler), 15960: nach `Freigabe Review`, gezielt,
  bei erreichter Etappe voll; Überlebende für die Domänenphase.
- P8 Startprompt einmal (Organisationsentwickler), 16220: wenn nichts mehr läuft.

## Empfehlung
Gib frei.
Folgen: neun Läufe zu je unter 120.000 Token. Regelumsetzer nacheinander: P3, P2, P4, P5,
P6; ich daneben P1, P4, P7, P8. P1 wirkt ab Domänenphase 11, P7 ab `Freigabe Review 11`.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [x] Fachkritiker: Kritik an der Retro
- [x] Architekt: Kritik an der Retro
- [x] Organisationsentwickler: Nachkorrektur
- [x] Stakeholder: Freigabe Retro 10
- [x] Organisationsentwickler: P1
- [x] Regelumsetzer: P2
- [x] Regelumsetzer: P3
- [x] Organisationsentwickler: P4
- [ ] Regelumsetzer: P5
- [x] Regelumsetzer: P6
- [x] Organisationsentwickler: P7
- [x] Organisationsentwickler: P8
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: ja
Kommentar: .
