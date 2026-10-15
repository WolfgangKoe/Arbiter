# Retro · Zyklus 5

Dashboard: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten,
`http://127.0.0.1:8765/` öffnen, Strg+C beendet.

Etappe 1 von 7 (Aufstellen), Zyklus 5, keine erreicht; 74 von 94 Kriterien haben einen
Akzeptanztest. Neu am Bildschirm: *Einheiten* auf die *Karte* ziehen, *Modelle*
verschieben, *gesperrt* stehen mit *Grund*, „zurück“, „Aufstellen der Einheit beenden“.
Es fehlen „gemeinsam übergehen“ mit *Protokoll*, *Gewinner* und Zone, *Leisten* und das
Aufstellen per Klick wie ArbiterMap.

## Was geklappt hat
- Die Domänenphase: Anforderungen und Mockups nach den Vorbildern, das Format passt (dein
  Urteil).
- Der Reviewer baute Fehler in den Code ein und fand zwei Fälle, die kein Test prüft.

## Was nicht geklappt hat
1. Du siehst nicht, was passiert: Der Fortschritt unten hakt nur ab, was ein Skript
   erkennt; die Kritik ist geschehen, ihr Haken fehlt.
2. Feinschliff bremste: 89 Anliegen, 114 Commits, nur 8 mit Produktcode; mehr neuer
   Prüfcode (2.668 Zeilen) als Produktcode (1.035). Rollen stritten über Form und Länge,
   Kritikrunden hatten kein Ende, Regelumsetzer und ich liefen neben dem Produkt.
3. Niemand prüfte die Anforderungen fachlich; die fehlende Bedienung per Klick fiel erst dir
   auf.
4. Ich habe Regeln vor deiner Freigabe geändert; P1 nimmt sie zurück.

## Backlog
Mutationstests sind jetzt P3; zwölf der übrigen 13 Punkte löscht P1.

## Prozess-Items
- P1 Ablauf nach deinem Modell (Organisationsentwickler):
  - Domäne: Der Anforderungsautor leitet zum Etappenziel die Happy Paths des Spielers aus
    ArbiterMap und Arbiter-old ab, UX zeichnet die Mockups, der Fachkritiker prüft beides
    gegen Ziel und Regeltext. Die Vorbilder gelten nur der Domäne; eine Abweichung ist eine
    Frage an dich. Dann der Plan; alle Rollen kritisieren.
  - Technik: Testautor, Kritik aller Rollen; Implementierer; den Produktcode prüfen
    Architekt (Architektur) und Reviewer (Lesbarkeit); dann das Review.
  - Kritik: je Artefakt eine Runde aller Kritiker; jeder ordnet seine Befunde ein, der Autor
    bessert nach oder widerspricht. Eine weitere Runde nur für, was aufhält; nach der
    dritten entscheidest du. Hält auf: Ein Schritt des Happy Path fehlt, eine *Sperre*
    greift zu Unrecht oder fehlt, obwohl ein Kriterium sie verlangt, ein Test prüft sein
    Kriterium nicht, neuer Code verletzt Architektur oder Lesbarkeit, eine Prüfung ist rot.
    Wartet auf die nächste Phase: Randfälle, Lücken abseits des Happy Path (auch eine
    *Sperre*, die nur der Regeltext verlangt), Namen und Ablage von Hilfsfunktionen,
    solange keine Prüfung rot ist. Entfällt: Form und Länge eines Anliegens, Geschmack
    ohne Regel.
  - Fehlt einer Rolle eine Entscheidung, fragt sie dich mit Empfehlung und arbeitet damit
    weiter, außer es hält den Happy Path auf; die Moderation listet solche Annahmen zuoberst.
  - Prozessregeln, Prämissen und Rollen ändern sich nur in der Prozessphase nach deiner
    Freigabe, die Architektur in der Technikphase. Die Retro beschreibt jedes Item in Worten.
  - Commits: nach jeder Phase und jedem Item mit Produktcode, samt Kritik und Anliegen.
- P2 Der Stand zeigt, was wirklich ist (Regelumsetzer): Rollen haken Kritik und
  Nachkorrektur selbst ab; wartende Anliegen gelten nicht als dran; erste Zeile Etappe und
  Kriterien wie oben.
- P3 Mutationstests (Regelumsetzer, 692): Ein Werkzeug baut Fehler in geänderte
  Domänenmodule ein und zählt, welche kein Test bemerkt. Es ersetzt die Probe des Reviewers,
  Lücken gehen an den Testautor. Die Schwelle schlage ich nach dem ersten Lauf vor.

Außerdem, da sie jede Rolle aufhalten: Schreibgrenze sperrt zu Unrecht (650), Commits
warten auf alle Prüfungen (601).

## Empfehlung
Freigeben. Danach P1 bis P3, dann Domänenphase 6 mit dem Aufstellen per Klick.
Stellungnahme: P1 gibt deine Antworten in 693 wieder, geschärft nach 695 und 697.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an der Retro
- [ ] Architekt: Kritik an der Retro
- [x] Organisationsentwickler: Nachkorrektur
- [x] Stakeholder: Freigabe Retro 5
- [ ] Organisationsentwickler: P1
- [ ] Regelumsetzer: P2
- [ ] Regelumsetzer: P3
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: ja
Kommentar: S. Anliegen 692 vom Architekten, bitte Mutationstests als item P3 einführen.
Stellungnahme: P3 steht, Backlog bereinigt.
