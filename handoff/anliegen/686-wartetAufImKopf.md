# Wartende Anliegen: Kopf erlaubt „wartet auf“, der Stand nennt sie nicht als dran

686 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) verlangt im Kopf
`· wartet auf <nr>`, solange erst ein anderes Anliegen erledigt sein muss;
`anliegenregeln/anliegen.py` meldet es rot. Gemeldet vom Koordinator; eingetreten bei 384
(wartete auf 385) und jetzt bei [421](421-schritteAbhaken.md), das auf
[490](490-fortschrittInPlanReviewRetro.md) wartet. Dazu die Antwort des Stakeholders in
Anliegen 630, F2 A: Anliegen an dich oder mich außerhalb der Prozessphase tragen
`· wartet auf die Prozessphase`, außer sie halten das Produkt auf. Heute nennt der Stand
beide Arten als dran.

**Kosten.** Der Stand schickt Rollen zu Anliegen, die nicht weitergehen können; in Zyklus 5
liefen Regelumsetzer und ich so neben dem Produkt (Anliegen 630, Befund 2). Wer den Kopf
nach dem Ablauf schreibt, macht die Prüfungen rot.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): die Zeilen zu `anliegenregeln/anliegen.py`
und `anliegenregeln/anliegenDran.py` in [Regeln](../../prozess/regeln.md#anliegenregeln),
der Backlogpunkt zum Kopf nach Anliegen 254 (in diesem Anliegen aufgegangen, bis auf
`beantwortetDurchFreigabe`).
1. `anliegen.py` lässt am Ende der Kopfzeile `· wartet auf <nr>` und
   `· wartet auf die Prozessphase` zu, dazu die Form `Auftrag`.
2. `anliegenDran.py`: Ein Anliegen mit `· wartet auf <nr>` ist für niemanden dran, solange
   `<nr>` im Ordner liegt; mit `· wartet auf die Prozessphase`, solange die Phase nicht
   läuft (`standregeln/phasenfolge.py`). Der Stand zählt es unter „wartet“ statt unter „Dran“.

Erledigt, wenn Scheiter-Tests zeigen: beide Endungen und `Auftrag` grün, `· wartet auf x`
rot; ein Anliegen, das auf ein vorhandenes wartet, ist nicht dran, nach dessen Löschen
wieder; eins, das auf die Prozessphase wartet, ist in der Technikphase nicht dran, in der
Prozessphase dran. Die Zeilen in Regeln stehen; den Vermerk im Ablauf setze ich.
Prozess-Item P2 der [Retro 5](../retro.md).

**Stellungnahme.**
