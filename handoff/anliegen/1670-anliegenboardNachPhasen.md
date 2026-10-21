# Anliegenboard nach Phasen, Kopf als Felder

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wortlaut des Stakeholders: „Ich sehe in handoff ganz viele fertige Anliegen, die
korrekterweise nicht mehr im Dashboard angezeigt werden. Es gibt aber immer noch viele offene
Anliegen, die auf ihre Bearbeitung in der entsprechenden Phase warten. Diese Logik wird im
Dashboard noch nicht abgedeckt. Gerade die Funktion ‚wartet auf …‘ fehlt komplett, und so
entsteht Intransparenz im Dashboard. Ich bin fein damit, wenn erledigte Anliegen nicht
angezeigt werden, aber alles andere sollte sichtbar sein, damit ich es kommentieren kann.
Ggf. braucht es in der Anliegenliste eine Trennung in Bereiche, wenn etwas für eine der
folgenden Phasen vorgemerkt ist, weil es die aktuelle Phase nicht blockiert. Somit entsteht
eine Art ‚rotierendes Anliegenboard‘, rotierend im Sinne der Phasenrotation. Das bitte für
die jetzige Prozessphase mit in die Retro nehmen und eine Maßnahme planen. Im Zuge dessen
kann auch der Kopf der Anliegen übersichtlicher gestaltet werden, statt ‚1660 · Auftrag · von
Stakeholder → Organisationsentwickler · Runde 1/3 · offen · wartet auf die Prozessphase‘ eher
als Felder je Zeile: ‚1660 · Auftrag‘ / ‚von Stakeholder → Organisationsentwickler‘ / ‚Runde
1/3 · offen‘ / ‚wartet auf · die Prozessphase‘. Dann haben wir eine Art Felderlogik, die ich
besser lesen kann, wenn ich in den Code schaue, und die hilft, das Dashboard besser zu
warten. Mache hier gerne einen besseren Vorschlag. Einen Gegenvorschlag in Richtung ‚Lassen
wir es möglichst so, wie es jetzt ist‘ werde ich nicht akzeptieren. Wir müssen auch in den
Prozessen Stück für Stück effektiver und effizienter werden, so dass ausreichend Transparenz,
aber auch Ordnung gewährleistet ist.“

Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)): Kopf und Status in
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen); das Board zeigte nur, wer dran ist, und
fällige Nachprüfungen, keine wartenden Anliegen.

**Kosten.** Der Stakeholder sieht vorgemerkte Anliegen nur in `handoff/` und kann sie nicht
kommentieren. Ein Kopf in einer Zeile mit sechs Teilen ist schwer zu lesen.

**Gegenvorschlag.** Fragen an die Prozessphase; den Mechanismus baut der Regelumsetzer:
1. Welche Bereiche zeigt das Board?
2. Welche Felder hat der Kopf, und wer liest und schreibt sie an einer Stelle?
3. Wie kommen die offenen Anliegen in die neue Form?
4. Was kann der Stakeholder im Formular setzen?

**Stellungnahme.** Angenommen, [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen), gebaut
mit P4. 1: dran je Rolle samt Nachprüfung, wartet auf ein Anliegen, vorgemerkt je Phase nach
der Rotation. 2: `Form:`, `Von:`, `An:`, `Runde:`, `Status:`, `Wartet auf:` je Zeile, die
Nummer nur im Dateinamen; ein Modul liest und schreibt. 3: ein Lauf schrieb alle offenen Köpfe
um. 4: Kommentar, Status und Antwort im Formular auf der Seite des Anliegens.
Kommentar: Woran erkenne ich an diesem Anliegen, dass ich es auf "erledigt" setzen kann?
Stellungnahme: Wenn in der [Retro 6](../retro.md) „Regelumsetzer: P4“ abgehakt ist und das Dashboard die Bereiche aus 1 und die Köpfe aus 2 zeigt.
Kommentar: Ein Kommentar hierzu. Es ist zwar nett, dass ich überall Kommentare setzen darf. Aber diese Funktion ist mir hier etwas zu offensiv. Ich hätte alles lieber kompakter. einen Kommentar setze ich dann, wenn ich das ANliegen öffne. Die Fortschrittsliste darf auch etwas kompakter sein und neben dem Anliegenboard als kompakte Liste angeordnet sein.
Stellungnahme: Gebaut ([Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt)): Karten ohne Feld; rechts neben dem Board der Fortschritt als Liste, Haken per Klick, ein gesetzter als Feld mit ✓, nicht entfernbar, Zeilen mit Fakt gesperrt; das Kommentarfeld erst beim Klick auf den Text der Zeile.
