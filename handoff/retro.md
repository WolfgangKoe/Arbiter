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
   ([289](anliegen/289-pruefungenBrechenAmHookDesNachbarnAb.md)). 290 nahm den Hook aus dem
   Prüflauf; ein Importfehler bricht ihn weiter ab, das behebt
   [304](anliegen/304-sammelfehlerBrechenPrueflaufAb.md) mit einer Zeile Konfiguration.
6. Der [Backlog](../prozess/backlog.md) löste für Retro 3 aus: Höchstmaße im Test,
   Gesamtmaß der Prüfskripte, Auslösezähler. Alles neue Mechanismen; nach Befund 2 sind sie
   bis Retro 4 zurückgestellt.
7. Claude Code bis 2.1.292: Nichts ersetzt einen eigenen Mechanismus. Die Korrekturen an der
   Sandbox (2.1.289, 2.1.290) gehen an den Versuch 215.
8. Dein Kommentar: zu viele offene Anliegen. Der Deckel griff nicht: 27 an den
   Regelumsetzer, Zufluss über die Ausnahme „Fehlverhalten“; seit Retro 2 kamen 139, 127 gingen.
9. Dein Kommentar: Die Schreibbilanz meldet deine Änderungen und die gleichzeitiger Läufe als
   „unklar, wer … Nicht committen“. Beides in [306](anliegen/306-offeneAnliegenWirksamBegrenzen.md).

## Geändert
Nach deinen Antworten in [296](anliegen/296-prozesslastEindaemmen.md) (F1 bis F3: A); zwei
bestehende Regeln angepasst, nichts neu gebaut.
- [Kennzahlen](../prozess/kennzahlen.md): Deckel, höchstens 10 offene Anliegen an den
  Regelumsetzer (F1).
- [Ablauf, Kritik am Code](../prozess/ablauf.md#kritik-am-code): am Code des Regelumsetzers
  nur Fehlverhalten, der Rest ein Sammelanliegen je Zyklus (F3).
- [Backlog](../prozess/backlog.md): Nachschliff 202 bis 206, 221; Befund 6 bis Retro 4.

## Anliegen an mich
- [150](anliegen/150-sonarlintAbdeckungUndToterCode.md) bleibt offen, bis SonarLint mit 216
  sperrt; ich melde es dort. 138 wartet auf 215, 219 auf 220, 289 auf 304.

## Prozess-Items
Keine. F2 ist erfüllt: 286, 287, 290, 294, 295 sind erledigt.

## Empfehlung
Erst [306](anliegen/306-offeneAnliegenWirksamBegrenzen.md) beantworten (F1 bis F3: A): Bestand
von 34 auf 10 offene, Sperre gegen neue über dem Deckel, Schreibbilanz löschen. Dann
freigeben; der Stand meldet Plan 4, Wählen per Klick (Review 3). Bis dahin beauftragt der
Koordinator den Regelumsetzer nur mit 304.

## Freigabe
Freigabe: offen
Kommentar: .
