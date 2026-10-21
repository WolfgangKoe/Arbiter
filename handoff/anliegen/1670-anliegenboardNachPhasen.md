# Anliegenboard nach Phasen, Kopf als Felder

1670 · Auftrag · von Stakeholder → Organisationsentwickler · Runde 1/3 · angenommen

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

Bestehende Regeln, die das berühren ([Ich 4](../../prozess/praemissen/ich.md)):
- Kopf und Status: [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen), geprüft von
  `anliegenregeln/anliegen.py`; Köpfe schreiben auch `standregeln/hindernis.py` und das
  Formular des Dashboards (`rollenregeln/dashboardAnliegenSeiten.py`).
- Das Dashboard zeigt je Rolle nur, wer dran ist, und fällige Nachprüfungen
  (`rollenregeln/dashboardAnliegen.py`, `zuständige`); was `anliegenregeln/anliegenDran.py`
  (`wartet`) als wartend erkennt, fehlt. In der Technikphase 6 sind das 20 Anliegen, dieses mitgezählt.
- Verwandt: [1070](1070-wartendeNachpruefungIstNichtFaellig.md) (wartende Nachprüfung gilt
  als fällig).

**Kosten.** Der Stakeholder sieht vorgemerkte Anliegen nur in `handoff/`, nicht im Dashboard,
und kann sie dort nicht kommentieren. Ein Kopf in einer Zeile mit sechs Teilen ist schwer zu
lesen, und jedes Skript, das ihn liest oder schreibt, zerlegt ihn selbst.

**Gegenvorschlag.** Fragen an die Prozessphase; den Mechanismus baut der Regelumsetzer:
1. Welche Bereiche zeigt das Board: jetzt dran, wartet auf ein anderes Anliegen, vorgemerkt
   je folgende Phase in der Reihenfolge der Rotation?
2. Welche Felder hat der Kopf, je Zeile eines, und wer liest und schreibt sie an einer Stelle
   (ein Lese- und Schreibmodul statt Muster in jedem Skript)?
3. Wie kommen die offenen Anliegen in die neue Form: ein Lauf, der alle Köpfe umschreibt?
4. Welche Felder kann der Stakeholder im Formular setzen, auch für Vorgemerktes?

**Stellungnahme.** Angenommen, [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen); den
Mechanismus baut der Regelumsetzer mit P4. 1: dran je Rolle samt Nachprüfung, wartet auf ein
Anliegen, vorgemerkt je Phase nach der Rotation. 2: `Form:`, `Von:`, `An:`, `Runde:`,
`Status:`, `Wartet auf:` je Zeile, die Nummer nur im Dateinamen; ein Modul liest und schreibt.
3: ein Lauf schreibt alle offenen Köpfe um. 4: Kommentar überall, Status und Antwort wie bisher.
