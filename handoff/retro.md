# Retro · Zyklus 3

Etappe 1 · Aufstellen, Plan 3 mit zwei Items. Grundlage: [Review 3](review.md),
[Moderation](moderation.md), git seit `Freigabe Retro 2`, Anliegen, Belegung je Lauf
(`prozess/dashboard/laeufe.jsonl`).

## Befunde
1. Inkrement: DoD 1 bis 4 erfüllt, QUE-2 und AUF-4 ohne Befund abgenommen. Die Mockups
   bleiben, bis die Komponentenseite steht (262).
2. Prozesslast zum zweiten Mal über der Schwelle: 90 von 129 neuen Anliegen gingen an den
   Regelumsetzer oder mich, 70 % (Retro 2: 52 %, Schwelle ein Drittel). Offen sind 38, alle
   in der Perspektive Prozess, 31 an den Regelumsetzer. Prüfskripte 367.500 Zeichen
   (Retro 2: 183.000), Produkt samt Frontend 29.100. Von 230 Läufen waren 70 des
   Regelumsetzers, 46 der Rollen am Produkt. Die Reaktion „erst einen Mechanismus löschen“
   ist nur Text und griff wieder nicht.
3. Kritik erzeugt Kritik: Gut die Hälfte der offenen Anliegen ist Kritik am Code der
   Prüfskripte; 202 bis 206 sind Nachschliff am Nachschliff.
4. Belegung: 9 Läufe über 120.000 Token, höchstens 145.000 (Testautor), keiner über
   150.000 (Retro 2: einmal 197.000). Dreimal war ich es.
5. Gleichzeitige Läufe gehen (279). Ein halber Hook-Code bricht den Prüflauf der Nachbarn ab
   ([289](anliegen/289-pruefungenBrechenAmHookDesNachbarnAb.md), Umsetzung 290).
6. Der [Backlog](../prozess/backlog.md) löst für Retro 3 aus: Höchstmaße im Test,
   `kennzahlen.py` mit Gesamtmaß, Auslösezähler. Alles neue Mechanismen; nach Befund 2
   stelle ich sie bis Retro 4 zurück.
7. Claude Code bis 2.1.292: Nichts ersetzt einen eigenen Mechanismus. Die Korrekturen an der
   Sandbox (2.1.289, 2.1.290) gehen an den Versuch 215.

## Fragen an dich
Aus der Moderation, auf deinen Kommentar angelegt:
[296](anliegen/296-prozesslastEindaemmen.md). Sie passen zwei bestehende Regeln an, die
Reaktion der Prozesslast und Kritik am Code; neu gebaut wird nichts.
- F1: höchstens 10 offene Anliegen an den Regelumsetzer; 202 bis 206, 221, 295 in den
  Backlog.
- F2: vor Plan 4 nur 294 (P1) und 286, falls die Nachprüfung eine Lücke findet; im Strang
  Hook-Code zuerst 290.
- F3: Kritik am Code der Prüfskripte wird nur bei Fehlverhalten ein Anliegen, der Rest ein
  Sammelanliegen je Zyklus.

## Anliegen an mich
- [107](anliegen/107-kritikAnDenPruefungen.md): angenommen, 253 ist erledigt; das Eindämmen
  führt 296. Du prüfst nach.
- 138 wartet auf 215, [150](anliegen/150-sonarlintAbdeckungUndToterCode.md) auf 216, 219 auf
  220, 289 auf 290; ich schließe sie mit dem Umsetzen.

## Prozess-Items (Regelumsetzer, vor Plan 4)
Nur, was auf Plan 4 wirkt ([Ablauf, Prozessphase](../prozess/ablauf.md#prozessphase) 1).
- P1 Elementverbot ohne Lücken
  ([294](anliegen/294-elementverbotHatLuecken.md)): Es prüft das Frontend, das Plan 4
  ändert. Kein neuer Mechanismus, eine Lücke im bestehenden. Gilt mit F2 A.

## Empfehlung
Beantworte 296; danach ziehe ich Kennzahlen, Ablauf und Backlog nach (Nachkorrektur). Zur
Freigabe: P1. Danach Plan 4 mit Wählen per Klick (Review 3); die Kette des Regelumsetzers
läuft daneben, nach den Strängen der Moderation.

## Freigabe
Freigabe: offen
Kommentar: .
