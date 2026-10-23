# Moderation

Stand vor „Freigabe Review 7“. Hält auf: nur Anliegen 3250
(Reviewer). Keine Frage hält die Freigabe auf; keine Annahme nach [Ich 1](../prozess/praemissen/ich.md).

## Dran
- Reviewer, hält Review 7 auf: Anliegen 3250
  (Rundgang: vier Dateien fehlen; Satz zu Schritt 1 gesehen oder nur im Test).
  Danach schreibt er `review.md` neu, unter 4.000 Zeichen.
- Reviewer, hält nicht auf (Kopf: Technikphase, also Review 8):
  Anliegen 3200 (Weggefallenes im Klickpfad,
  Zyklusziel nennt jede *Sperre*) und
  Anliegen 3251 (Links, Belege, *Modell*).
- Organisationsentwickler (Prozessphase):
  [2040](anliegen/2040-pythonUeberBashNachFreigabeRetro6.md),
  [2360](anliegen/2360-es8MechanismusNachziehenUndHakenP5.md),
  [2590](anliegen/2590-ablaufUndRegelnInUnterordner.md),
  [2591](anliegen/2591-innenIchDesStakeholdersInDenPraemissen.md),
  [2201](anliegen/2201-aenderungenDesStakeholdersVorherErproben.md),
  [3050](anliegen/3050-hoechstmassDerArchitekturNach2570.md).
- Regelumsetzer (Prozessphase):
  [2460](anliegen/2460-hindernisAbhakenUndCommitBeiLaeufen.md),
  [2592](anliegen/2592-sedInSchleifeUmgehtSchreibgrenze.md),
  [2720](anliegen/2720-rueckverfolgungNenntEinzeldateiStattT1.md),
  [3120](anliegen/3120-architekturkarteImDashboard.md).
- Ux (Domänenphase): [2920](anliegen/2920-leistenNamenInDenMockups.md),
  [3040](anliegen/3040-que7MockupZeigtZurueckUndUebergehenBeiKohaerenz.md).
- Planer (Domänenphase): [3051](anliegen/3051-architekturUmordnenInPlan8.md), wartet auf F1.
- Architekt: [2215](anliegen/2215-leistenOhneEigenenNamen.md) wartet auf 2920,
  [2740](anliegen/2740-gemesseneUndBeschriebeneArchitektur.md) auf 3120.
- Fachkritiker: Anliegen 3200 fängt Plan 8 selbst ab
  (Domänenphase, Etappe 2 mit Kohärenz); nichts zu tun.

## Vorschläge
- Reviewer, ein Lauf für Review 8: 3200 und 3251 betreffen dasselbe Review (Klickpfad,
  Zyklusziel, Belege, Begriffe). Zusammenlegen dürfen die Absender (Fachkritiker,
  Organisationsentwickler); der Reviewer arbeitet beide in einem Durchgang ab.
- 3250 Punkt 1 und 3251 Punkt 1 (Dateien als Link) überlappen: Der Reviewer setzt in Review 7
  die vier Dateien gleich als Link; 3251 Punkt 1 bleibt für die übrigen Stellen.
- Der Stakeholder sagt im Chat: Fachlich sei alles in Ordnung, „Einheit zurücklegen“ gehe wie
  gewünscht. 3200 verlangt nur Klarheit im Review, nichts am Gebauten; es hält nicht auf.
- 3250 schließt der Organisationsentwickler nach Nachprüfung; ändert der Reviewer den Status,
  gilt der neue Stand. 3200 und 3251 bleiben bis Review 8 offen.
- Platz: Review 7 hat 3.934 von 4.000 Zeichen; Punkt 1 „Aus Review 6 behoben“ im Rundgang kann
  für 3250 weichen (Vorschlag des Absenders).
- Stränge: Prozessphase: Organisationsentwickler und Regelumsetzer getrennt, nur ein Lauf mit
  Hook-Code; 2460, 2592, 2720 und 3120 berühren `prozess/pruefungen/`, also nacheinander.
  2590 und 2591 ändern `ablauf.md`, `regeln.md` und die Prämissen: ein Lauf, danach 2360.
  Domänenphase: Ux (2920, 3040) und Planer (3051) gleichzeitig; Architekt danach 2215.
- 2040 und 2201 sind Belege für Retro 7, keine Arbeit vorher.

## Fragen an dich
- [3051 · F1](anliegen/3051-architekturUmordnenInPlan8.md): Nimmst du das Umordnen der
  Architektur als erstes Item in Plan 8? Empfehlung ja; hält die Freigabe von Review 7 nicht auf.
