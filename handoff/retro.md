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
statt drei Stunden (8961, 8970).

## Was nicht geklappt hat
1. 8 von 20 Hindernissen gingen an den Testautor: vier Tests grün vor dem Code (7300, 7320,
   7400, 7660), zwei nie grün (7640, 8280).
2. Du suchtest einen Fehler in den Tests der *Leisten* aus einem Nachbarlauf; ein Lauf mit
   `-x` meldete grün, ohne alle Prüfungen zu sehen (8022, 8042).
3. Ein neues Hindernis trug sofort „beseitigt“ (8951, 8962).

Kennzahlen unter der Schwelle: Prozesslast 19 von 126, Prüfcode 843 gegen 1.093 Zeilen. Keine
Neuerung von Claude Code ersetzt einen Mechanismus.

## Prozess-Items
Eingeplant ist jedes Anliegen an diese Phase (dein Auftrag), Einzelheiten stehen in 9000 und
9010. Erprobt ist keines, Rückweg: Commit `P<k>:` zurücknehmen.
- P1 Tests rot vor dem Code (Regelumsetzer): Ist beim Abhaken der Tests eines Items einer
  grün, meldet der Befehl dem Testautor ein Hindernis: rot machen oder die Stelle nennen, die
  das Kriterium schon erfüllt; das prüft die Kritik.
- P2 Belege in der DoD (Organisationsentwickler), 8022, 8042, 8961, 6960: DoD 1 und 2 ohne
  `-x`, neben einem Lauf auf einem Abzug, die Meldung nennt den Stand; der volle
  Mutationslauf nur im Zyklus, der die Etappe abschließt (Antwort A).
- P3 Stand und Fortschritt (Regelumsetzer), 7030, 7031, 8951, 8962, 8990 (1): Items des Plans
  nur aus „Items“; Commits gelingen, solange nur deren Tests fehlen (7031 C); „beseitigt“ erst
  nach einem späteren Commit und mit `angenommen` oder `erledigt` auf der Platte; der Stand
  lädt schneller.
- P4 Mutationslauf (Regelumsetzer), 8990 (5, 6, 8): Alle Module laufen zugleich, ein Test
  belegt das; ein gleichwertiger Mutant gilt nur in seiner Klasse oder Funktion.
- P5 Sperren und Anliegen (Regelumsetzer), 9011, 3960, 6432, 8044: 9011 vor deiner Freigabe
  (Commits an Prüfskripten scheitern). Python ohne Skriptdatei gesperrt, `pytest` nicht, je
  Rolle geprobt; ohne Zeile `Antwort:` geht deine Antwort nicht verloren; „UX“ ist Rolle;
  SonarLint 6.2.
- P6 Dashboard (Regelumsetzer), 8860, 6988: Tokenbericht je Seite, Pfeile nur am angeklickten
  Kasten, die Ansicht bleibt beim Neuladen; der Test, der nur Text sucht, entfällt.
- P7 Abdeckung des Frontends (Regelumsetzer, dann Organisationsentwickler), 6471: Misst ein
  Versuch die Zeilen von `technik/frontend/`, verlangt DoD 1 dort 95 %; liegt der Bestand
  darunter, fragt dich ein Anliegen.
- P8 Wartendes, Rollen (Regelumsetzer, dann Organisationsentwickler), 7380, 6987: Wartet ein
  Anliegen auf eine Domänen- oder Technikphase, wird es dort ein Schritt im Fortschritt,
  in der Retro steht es in einem Item. CLAUDE.md und die Phasen verlinken die Rollen,
  Ordner-CLAUDE.md die ihrer Perspektive.
- P9 Formate (Organisationsentwickler), 6500, 7080: Domäne mit `Etappe: <n>`;
  Kennzahlen ohne Summe der Architektur, ein voller Vertrag wird Ordner.

## Empfehlung
Beantworte F1 bis F3 in [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) im
Dashboard; vorher wartet P6. Dann gib frei.
Folgen: 12 Läufe zu je unter 120.000 Token. Regelumsetzer nacheinander, Bestand zuerst
(306): P3, P5, P4, P6, P1, P7, P8; ich daneben P2, P9, P7, P8; Domänenphase 10 nach 8
Läufen. Rund 300 Zeilen Prüfcode zählen in Zyklus 10 (räumt auf, 8880); bei
weniger Produktcode löscht Retro 10 einen Mechanismus vor jedem neuen.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [x] Fachkritiker: Kritik an der Retro
- [x] Architekt: Kritik an der Retro
  Hindernis: Architekt → Organisationsentwickler: Ein wartendes Anliegen (7031) fehlt, P1, P4, P6, P7 und P8 lassen Fälle offen, Probe und Rückweg fehlen (Anliegen 9010); beseitigt: Commit „Retro 9 nach Kritik nachgebessert: 9000, 9010, 8970 und 8973 angenommen“
  Hindernis: Architekt → Regelumsetzer: Ein Test der freien Nummern ist rot, seit Anliegen 9000 besteht; Commits der Prozess-Items scheitern daran (Anliegen 9011); beseitigt: Commit „Kritik an Retro 9 nachgeprüft, Test der freien Nummern repariert“
- [x] Organisationsentwickler: Nachkorrektur
- [x] Stakeholder: Freigabe Retro 9
- [x] Regelumsetzer: P1
- [x] Organisationsentwickler: P2
- [x] Regelumsetzer: P3
- [x] Regelumsetzer: P4
- [x] Regelumsetzer: P5
- [x] Regelumsetzer: P6
- [x] Regelumsetzer: P7
- [x] Regelumsetzer: P8
- [x] Organisationsentwickler: P9
- [x] Koordinator: nach dev gepusht

## Freigabe
Freigabe: ja
Kommentar: .
