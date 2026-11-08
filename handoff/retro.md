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
Prüfcode 876 gegen 1.350 Zeilen Produktcode.

## Was nicht geklappt hat
1. Zwei Items sind gebaut, wie Plan und Kriterium es sagen, du meintest es anders: Beim
   *Griff* rückt das *Spielfeld* (QUE-7.1 nimmt ihn aus), nach „gemeinsam übergehen“ folgen
   die *Modelle* nicht dem Zeiger. Darum fehlt Etappe 2; du schreibst „wieder“ ([15460](anliegen/15460-uebergehenUndLeistenNochInZyklus10.md)).
2. Die Prüfung „grün vor dem Code“ legte 16 Anliegen an, nur zwei machten einen Test rot; je
   Kritiker ein Doppel, Nummern außerhalb des Bereichs.
3. Läufe zu groß: Implementierer und Testautor brachen an der Tokengrenze ab, der Reviewer
   zweimal, das Umbenennen der Tests brauchte vier Läufe. Jeder Commit hält alle Rollen an.

Der gezielte Mutationslauf fängt 82 % ([15462](anliegen/15462-mutationZyklus10Ueberlebende.md),
Testautor); der volle läuft noch, seine Lücken schreibt der Reviewer als Anliegen. Keine
Neuerung von Claude Code ersetzt einen Mechanismus. Ohne Item: 12993 durfte direkt auf
`erledigt`, Absender und Empfänger sind eine Rolle; 15360 hat 3.816 Zeichen. Aus 14500 ac,
ai bis ak, am, au (Kosten der Kritik), an (der Hook fing es), ap (kein `ruff format` im
Hook), ar, at (Rechner, Limit).

## Prozess-Items
Einzelheiten in den Anliegen; Rückweg: Commit `P<k>:` zurücknehmen.
- P1 Ausprobieren vor der Freigabe (Organisationsentwickler), 15460: Gleicht eine Geste
  einer gebauten, nennt die Anforderung, worin sie abweicht (DoR 6). Sagt ein Kriterium, was
  beim Ziehen geschieht, kannst du im Mockup ziehen und siehst es vor der Freigabe Plan.
- P2 Hindernisse kurz (Regelumsetzer), 12520, 15301, 14500: Unter einem Schritt steht nur
  `- [ ] Hindernis <nr> <Titel>`, Einzelheiten im Anliegen. Der Haken kommt mit `angenommen`
  oder `erledigt` und bleibt.
- P3 Grüne Tests einmal je Item (Regelumsetzer), 11500, 12900, 13102, 13420: Die Prüfung
  läuft einmal je Item, ein Anliegen an den Testautor gilt für beide Kritiker. Sie zählt nur
  den Umfang, einen nachgereichten Test misst sie am Stand seines Commits.
- P4 Parallel als Regel (Organisationsentwickler, dann Regelumsetzer), 14360, 11100, 14500:
  Nach jedem Lauf nennt der Hook, was frei ist, und der Koordinator startet es. Jeder
  Auftrag passt in einen Lauf: Ein Item teilt er vorher, das Review in Bildschirm und
  Rundgang. Der Commit läuft in einem eigenen Arbeitsbaum, die Rollen arbeiten daneben
  weiter, der Hook prüft genau den Commit. Erprobt nur an einem Spielzeug-Repo in `/tmp`.
- P5 Etappe und Fortschritt (Regelumsetzer), 15361, 9801, 13150: Nach einer erreichten
  Etappe stehen Ausformulieren und Freigabe der nächsten im Fortschritt. Abgehakte Zeilen
  bleiben im Endstand, ein Kriterium einer späteren Etappe verlangt keinen Test.
- P6 Dashboard lädt schneller (Regelumsetzer), 8860: Ursache der Ladezeit messen, beheben,
  mit Messung davor und danach im Anliegen.

Ins [Backlog](../prozess/backlog.md): eine Vorlage zum Umbenennen ganzer Testdateien, eine
Freigabe ohne Moderation davor.

## Empfehlung
Beantworte F1 in [14360](anliegen/14360-parallelArbeitenIstDieRegel.md), Empfehlung B, dann
gib frei.
Folgen: sieben Läufe zu je unter 120.000 Token. Regelumsetzer nacheinander: P3, P2, P4, P5,
P6. Ich daneben: P1, P4. P1 wirkt ab der Domänenphase 11. Ein ziehbares Mockup kostet den UX-Lauf mehr.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an der Retro
- [ ] Architekt: Kritik an der Retro
- [ ] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 10
- [ ] Organisationsentwickler: P1
- [ ] Regelumsetzer: P2
- [ ] Regelumsetzer: P3
- [ ] Organisationsentwickler: P4
- [ ] Regelumsetzer: P5
- [ ] Regelumsetzer: P6
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
