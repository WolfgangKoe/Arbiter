# Hindernis einer neuen Runde gilt sofort als beseitigt

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [beseitigt.py](../../prozess/pruefungen/standregeln/beseitigt.py), Zeile 30, liest
den Status des Anliegens aus `HEAD`. Öffnet ein Kritiker eine neue Runde, ist sie noch nicht
committet; in `HEAD` steht die vorige Runde auf `angenommen`. So bekam das neue Hindernis aus
Runde 2 von 8960 in [plan.md](../plan.md) gleich `beseitigt: Commit „Review 9 nach Kritik
nachgebessert, 8880 vom Stakeholder beantwortet“`, den Commit aus Runde 1, ebenso das aus
Runde 2 von 8950 (Commit „Nachprüfungen zu Review 9: 8950 und 8960 in Runde 2, 8880 wartet
auf Plan 10“). Der Stakeholder liest beide als erledigt, solange sie es nicht sind, und ein
Kritiker könnte schon abhaken ([Fortschritt](../../prozess/ablauf/fortschritt.md), Befehl).

**Kosten.** Ohne Änderung: Jede zweite Runde zeigt im Fortschritt den falschen Commit, so
wie jetzt bei 8950 und 8960. Änderung: ein Zug in `beseitigtDurch`, dazu ein Test.

**Gegenvorschlag.** Ein Hindernis gilt erst als beseitigt durch einen Commit, der nach der
Zeile `Hindernis:` kam: etwa nur, wenn der Status im Arbeitsstand ebenfalls `angenommen` oder
`erledigt` ist, oder wenn der Commit, der die Zeile ins plan.md brachte, älter ist als der
beseitigende.

**Stellungnahme.** Umgesetzt in Retro 9 P3 nach dem ersten Weg: [beseitigt.py](../../prozess/pruefungen/standregeln/beseitigt.py)
(`beseitigtDurch`) nennt einen Commit nur, wenn die Datei des Anliegens im Arbeitsstand gleich
`HEAD` ist und dort `angenommen` oder `erledigt` trägt; eine neue Runde oder ein noch nicht
committeter Status ergibt keinen Vermerk. Scheiter-Test in
[hindernisTest.py](../../prozess/pruefungen/standregeln/hindernisTest.py)
(`testEineNeueRundeLässtDasHindernisOffenBisIhrCommitDenStatusTrägt`). `erledigt` folgt dem Haken P3.
