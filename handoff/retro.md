# Retro · Zyklus 6

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 1 von 7 (Aufstellen), Zyklus 6, keine erreicht; 78 von 103 Kriterien belegt
(Zyklus 5: 74 von 94, [Review 6](review.md)).

## Was geklappt hat
Alle drei Items abgenommen, eines mit Vorbehalt (AUF-26, 1820); Mutationstests fanden
ungeprüfte Fälle (1551, 1590, 1710).

## Was nicht geklappt hat
1. Der Mutationslauf dauerte über 100 Minuten (1570) und fand keinen Fehler am Bildschirm;
   Umformungen gegen gleichwertige Mutanten lesen sich schlechter (1751), eine brachte einen
   float-Fehler (1760).
2. Sechsmal schrieb eine Rolle per Python über Bash (Lücke 510).
3. Befunde standen nur in Schlussantworten (Ich 5), Empfänger setzten `erledigt` (1581, 1591).
4. Die DoD war bei rotem SonarLint abgehakt (Rundgang 1); Bildschirmtests holte erst der
   Reviewer nach.
5. Der Befehl für ein Hindernis vergibt fremde Nummern (Rundgang 3).
6. Der Koordinator sagte „läuft allein“, startete drei Rollen.
7. Bis „Freigabe Review 6“ rund 870 Zeilen Prüfcode, 518 Produktcode, beide ohne Tests: über
   der Schwelle (730). Prozesslast 15 von 148 Anliegen, unter einem Drittel.
8. Wartende Anliegen fehlen im Dashboard (1670), Kommentare doppeln Testnamen (1660).
9. Dreimal wich das Gebaute ohne deine Entscheidung von ArbiterMap ab, spät bemerkt (DoR 6,
   1841): Sprung über fremde *Bases* (1820), Loslassen über der Kante, Greifpunkt (1610).

## Prozess-Items
Zwei aus Befunden (P1, P3), deine Aufträge P2, P4, P5 (Anliegen 1671 F1).
- P1 Regeln nachziehen (Organisationsentwickler): Ablauf und Rollen nennen: Kennzahl
  Prüfcode gegen Produktcode ohne Tests, Beginn der Retro, Kritiker gleichzeitig (730), ein
  Commit für mehrere Items (740), nie `erledigt` durch den Empfänger und Befunde nur als
  Anliegen (3), Es 8 (1660), Kopf (1670), DoD und Commits zu P2, Backlog mit „Freigabe Retro
  6“. Der Koordinator sagt jeder Rolle, wer neben ihr läuft (6) und welche Nummern sie
  vergibt, und committet nach jedem Lauf, der etwas abschließt; der Implementierer meldet
  erst mit allen Tests fertig (4). DoR 6 gilt für ArbiterMap samt Frontend, auch wo
  Architektur oder Empfehlung die Bedienung festlegen; der Fachkritiker prüft die Fundstelle (9).
- P2 Prüfen in Minuten (Regelumsetzer, 1570, 1740, 1751): Mutanten nur in geänderten Zeilen,
  je Mutant nur die Tests, die sie ausführen, sonst alle; ein Ergebnis gilt, solange
  `technik/`, `pyproject.toml` und `domaene/daten` gleich sind (1850). Der volle Lauf, auch
  über `web/`, nur in der Retro, ohne aufzuhalten; seine Lücken nach 1671 F2: ein fehlendes
  Kriterium in die Domänenphase, sonst in die Technikphase. Unter 95 % wird jeder Überlebende
  angegangen, ein gleichwertiger zählt mit Begründung beim Werkzeug nicht; Code ändert sich
  nur, wenn er lesbarer wird. Der Commit-Hook lässt die Produkttests aus.
- P3 Schreiben nur mit Write und Edit (Regelumsetzer, 2): Skripte einer Rolle schreiben nicht
  ins Projekt: die Sandbox von Claude Code, erst an einer Kopie erprobt (1850);
  `bashSchreiben.py` verliert, was sie sperrt.
- P4 Anliegenboard nach Phasen (Regelumsetzer, 1670): Das Dashboard zeigt jedes nicht
  erledigte Anliegen nach Phase; ein Modul liest und schreibt den Kopf
  für alle Skripte und vergibt nur freie Nummern aus dem Bereich des Auftrags (5); dazu 1070.
- P5 Prüfungen statt Kommentare (Regelumsetzer, 1660): im Code nur Werkzeugkommentare und
  gedeckelte TODOs (Es 8); die bestehenden Kommentare entfernt er im Prüfcode, Implementierer
  und Testautor in der Technikphase 7, rot erst in deren DoD (Anliegen 1860).

## Empfehlung
Freigabe samt 1860, dann P1, danach P2 bis P5 und Anliegen 1790
(kein Item).

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [x] Fachkritiker: Kritik an der Retro
- [x] Architekt: Kritik an der Retro
- [x] Organisationsentwickler: Nachkorrektur
- [x] Stakeholder: Freigabe Retro 6
- [x] Organisationsentwickler: P1
- [x] Regelumsetzer: P2
- [ ] Regelumsetzer: P3
- [x] Regelumsetzer: P4
- [x] Regelumsetzer: P5
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: ja
Kommentar: Du kannst wieder häufiger committen, dafür ist es aber nicht nötig, jedes Mal die komplette Prüfung durchlaufen zu lassen.
Stellungnahme: P1 (Commit nach jedem Lauf, der etwas abschließt), P2 (Hook ohne Produkttests).
