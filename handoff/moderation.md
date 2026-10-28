# Moderation

Stand: Retro 8 wartet auf deine Freigabe ([Retro 8](retro.md)). Kein offenes Anliegen hält das
Inkrement auf; 6431 hält die Items P1, P3 und P4 der Retro auf.

## Dran
Blockiert: nur Anliegen 6431 (P1, P3, P4 brauchen F1 bis F3).
- Stakeholder: Anliegen 6431 F1 bis F3 und Freigabe Retro 8.
- Organisationsentwickler, Prozessphase 8: Anliegen 4620, Anliegen 4040.
- Regelumsetzer, Prozessphase 8: Anliegen 3900,
  [4301](anliegen/4301-fortschrittFuerItemOhneKriterium.md),
  [3780](anliegen/3780-restePruefcodeNach3301.md), Anliegen 4120,
  [4140](anliegen/4140-architekturAlsReiterBisZuDenDateien.md).
- Nachprüfung fällig: Anliegen 6870, Absender
  Koordinator, nach Regel niemand (siehe Vorschläge); Regelumsetzer, laufen daneben:
  Anliegen 6760,
  Anliegen 6820.
- Wartet auf 6431: Anliegen 6380, Anliegen 6430.
- Alle übrigen warten auf Domänen- oder Technikphase 9 oder Prozessphase 9
  ([3960](anliegen/3960-pythonOhneStrichUndLueckenInRegeln.md),
  [6432](anliegen/6432-antwortOhneZeileUndRolleUx.md),
  [6471](anliegen/6471-frontendOhneAbdeckung.md)); sie halten nichts auf.

## Vorschläge
- 6870, wer setzt `erledigt`: [Status der Anliegen](../prozess/ablauf/anliegenStatus.md) weist
  es dem Absender zu, der Empfänger setzt es nie. Absender ist der Koordinator, der keine Datei
  schreibt ([Koordinator](../.claude/agents/koordinator.md)). Für diesen Fall fehlt eine Regel
  ([Anliegen](../prozess/ablauf/anliegen.md), [Kritik](../prozess/ablauf/kritik.md) nennen ihn
  nicht). Empfehlung an den Organisationsentwickler (Autor des Ablaufs): Hat der Koordinator ein
  Anliegen gestellt, prüft auf seinen Auftrag eine Rolle, die nicht Empfänger ist, in seinem
  Namen nach und setzt `erledigt`; Absender bleibt er. Ich schreibe kein Anliegen: der
  Koordinator lässt es als Kritik 6900 anlegen. Bis dahin bleibt 6870 `angenommen`; du kannst
  `erledigt` selbst eintragen.
- 6430 und 6380 sind erledigt, wenn P3 und P4 stehen; du schließt sie nach Nachprüfung (Absender
  Stakeholder). 6431 schließt der Organisationsentwickler nach deinen Antworten.
- 4120 Schritt 1 und 2 sind Fälle von „doppelt“ aus 4040; P5 und P6 führen sie aus, dann
  kann der Organisationsentwickler 4120 schließen.
- 3900 und 4301 ändern beide `standregeln/fortschritt.py`: ein Lauf; P7 (Stand, Dashboard)
  berührt dieselben Module und folgt danach.
- 5181 und 4261 tragen deinen `Kommentar:`; 5181: ob Verschieben ohne Zurücklegen abbildbar
  ist, beantwortet die Domänenphase 9; 4261: Umbenennung von „Normal Move“ beachten.

Stränge der Prozess-Items nach der Freigabe:
- Organisationsentwickler, Kette: P1, P3, P5 (gemeinsame Dateien `rollenMitAusloeser.md`,
  `kritik.md`). P1 und P3 erst nach deinen Antworten; 4620 gehört in P3.
- Regelumsetzer, zwei Stränge gleichzeitig, wenn P4 keinen Hook-Code ändert (sonst P4 nach A):
  A: 3900 + 4301, dann P7. B: P4 (`formregeln/kommentare.py`, nach F1), dann P6 (3780, 4120).
- Organisationsentwickler und Regelumsetzer laufen nebeneinander. 4140 nach P6.

## Fragen an dich
Mit `Annahme:` (die Arbeit läuft weiter):
- [5181](anliegen/5181-klickAufEineAufgestellteEinheit.md) F1: Wählt in der Aufstellung der
  Klick eine aufgestellte Einheit aus? Annahme: A, der Klick ändert nichts.
- [6500](anliegen/6500-etappeEinesKriteriums.md): Format `Etappe: <n>` und `(Etappe <n>)`;
  Annahme: P7 zählt danach. Antwort an den Anforderungsautor.

Ohne `Annahme:`:
- Anliegen 6431 F1 (Docstrings), F2 (Testautor auf Opus), F3 (Prämissen verschieben): Der
  Organisationsentwickler hat F2 und F3 unter „Klärung“ erklärt. Trage je `Antwort:` ein.
- [4882](anliegen/4882-itemKatalogwerteGliedern.md) F1: Katalogwerte gliedern als erstes Item
  von Plan 9 (A) oder in Etappe 8 (B)? Empfehlung: A. Eine Zeile `Antwort:` fehlt dort.
