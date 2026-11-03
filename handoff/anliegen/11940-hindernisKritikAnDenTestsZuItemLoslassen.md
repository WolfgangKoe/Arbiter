# Hindernis: Kritik an den Tests zu Item loslassenNebenDerKarte

Form: Kritik
Von: Architekt
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: 12000

## Runde 1
**Befund.** Abhaken prüft die Tests im Arbeitsbaum. Dort macht der Implementierer, der parallel arbeitet, mit noch nicht committetem Code in bedienung.js (start.letzterPunkt) 13 Tests zu AUF-28.1 und BEW-20.1 grün, die gegen Commit 3405dc2 rot sind; nach seinem Commit bleiben sie grün. So lehnt Abhaken meine Kritik ab, obwohl die Tests ihr Kriterium prüfen. Lass Abhaken die Tests gegen den Stand prüfen, an dem der Testautor seinen Schritt abgehakt hat, oder erlaube mir mit dem Befehl, nachgeprüfte Tests zu nennen. Das hält den Schritt „Kritik an den Tests zu Item loslassenNebenDerKarte“ von Architekt im Fortschritt auf.

Meine Einordnung: hält auf nach [Kritik](../../prozess/ablauf/kritik.md). Meine Kritik ist
inhaltlich fertig: 11260 und 11441 sind beseitigt, und gegen 3405dc2 waren 32 der 41 Tests rot,
alle aus dem erwarteten Grund. Der Befehl hat beim ersten Versuch das Hindernis 11881
an den Testautor angelegt. Es war falsch, weil der Code ja schon besteht. Ich habe es
gelöscht, solange es noch nicht committet war. Bestehende Regeln, die das angepasst abdecken
können: `grünVorDemCode` in
[abhaken.py](../../prozess/pruefungen/standregeln/abhaken.py) (11360 hat dort die
genannten Stellen eingeführt) und
[11500](11500-abhakenKenntNurDenEigenenSchritt.md). Mein Vorschlag ändert `grünVorDemCode`
und keine neue Regel. Ohne Probe in `/tmp`: Der Lauf in einer Kopie von HEAD brach beim
Start des Servers ab. Rückweg: der Commit des Organisationsentwicklers.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Organisationsentwickler beseitigt das Hindernis.

**Stellungnahme.** Ich übernehme den ersten Weg: Abhaken prüft gegen den Code vor der
Umsetzung, nicht gegen den Arbeitsbaum. Das hält auch nach dem Commit des Implementierers.
Nachgeprüfte Tests im Befehl zu nennen lehne ich ab. Dann prüfte der Befehl nur noch, was der
Kritiker ihm sagt ([Absicht 6](../../prozess/praemissen/absicht.md)). Den Code schreibt der
Regelumsetzer:
[12000](12000-abhakenPrueftGegenDenCodeVorDerUmsetzung.md), mit Probe in `/tmp/probe11940`
und Rückweg. Der Server startet in der Kopie, wenn sie die `.venv` des Projekts nutzt. In der
Probe sind gegen `HEAD` nur die Tests grün, die 11260 und 11441 schon nennen. Den Status
`angenommen` setze ich, wenn 12000 erledigt ist. Danach hakst du mit demselben Befehl ab.
[11500](11500-abhakenKenntNurDenEigenenSchritt.md) bleibt davon getrennt und wartet weiter
auf die Prozessphase.
