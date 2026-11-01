# Retro · Zyklus 9

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 2 von 10 (Phasen und Bewegungsphase) läuft ([Review 9](review.md)); 132 von 151
Kriterien belegt, davon Etappe 2: 57 von 63 (Zyklus 8: 95 von 123). Neu am Bildschirm:
„gemeinsam übergehen“ mit *Protokoll*, *Auswahl* von *Einheit* oder *Modell*, *Grenzkreise*,
*Vorrücken* samt Zurücknehmen, Anhalten an der Grenze, ein- und ausfahrende *Leisten*.

## Was geklappt hat
Alle vier Items abgenommen. Der volle Mutationslauf brauchte auf 8 Kernen gut anderthalb
statt drei Stunden, 96 % gefangen (8961).

## Was nicht geklappt hat
1. 8 von 20 Hindernissen gingen an den Testautor, auch auf Opus: Vier Tests waren grün vor dem
   Code (7300, 7320, 7400, 7660), zwei nie grün (7640, 8280). „Am Ende rot“ steht beim
   [Testautor](../.claude/agents/testautor.md) nur als Text.
2. Du suchtest einen Fehler in den Tests der *Leisten*, der aus einem Nachbarlauf kam; ein Lauf
   mit `-x` meldete grün, ohne alle Prüfungen zu sehen (8022, 8042).
3. Ein neues Hindernis trug sofort „beseitigt“ (8951, 8962).

Kennzahlen unter der Schwelle: Prozesslast 19 von 126, Prüfcode 843 gegen 1.093 Zeilen. Keine
Neuerung von Claude Code ersetzt einen Mechanismus. 6361 ist nachgeprüft und erledigt.

## Prozess-Items
Eingeplant ist jedes Anliegen, das auf diese Phase wartet (dein Auftrag); P1 bis P3 gelten den
Befunden.
- P1 Tests rot vor dem Code (Regelumsetzer): Hakt der Testautor „Tests zu Item <k>“ ab, laufen
  dessen Tests; ist einer grün, hakt der Befehl nicht ab, bis der Test den Zustand vorher prüft
  oder begründet ist. Nicht erprobt, Rückweg: Commit zurücknehmen.
- P2 Belege in der DoD (Organisationsentwickler), 8022, 8042, 8961, 6960:
  [DoD](../prozess/ablauf/dod.md) 1 und 2 ohne `-x`, bei einem Lauf daneben auf einem Abzug in
  `/tmp`, die Meldung nennt den Stand: „grün“ gilt für einen Stand, den es gab. Der volle
  Mutationslauf nur im Zyklus, der die Etappe abschließen soll (Antwort A).
- P3 Stand und Fortschritt (Regelumsetzer), 8962 mit 8951, 7030, 8990 (1): „beseitigt“ erst
  durch einen Commit nach dem Hindernis, Items nur aus dem Abschnitt „Items“, der Stand lädt
  schneller.
- P4 Mutationslauf (Regelumsetzer), 8990 (5, 6, 8): Alle Kerne bleiben belegt, ein Test
  belegt das; ein gleichwertiger Mutant gilt nur für seine Klasse.
- P5 Sperren und Anliegen (Regelumsetzer), 3960, 6432, 8044: Python ohne Skriptdatei ist
  gesperrt, die Regeln nennen die übrigen Lücken; fehlt die Zeile `Antwort:`, geht deine Antwort
  nicht verloren; „UX“ gilt als Rolle; SonarLint 6.2.
- P6 Dashboard (Regelumsetzer), 8860 mit 6988: Tokenbericht je Seite, Pfeile nur am
  angeklickten Kasten, die Ansicht bleibt beim Neuladen.
- P7 Abdeckung des Frontends (Regelumsetzer, dann Organisationsentwickler), 6471: Nach einem
  Versuch in `/tmp` misst DoD 1 auch `technik/frontend/`: Verhalten ohne Test fällt ohne Lesen
  auf. Unterschreitet der Bestand die Schwelle, fragt dich ein Anliegen.
- P8 Rollen verlinkt, Wartendes im Plan (Organisationsentwickler), 6987, 7380: CLAUDE.md und die
  drei Phasen verlinken die Rollen, jede Ordner-CLAUDE.md nur die ihrer Perspektive; der Plan
  nennt die Anliegen, die auf seine Technikphase warten: Du siehst, wann das Aufräumen kommt.
- P9 Formate (Organisationsentwickler), 6500, 7080: [Domäne](../domaene/CLAUDE.md) mit
  `Etappe: <n>`; [Kennzahlen](../prozess/kennzahlen.md) ohne Summe der Architektur, ein voller
  Vertrag wird Ordner.

## Empfehlung
Beantworte F1 bis F3 in [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) im
Dashboard; vorher wartet P6. Dann gib frei.
Folgen: 10 Läufe zu je unter 120.000 Token, höchstens 1,2 Millionen. Der
Regelumsetzer nacheinander, Bestand zuerst (306): P3, P5, P4, P6, P1, P7; ich daneben P2,
P9, P8, dann P7. Die Domänenphase 10 beginnt nach 7 Läufen nacheinander.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an der Retro
- [ ] Architekt: Kritik an der Retro
  Hindernis: Architekt → Organisationsentwickler: Ein wartendes Anliegen (7031) fehlt, P1, P4, P6, P7 und P8 lassen Fälle offen, Probe und Rückweg fehlen (Anliegen 9010)
  Hindernis: Architekt → Regelumsetzer: Ein Test der freien Nummern ist rot, seit Anliegen 9000 besteht; Commits der Prozess-Items scheitern daran (Anliegen 9011)
- [ ] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 9
- [ ] Regelumsetzer: P1
- [ ] Organisationsentwickler: P2
- [ ] Regelumsetzer: P3
- [ ] Regelumsetzer: P4
- [ ] Regelumsetzer: P5
- [ ] Regelumsetzer: P6
- [ ] Regelumsetzer: P7
- [ ] Organisationsentwickler: P8
- [ ] Organisationsentwickler: P9
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
