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
7. Review 4 hat über 7.000 Zeichen vor dem Abschnitt Freigabe, Höchstmaß 4.000; ein voller
   Klickpfad wüchse mit jedem Zyklus (Anliegen 359). Die Prüfung der Höchstmaße bleibt im
   [Backlog](../prozess/backlog.md); Schritt 6 schneidet den Klickpfad aufs Neue.

## Geändert
- [Ablauf, Technikphase](../prozess/ablauf.md#technikphase), Schritt 6: Unter der ersten
  Zeile steht der Startbefehl, dann der Abschnitt „Am Bildschirm prüfen“: ein Satz zum
  Gesamten, ein Klickpfad mit erwartetem Bild nur für das Neue; das Zyklusziel nennt
  zuerst, was danach am Bildschirm machbar ist und was noch nicht, mit den Begriffen des
  Glossars (Anliegen 353, 355, 358, 359). Mechanismus: nur Text.
- [Ablauf, Freigabe und Kommentare](../prozess/ablauf.md#freigabe-und-kommentare): In
  `handoff/` heißt ein Commit mit seinem Betreff, nicht mit der Kennung (354). Mechanismus:
  nur Text.

Kein neuer Mechanismus.

## Anliegen an mich
353, 354 und 355 umgesetzt, 289 mit Anliegen 304 umgesetzt; die Nachprüfung liegt beim
Reviewer. Die Kritik an dieser Retro, 357 und 358 (Planer) und 359 (Architekt), ist
umgesetzt und erledigt.

## Anliegen an dich
356, aus Befund 6, hast du angenommen: Die Prämisse steht als Punkt 5 in
[wir.md](../prozess/praemissen/wir.md), 356 ist erledigt.
Deine Frage dort, ob jede Rolle sie liest: Ja. Die Root-CLAUDE.md bindet `wir.md` ein, und
Claude Code lädt sie auch in jede Rolle, die der Koordinator startet. Ausgenommen sind nur
die eingebauten Rollen Explore und Plan und Rollen mit `omitClaudeMd`; beides nutzen wir
nicht. Gelesen heißt nicht befolgt, der Mechanismus ist nur Text. Dein Beobachten ist der
Befund: Zeigt ein Kommentar von dir wieder auf Unverständliches, schlage ich in der Retro
einen Mechanismus vor.

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
