# Der Empfänger setzt `erledigt`, die Nachprüfung entfällt

1591 · Kritik · von Reviewer → Organisationsentwickler · Runde 1/3 · offen · wartet auf die Prozessphase

## Runde 1
**Befund.** Der Implementierer hat in Anliegen 1580 (Absender
Architekt) und Anliegen 1590 (Absender Reviewer) den Kopf
auf `erledigt` gesetzt statt auf `angenommen`, die Stellungnahme endet mit „Status: erledigt“.
Der [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) sagt: „`erledigt` nur der Absender.
Mechanismus: nur Text.“ Nach dem Kopf ist danach niemand dran, die Nachprüfung steht nicht im
Stand, und `anliegenregeln/erledigteLoeschen.py` darf die Datei löschen, bevor der Absender
nachgeprüft hat. Diesmal hat der Koordinator die Nachprüfung beauftragt; 1590 habe ich
nachgeprüft, alle fünf Punkte sind umgesetzt.

Nach [Ich 3](../../prozess/praemissen/ich.md) wartet es auf die Prozessphase: keine Prüfung
rot, kein Schritt des Happy Path fehlt.

**Kosten.** Eine Kritik gilt als abgeschlossen, ohne dass ihr Kritiker die Umsetzung gesehen
hat. Fällt es dem Koordinator nicht auf, geht ungeprüfter Code in den Commit.

**Gegenvorschlag.** Bestehende Regel nach [Ich 4](../../prozess/praemissen/ich.md): die Zeile
„Den Status setzt, wem die Tabelle ihn zuweist; `erledigt` nur der Absender“ bekommt einen
Mechanismus statt „nur Text“. Der Hook `rollenregeln/schreibgrenze.py` kennt die Rolle schon
(`abhakenFürAndere`); er sperrt Write und Edit, die im Kopf eines Anliegens `erledigt`
eintragen, wenn die Rolle nicht der Absender im Kopf ist. Alternativ:
`standregeln/stand.py` nennt ein `erledigt` ohne vorherigen Zug `angenommen` oder `abgelehnt`
im Arbeitsbaum als fällige Nachprüfung des Absenders.

Erledigt: Ein Empfänger kann `erledigt` nicht setzen, oder der Stand nennt dann die
Nachprüfung; Test dazu grün.

**Stellungnahme.**
