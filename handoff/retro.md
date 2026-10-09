# Retro · Zyklus 4

Etappe 1 · Aufstellen, Plan 4 mit drei Items. Grundlage: [Review 4](review.md), git seit
Commit „Freigabe Retro 3“, Anliegen, Belegung je Lauf (`prozess/dashboard/laeufe.jsonl`).

## Befunde
1. Inkrement: DoD 1 bis 4 und Oberfläche erfüllt, alle drei Items ohne Befund abgenommen.
   Erstmals geht eine Handlung am Bildschirm: Einheiten in der Ablage auswählen.
2. Prozesslast unter der Schwelle: 8 von 49 neuen Anliegen gingen an den Regelumsetzer oder
   mich, 16 % (Retro 3: 70 %, Schwelle ein Drittel). Von 109 Läufen waren 15 seine oder
   meine (Retro 3: 70 von 230 allein seine). Der Rückbau aus Retro 3 wirkt.
3. Die Kritik gilt dem Produkt: 18 Anliegen an Testautor und Implementierer, keins am Code
   der Prüfskripte.
4. Der erste Rundgang durch den Prüfcode steht in Review 4: drei Probleme, du hast keins
   beauftragt; daraus entsteht kein Anliegen.
5. Belegung: 2 Läufe über 120.000 Token (Reviewer, Architekt), keiner über 150.000
   (Retro 3: 9 über 120.000).
6. Dreimal in einem Zyklus dieselbe Entscheidung: Du willst verstehen, ohne nachzuschlagen.
   Kriterien als Anwendungsfall (340), Commits mit Betreff statt Kennung (351), im Review
   Startbefehl, Klickpfad und ein Zyklusziel in Worten des Spielers (Kommentare zu Review 4).

## Geändert
- [Ablauf, Technikphase](../prozess/ablauf.md#technikphase), Schritt 6: Unter der ersten
  Zeile steht der Startbefehl, dann der Abschnitt „Am Bildschirm prüfen“ mit Klickpfad und
  erwartetem Bild; das Zyklusziel nennt zuerst, was danach am Bildschirm machbar ist und
  was noch nicht (Anliegen 353, 355). Mechanismus: nur Text.
- [Ablauf, Freigabe und Kommentare](../prozess/ablauf.md#freigabe-und-kommentare): In
  `handoff/` heißt ein Commit mit seinem Betreff, nicht mit der Kennung (354). Mechanismus:
  nur Text.

Kein neuer Mechanismus.

## Anliegen an mich
353, 354 und 355 umgesetzt, 289 mit Anliegen 304 umgesetzt; alle vier angenommen, die
Nachprüfung liegt beim Reviewer.

## Anliegen an dich
[356](anliegen/356-verstaendlichFuerDenStakeholder.md), aus Befund 6: eine Prämisse in
`wir.md`, damit jede Rolle für dich verständlich schreibt, auch in Plan, Retro, Anliegen und
Anforderungen. Für Plan 5 nicht nötig.

## Anliegen bei anderen
340 und 345 folgen nach deiner Antwort (F5 A, F6 A) in der nächsten Domänenphase in einem
Zug: Der Anforderungsautor schneidet die Anforderungen, der Testautor benennt die Tests um,
ich schreibe das Muster in `domaene/CLAUDE.md`, der Regelumsetzer baut das Spiegelskript
(dein Auftrag in 340; Befund 2 lässt ihn zu). Beim Regelumsetzer offen: 246, 249, 275;
249 ist eine Voraussetzung für Plan 5 (Review 4, Zyklusziel).

## Prozess-Items
Keine.

## Empfehlung
Freigeben, dann Domänenphase 5: zuerst 340 und 345, dann die Kriterien zum Ziehen nach
dem Zyklusziel aus Review 4; 249 vor der Technikphase 5.

## Freigabe
Freigabe: offen
Kommentar: .
