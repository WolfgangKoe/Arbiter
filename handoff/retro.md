# Retro · Zyklus 6

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 1 von 7 (Aufstellen), Zyklus 6, keine erreicht; 78 von 103 Kriterien haben einen
Akzeptanztest (Zyklus 5: 74 von 94). Neu am Bildschirm: eine *Einheit* per Klick als
*Formation* *setzen*, als Block oder ein *Modell* allein ziehen; sie halten an fremden *Bases*
und am Rand der Zone an ([Review 6](review.md)).

## Was geklappt hat
- Alle drei Items des Plans sind gebaut, abgenommen und gelöscht.
- Die Mutationstests fanden Fälle, die kein Test prüfte (1551, 1590).

## Was nicht geklappt hat
1. Der Reviewer wartete auf Mutationsläufe: 72 Minuten im ersten Lauf, die DoD jetzt über
   80; jeder Mutant startet alle Tests samt Bildschirmtests (1570).
2. Viermal schrieb eine Rolle per Python-Skript über Bash (Testautor, Architekt in 1530,
   Implementierer in 1542 und 1551); die Schreibgrenze sperrte spät oder nicht (Lücke 510).
3. Befunde standen nur in der Schlussantwort (Anforderungsautor zu W3 und que-7, Reviewer
   zu 1551); der Koordinator forderte die Anliegen nach ([Ich 5](../prozess/praemissen/ich.md)).
4. Der Implementierer setzte als Empfänger `erledigt`; die Nachprüfung hätte entfallen
   können (1581, 1591).
5. Der Befehl für ein Hindernis vergab eine Nummer aus dem Bereich einer anderen Rolle; das
   Hindernis zu 1560 fehlt im Plan.
6. Prüfcode gegen Produktcode (730): seit „Freigabe Retro 5“ 1.659 neue Zeilen Prüfcode,
   539 Produktcode, über der Schwelle.
   Prozesslast: 12 von 134 neuen Anliegen, unter einem Drittel.
7. Wartende Anliegen fehlen im Dashboard (1670); Kommentare im Code wiederholen, was
   Testnamen und Prüfungen sichern (1660).

Ohne Item: Architekt und Reviewer lagen bei 128.000 Token, der Hook meldete wie vorgesehen;
gleichzeitige Läufe sahen fremde Zwischenstände rot und liefen bei geteilten Dateien
nacheinander, wie [Gleichzeitige Läufe](../prozess/ablauf.md#gleichzeitige-läufe) es verlangt.

## Prozess-Items
Zwei aus Befunden (P1, P3), dazu deine Aufträge (P2, P4, P5); ob das gilt: [1671](anliegen/1671-prozessphaseVorziehen.md).
- P1 Regeln nachziehen (Organisationsentwickler): Was du entschieden hast, steht danach im
  Ablauf und in den Rollen: Kennzahl Prüfcode gegen Produktcode, Beginn der Retro, Kritiker
  gleichzeitig (730), ein Commit für mehrere Items (740), der Empfänger setzt nie `erledigt`
  (Befund 4), Befunde nur als Anliegen (Befund 3), Es 8 nach 1660, der Kopf nach 1670 und
  die drei Punkte des [Backlogs](../prozess/backlog.md) mit Auslöser „Freigabe Retro 6“.
- P2 Mutationslauf in Minuten (Regelumsetzer, 1570): Mutanten nur in geänderten Zeilen, je
  Mutant nur die Tests, die die Zeile ausführen; ein Ergebnis gilt weiter, solange Modul und
  Tests gleich bleiben. Den Zielwert schlage ich in 1570 vor.
- P3 Schreiben nur mit Write und Edit (Regelumsetzer, Befund 2): Ein Skript einer Rolle
  schreibt nicht mehr ins Projekt. Zuerst das Bordmittel, die Sandbox von Claude Code für
  Bash; das Betriebssystem setzt sie auch für Skripte durch, Teile von
  `rollenregeln/bashSchreiben.py` entfallen dann.
- P4 Anliegenboard nach Phasen (Regelumsetzer, 1670): Das Dashboard zeigt alle nicht
  erledigten Anliegen: wer jetzt dran ist, was auf ein anderes wartet, was für die nächsten
  Phasen vorgemerkt ist, je mit Kommentarfeld. Den Kopf lesen und schreiben alle Skripte
  über ein Modul, auch der Befehl für ein Hindernis, der nur freie Nummern vergibt (Befund 5).
- P5 Prüfungen statt Kommentare (Regelumsetzer, 1660): Im Code stehen nur Werkzeugkommentare
  und gedeckelte TODOs; ein TODO aus einer früheren Technikphase macht die DoD rot.

## Empfehlung
Kritik und Freigabe nach „Freigabe Review 6“; vorher fehlen der Fortschritt dieser Retro und
die Aufträge aus dem Rundgang Prüfcode des Reviews. Danach P1, dann P2 bis P5.

## Freigabe
Freigabe: offen
Kommentar: .
