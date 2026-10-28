# Status der Anliegen

Der Status ist der letzte Zug; daraus folgt, wer dran ist. Kopf und Runden:
[Anliegen](anliegen.md).

Zug | setzt | Status | dann dran
---|---|---|---
stellen, neue Runde, Klärung | Absender | offen | Empfänger
nachfragen | Empfänger | rückfrage | Absender: klären
umsetzen, beantworten | Empfänger | angenommen | Absender: nachprüfen
widersprechen, Frage verwerfen | Empfänger, mit Begründung | abgelehnt | Absender: neue Runde oder `erledigt`
nach Runde 3/3 weiter uneins | Absender | eskaliert | Stakeholder: entscheidet
abschließen | Absender | erledigt | niemand: `anliegenregeln/erledigteLoeschen.py` löscht die Datei

Seine Züge in einem Anliegen setzt der Stakeholder im Formular des Dashboards: Es bietet nur
die Status an, die ihm die Tabelle zuweist, und je Frage ein Feld für die Antwort; eine
Legende im Anliegen entfällt (Anliegen 420). Mechanismus: `rollenregeln/dashboardAnliegenSeiten.py`
(`formular`), `rollenregeln/zuegeUebernehmen.py` ([Rollenregeln](../regeln/rollenregeln.md)).
Das Dashboard zeigt jedes nicht erledigte Anliegen als Karte ohne Eingabefeld, in Bereichen:
dran je Rolle samt fälliger Nachprüfung, wartet auf ein Anliegen, vorgemerkt je folgende Phase
in der Reihenfolge der Rotation. Kommentiert wird im Formular, wenn er das Anliegen öffnet
(Anliegen 1670, 2060). Mechanismus: `rollenregeln/dashboardAnliegen.py`,
`rollenregeln/dashboardAnliegenSeiten.py` ([Rollenregeln](../regeln/rollenregeln.md)).
Ein `Kommentar:` von ihm, der den Status nicht ändert, geht an die andere Rolle des Anliegens:
Sie antwortet mit einer Zeile `Stellungnahme:` darunter und ist bis dahin dran (Anliegen
384). Mechanismus: nur Text.
Die Moderation verlinkt Fragen, er antwortet im Anliegen; ihre Vorschläge korrigiert er mit
einer Zeile `Kommentar:` darunter ([Moderator](../../.claude/agents/moderator.md)). Mechanismus:
nur Text.

- Runde 3/3 ist die letzte: Der Zähler verhindert, dass zwei Rollen endlos diskutieren.
  Wäre danach eine weitere Runde nötig, setzt der Absender `eskaliert`; auch eine Hebung
  wählt dann der Stakeholder. Er schreibt seine Entscheidung ins Anliegen: zurück auf
  `Runde 1/3 · offen` oder eine andere Anweisung. Die Runde senkt und `eskaliert` ändert nur
  er; mit seiner Entscheidung setzt er auch den Kopf, sonst bleibt er dran. Mechanismus:
  `anliegenregeln/anliegen.py` (Runde höchstens 3), `anliegenregeln/anliegenDran.py` (bei
  `eskaliert` ist der Stakeholder dran); wer Runde und Status ändert, nur Text.
- Reicht der Empfänger einen Teil an eine andere Rolle weiter, setzt er `angenommen` erst,
  wenn jenes Anliegen erledigt ist; bis dahin trägt der Kopf `Wartet auf: <nr>`. Baut ein
  Prozess-Item den Mechanismus, setzt er `angenommen`, sobald die Regel steht, und seine
  Stellungnahme nennt das Item: `erledigt` folgt dessen Haken im Fortschritt der Retro
  (Anliegen 1570). Mechanismus: nur Text.
- Den Status setzt, wem die Tabelle ihn zuweist. Der Empfänger setzt nie `erledigt`, das
  setzt der Absender nach seiner Nachprüfung (Anliegen 1581, 1591). Ist der Koordinator
  Absender, der keine Datei schreibt, beauftragt er die Nachprüfung: Sie macht ein Kritiker
  des geänderten Artefakts nach der [Kritik](kritik.md), hat es keinen, der
  Organisationsentwickler, ist dieser Empfänger, der Architekt. Er setzt `erledigt`,
  Absender bleibt der Koordinator (Anliegen 6900). Mechanismus: nur Text.
- Wer `angenommen`, `abgelehnt` oder `rückfrage` setzt, schreibt in der letzten Runde eine
  Stellungnahme mit Text: was umgesetzt ist und wo, die Begründung oder die Frage; dem
  Stakeholder genügen seine Antworten. Eine Stellungnahme in einer früheren Runde zählt
  nicht. Mechanismus: nur Text.
- Die Nummer ist eindeutig, der Absender eines Anliegens ändert sich nie; wer eine Nummer
  belegt vorfindet, nimmt die nächste freie. Mechanismus: nur Text.
- Ist der Stakeholder Absender, nennt der Stand die fällige Nachprüfung; er trägt
  `erledigt` selbst ein. Mechanismus: `standregeln/stand.py`.
- Den Status eines Anliegens an ihn setzt der Stakeholder selbst; die Freigabe beantwortet
  keine Frage. Mechanismus: nur Text; abweichend nennt der Stand nach einer Freigabe den
  Absender als dran (`anliegenregeln/anliegenDran.py`, `beantwortetDurchFreigabe`).
- Niemand löscht ein committetes Anliegen von Hand; git ist das Archiv. Mechanismus:
  `anliegenregeln/erledigteLoeschen.py` (löscht erledigte), `rollenregeln/entfernen.py`
  (sperrt `rm` und `mv` committeter).
- Nach jedem Rollenlauf meldet ein Hook dem Koordinator die geänderten Status und wer dran
  ist, mit dessen Belegung. Mechanismus: `standregeln/stand.py` (PostToolUse auf Agent)
  nennt, wer dran ist und welche Nachprüfung fällig ist; geänderte Status und Belegung nur
  Text.
- Der Koordinator beauftragt die Rolle, die dran ist: Lief sie in diesem Chat und liegt ihre
  Belegung unter 120.000 Token, setzt er sie mit `SendMessage` fort, sonst startet er sie
  neu. Ein Anliegen, das aufhält ([Kritik](kritik.md)), bearbeitet der Empfänger in
  jeder Phase; die übrigen tragen `Wartet auf: <Phase>` seiner Perspektive.
  Mechanismus: Wartende sind nicht dran, `anliegenregeln/anliegenDran.py`; ob ein Anliegen
  aufhält: nur Text.
