# Moderation

Stand: Prozessphase, Retro 9 wartet auf Kritik und Freigabe ([Retro](retro.md)). Nur 8860 hält
die Freigabe auf (P6 wartet auf deine Antwort).

## Dran
Blockiert das Inkrement: nichts außer 8860 (Stakeholder, siehe Fragen).
- Stakeholder: [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) (`rückfrage`, du
  bist Absender und dran).
- Regelumsetzer: Anliegen 3960,
  Anliegen 6432,
  Anliegen 6988,
  Anliegen 7030,
  Anliegen 8044,
  Anliegen 8962,
  Anliegen 8990.
- Organisationsentwickler: [6471](anliegen/6471-frontendOhneAbdeckung.md),
  Anliegen 7080,
  [7380](anliegen/7380-wartendeAnliegenEinplanen.md),
  Anliegen 8022,
  Anliegen 8042; Nachprüfung 6500, 6960, 6987, 8961.
- Reviewer: Nachprüfung 8970, 8973.

## Vorschläge
Befund zu deinem Auftrag (Fragen an den Stakeholder, ohne dass er am Zug ist). Geprüft sind
alle Anliegen mit `**F<n>`: 6960, 6987, 7031, 7800, 8840, 8860, 8880, 8961.
- Gleiches Muster nur in Anliegen 8840:
  Absender Stakeholder, `offen`, F1 bis F3 mit `Antwort: .`; dran wäre der Anforderungsautor,
  du hast keine Antwortfelder. Anforderungsautor: Status auf `rückfrage` setzen
  ([Status der Anliegen](../prozess/ablauf/anliegenStatus.md)). Er ist erst in der
  Domänenphase 10 dran; setzt er es nicht früher, kannst du 8840 nicht beantworten. Ob er es
  vor dieser Phase tun darf, entscheidet der Koordinator.
- Die anderen sechs sind unauffällig: An Stakeholder mit `angenommen` (6960, 6987, 7031,
  7800, 8880, 8961), Antworten stehen; 7031 hat in Runde 2 beantwortete Fragen.
- Ursache ist eine Regellücke, kein Einzelfall: Eine Rolle stellt Fragen in der Stellungnahme
  eines `offen`-Anliegens, das sie als Empfänger bearbeitet. [Anliegen](../prozess/ablauf/anliegen.md)
  sagt „Eine Rückfrage steht in der Stellungnahme“, nennt aber nicht, dass der Status dann
  `rückfrage` sein muss. Organisationsentwickler (Autor des Ablaufs): das ergänzen (Ich 4,
  bestehende Regel anpassen); ein Prüfskript dazu wäre Sache des Regelumsetzers, nur mit
  Vorschlag und Probe in `/tmp` (Ich 5).
- Regelumsetzer: 8860 ist mit `rückfrage` behoben; das Formular dafür deckt
  `rollenregeln/zuegeUebernehmen.py` schon ab, kein weiterer Hook nötig.
- Zusammen: 8042 und 8022 (Prüfläufe); 6960, 8961, 8970, 8973 (Mutationslauf).
- Stränge Regelumsetzer: Hook-Code höchstens einer (7030, 8962, 6988 nacheinander); 3960,
  6432, 8044 daneben. Organisationsentwickler: Ablauf (7380, 8022, 8042) getrennt von
  Formaten (6471, 7080).

## Fragen an dich
Zuoberst mit Annahme:
- [8860](anliegen/8860-dashboardLangsamUndUnuebersichtlich.md) F1 Tokenbericht seitenweise,
  F2 Architektur (dein Kommentar liegt vor), F3 Ansicht merken. Die Rolle fragt, ob
  „Ansonsten wie empfohlen“ auch für F1 und F3 gilt. Annahme: bis zur Antwort setzt sie
  nichts um.
- Anliegen 8840 F1 bis F3: Annahme
  Empfehlungen ab Domänenphase 10; beantwortbar erst nach `rückfrage` (siehe Vorschläge).
