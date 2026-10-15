# Retro · Zyklus 5

Dashboard öffnen: im Projektordner
`python3 prozess/pruefungen/gemeinsam/lauf.py rollenregeln.dashboardServer` starten, im
Browser `http://127.0.0.1:8765/` öffnen, beenden mit Strg+C.

Etappe 1 · Aufstellen, Zyklus 5. Etappe 1 von 7, keine erreicht; 74 von 94 Kriterien haben
einen Akzeptanztest. Neu am Bildschirm: *Einheiten* auf die *Karte* ziehen, *Modelle*
verschieben, *gesperrt* stehen mit *Grund*, „zurück“, „Aufstellen der Einheit beenden“.
Es fehlen „gemeinsam übergehen“ mit *Protokoll*, *Gewinner* und Zone, *Leisten* und das
Aufstellen per Klick wie ArbiterMap.

## Was geklappt hat
- Die Domänenphase: Anforderungen und Mockups nach ArbiterMap und Arbiter-old, das Format
  passt (dein Urteil).
- Der Reviewer baute Fehler in den Code ein und fand zwei Fälle, die kein Test prüft.

## Was nicht geklappt hat
1. Du siehst nicht, was passiert. Der Abschnitt Fortschritt unten hakt nur ab, was ein
   Skript an Dateien und Commits erkennt; die Kritik ist geschehen, ihr Haken fehlt, weil
   die Rollen ihn nicht setzen können. Er zeigt also zu wenig, nicht zu viel.
2. Feinschliff bremste: 89 Anliegen in fünf Tagen, 114 Commits, nur 8 mit Produktcode, jeder
   wartete 7 bis 8 Minuten auf alle Prüfungen; mehr neuer Prüfcode (2.668 Zeilen) als
   Produktcode (1.035). Rollen stritten über Form und Zeichenzahl, Kritikrunden hatten kein
   Ende, und Regelumsetzer und ich liefen neben dem Produkt.
3. Niemand prüfte die Anforderungen fachlich; die fehlende Bedienung per Klick fiel erst dir
   auf.
4. Ich habe Regeln vor deiner Freigabe geändert. Gegen dein Modell stehen davon: Feinschliff
   in einen Backlog je Perspektive (Ich 3, Fachkritiker, Architekt, Reviewer), den es nicht
   gibt, und ein Commit je Lauf mit Code statt je Phase und Item. Beides nimmt P1 zurück.

## Backlog
Von 14 Punkten zählen noch zwei: Mutationstests (deine Vormerkung, spätestens zu Etappe 2)
und Kriterien je Etappe zählen (sobald Etappe 1 erreicht ist). Die übrigen zwölf sind
Prüfungen und Werkzeuge ohne Anlass; P1 löscht sie.

## Prozess-Items
Umgesetzt erst nach deiner Freigabe.
- P1 Ablauf nach deinem Modell (ich):
  - Domäne: Der Anforderungsautor leitet zum Etappenziel die Happy Paths aus Sicht des
    Spielers aus ArbiterMap und Arbiter-old ab, UX zeichnet die Mockups. Der Fachkritiker
    prüft Anforderungen und Mockups fachlich, Maßstab: Ziel, Regeltext, ArbiterMap und
    Arbiter-old als Reflexionsfläche. Dann der Plan; alle Rollen kritisieren.
  - Technik: Testautor, Kritik aller Rollen; Implementierer; den Produktcode prüfen der
    Architekt (Architektur) und der Reviewer (Lesbarkeit); dann das Review.
  - Kritik: je Artefakt eine Runde aller Kritiker, danach bessert der Autor nach; eine
    weitere Runde nur für, was aufhält (693, F1); nach der dritten entscheidest du.
  - Regeln, Prämissen und Rollen ändern sich nur in der Prozessphase, nach deiner Freigabe.
    Die Retro sagt, was geklappt hat, was nicht, was im Backlog zählt, und beschreibt jedes
    Item in Worten statt mit Verweisen.
  - Commits: nach jeder Phase und nach jedem Item mit Produktcode; Kritik und Anliegen
    gehen mit.
- P2 Der Stand zeigt, was wirklich ist (Regelumsetzer): Rollen haken Kritik und
  Nachkorrektur selbst ab; wartende Anliegen gelten nicht als dran; erste Zeile „Etappe 1
  von 7 · 74 von 94 Kriterien“.

Außerhalb der Items, weil sie jede Rolle aufhalten: Schreibgrenze sperrt zu Unrecht (650),
Commits warten auf alle Prüfungen (601).

## Zu entscheiden
In [693](anliegen/693-ablaufNachDeinemModell.md): wann etwas bremst (F1), für wen
ArbiterMap und Arbiter-old Vorbild sind (F2), was eine Rolle tut, wenn ihr eine
Entscheidung fehlt (F3). Deine Rückfragen in 687 beantwortet die Klärung dort.

## Empfehlung
693 beantworten, dann freigeben. Danach P1, P2, dann Domänenphase 6 mit dem Aufstellen per
Klick.

## Fortschritt
- [x] Organisationsentwickler: Retro geschrieben
- [ ] Fachkritiker: Kritik an Regeländerungen
- [ ] Architekt: Kritik an Regeländerungen
- [ ] Organisationsentwickler: Nachkorrektur
- [ ] Stakeholder: Freigabe Retro 5
- [ ] Regelumsetzer: P1
- [ ] Regelumsetzer: P2
- [ ] Koordinator: nach dev gepusht

## Freigabe
Freigabe: offen
Kommentar: .
