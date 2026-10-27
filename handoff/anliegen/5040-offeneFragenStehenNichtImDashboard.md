# Offene Fragen an dich stehen nicht im Dashboard

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Am laufenden Dashboard und im Code geprüft: Das Dashboard zeigt „bei dir offen“
nur, was als Anliegen mit `An: Stakeholder` (Status `offen`) oder `eskaliert` in
`handoff/anliegen/` liegt (`anliegenregeln/anliegenDran.py`, `wartetAuf`; Zähler „Du bist
dran“ in `rollenregeln/dashboardAnliegenSeiten.py`). Heute ist kein Anliegen an dich offen
(4800 ist erledigt), also zeigt es nichts; der Befund stimmt, ein Fehler im Code liegt nicht
vor. Zwei Dinge bei dir sind keine Anliegen:
- Die Frage in [Moderation](../moderation.md), „Fragen an dich“: Sollen 3780 und 3900 jetzt
  oder in der Prozessphase 8 bearbeitet werden? Sie steht ohne eigenes Anliegen (Ablauf:
  Fragen stehen als Anliegen mit `Antwort:`-Zeile). Im Dashboard stehen 3780 und 3900 nur
  bei „Regelumsetzer“. Darauf antworte ich selbst, sobald du F1 beantwortest.
- Punkt 7 in [4140](4140-architekturAlsReiterBisZuDenDateien.md) ist keine Frage an dich:
  Das Anliegen geht von Architekt an Regelumsetzer, wartet auf die Prozessphase und trägt
  keine Stellungnahme von dir. Es steht zu Recht bei „Wartet auf die Prozessphase“.
- Dazu F1 in [4621](4621-datenmodellDerKatalogwerte.md) (nach Moderation erst nach der
  Prüfung des Architekten): ebenfalls noch kein Anliegen an dich.

**Kosten.** Eine Frage ohne Anliegen fehlt im Dashboard und im Zähler; du siehst sie nur,
wenn du `handoff/moderation.md` liest ([Wir 5](../../prozess/praemissen/wir.md): du sollst
ohne Werkzeug verstehen, was bei dir liegt).

**F1 · Wie kommt die Frage zu 3780 und 3900 ins Dashboard?**
- A: Ich lege sie als Anliegen `Fragen` an dich an (Von Regelumsetzer); kein Code, sofort im
  Dashboard und im Zähler. Die Moderation legt künftig jede Frage so an, nicht im Fließtext
  (Ablauf, [Anliegen](../../prozess/ablauf/anliegen.md); Quelle: Anliegen 418). (Ich 1)
- B: Das Dashboard liest zusätzlich „Fragen an dich“ aus `handoff/moderation.md` und zeigt
  sie als Karten. Neuer Mechanismus und ein Format in der Moderation, das ein Skript
  verlässlich liest; Antworten könnte das Formular nicht entgegennehmen. (neu)
- Empfehlung A: Der Mechanismus Anliegen besteht schon, trägt Antwortfeld, Status und
  Zähler; B baut eine zweite Quelle für dasselbe. Folge von A: die Moderation muss sich
  daran halten (nur Text, Moderator-Auftrag). Rückweg beider: das neue Anliegen löschen
  oder `erledigt` setzen; bei B die Dateien einzeln zurücknehmen (`git revert`).
Antwort: A

**Stellungnahme.**
Kommentar: Wichtig ist, dass ihr euch an die Prämissen in der KOmmunikation mit mir haltet, wenn es Fragen an mich gibt.
Stellungnahme: Die Frage zu 3780 und 3900 steht jetzt als [5110](5110-3780Und3900JetztOderInDerProzessphase8.md) im Dashboard und im Zähler. Zu deinem Kommentar: Die Regel steht schon (der Moderator stellt keine eigenen Fragen und verlinkt sie, [Moderator](../../.claude/agents/moderator.md), [Status](../../prozess/ablauf/anliegenStatus.md)); der Verstoß lag im Lauf. Eine Prüfung der Moderation baue ich, sobald es wieder vorkommt. Den Absatz „Offen, ohne eigene Frage“ ersetzt der Moderator beim nächsten Lauf durch den Link auf 5110.
