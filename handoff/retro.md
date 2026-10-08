# Retro · Zyklus 3

Etappe 1 · Aufstellen, Plan 3 mit zwei Items. Grundlage: [Review 3](review.md), git seit
`Freigabe Retro 2`, Anliegen, Belegung je Lauf (`prozess/dashboard/laeufe.jsonl`).

## Befunde
1. Inkrement: DoD 1 bis 4 erfüllt, QUE-2 und AUF-4 ohne Befund abgenommen.
2. Prozesslast zum zweiten Mal über der Schwelle: 90 von 129 neuen Anliegen gingen an den
   Regelumsetzer oder mich, 70 % (Retro 2: 52 %, Schwelle ein Drittel). Von 230 Läufen waren
   70 des Regelumsetzers, 46 der Rollen am Produkt.
3. Kritik erzeugt Kritik: Gut die Hälfte der offenen Anliegen war Kritik am Code der
   Prüfskripte, 202 bis 206 Nachschliff am Nachschliff. Deckel und „Kritik nur bei
   Fehlverhalten“ griffen nicht.
4. Belegung: 9 Läufe über 120.000 Token, keiner über 150.000.
5. Dein Kommentar in Anliegen 296 und 306: Die Organisation
   ist zum Produkt geworden; du willst Anforderungen, Akzeptanztests und grünen Produktcode
   sehen.

## Ergebnis: Rückbau und Rundgang
Deine Entscheidung, umgesetzt in be16d8d:
- Rückbau: Prüfskripte von 111 auf 60 Dateien, 390.000 auf 213.000 Zeichen, 900 auf 436
  Tests. Es bleiben Kriterium zu Akzeptanztest, Importvertrag, Benennung, Glossar,
  Codequalität des Produkts, Schreibgrenze, Stand, Belegung, Dashboard, Löschen erledigter
  Anliegen ([Regeln](../prozess/regeln.md)).
- Neue Regeln und Mechanismen erst bei beobachtetem Bedarf, wie bei den Rollen; Vorrang hat
  das Produkt ([Ablauf, Prozessphase](../prozess/ablauf.md#prozessphase)).
- Rundgang: Keine Kritik am Code der Prüfskripte und Hooks mehr. Einmal je Zyklus geht der
  Reviewer mit dir durch den neuen Prüfcode und notiert die wesentlichen Probleme im
  Review; was du beauftragst, wird ein Anliegen an den Regelumsetzer
  ([Ablauf, Technikphase](../prozess/ablauf.md#technikphase), Schritt 6). Kritik am
  Produktcode bleibt ([Kritik am Code](../prozess/ablauf.md#kritik-am-code)).
- Regelumsetzer und Dashboard bleiben.

## Geändert
Texte auf den Bestand gebracht, nichts neu gebaut:
- [Ablauf](../prozess/ablauf.md): Verweise auf entfallene Mechanismen sind „nur Text“; den
  nächsten Schritt leitet der Koordinator aus Ablauf und Freigabe-Commits ab; Rundgang;
  Kritik am Code nur am Produkt.
- [Kennzahlen](../prozess/kennzahlen.md): Deckel gelöscht, Höchstmaße nur Text.
- [Backlog](../prozess/backlog.md): Nachschliff und Gesamtmaß der Prüfskripte gelöscht;
  Auslöser nach Bedarf.
- Prämissen [ich](../prozess/praemissen/ich.md), [es](../prozess/praemissen/es.md): nur die
  Angaben „Mechanismus:“. In es.md, SOLID D, verweist „Schichten in Regeln“ auf nichts mehr;
  der Inhalt ist deine Entscheidung.
- Rollen: Reviewer (Rundgang), Koordinator, Regelumsetzer, UX, ich.
- 18 Anliegen erledigt (Entfällt mit dem Rückbau), dazu 303 und 306.

## Anliegen an mich
138 und 219 entfallen mit dem Rückbau (erledigt).
[150](anliegen/150-sonarlintAbdeckungUndToterCode.md) bleibt offen bis 216 (SonarLint beim
Commit). [289](anliegen/289-pruefungenBrechenAmHookDesNachbarnAb.md) wartet auf 304.

## Prozess-Items
Keine.

## Empfehlung
Freigeben, dann Plan 4, Wählen per Klick (Review 3); der erste Rundgang steht in Review 4.
Offen beim Regelumsetzer bleiben 202, 203, 216, 228, 229, 232, 246, 249, 275, 302, 304.
Davon sind 202, 203, 228, 229, 232 und 302 Kritik am Code der Prüfskripte; ich empfehle,
sie wie die übrigen zu schließen und Wesentliches im Rundgang zu nennen.

## Freigabe
Freigabe: ja
Kommentar: .
