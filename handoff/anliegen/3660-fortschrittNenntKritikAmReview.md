# Der Fortschritt nennt die Kritik am Review nicht

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Mit Retro 7, P1 kritisieren Fachkritiker und Organisationsentwickler ein Review
([Ablauf, Kritik](../../prozess/ablauf/kritik.md); Technikphase 7). Die Tabelle im
[Fortschritt](../../prozess/ablauf/fortschritt.md) hat dafür in „Technik 6, 7“ die Zeilen
`je Kritiker: Kritik am Review`, abgehakt per Befehl. `standregeln/fortschritt.py` schreibt
nach „Reviewer: Review geschrieben“ gleich „Stakeholder: Freigabe Review <n>“
(`fortschritt.py:100–102`); die Zeilen fehlen, im Ablauf stehen sie als „nur Text“.

**Kosten.** In Technikphase 8 nennt der Stand nach dem Review gleich die Freigabe; der
Koordinator beauftragt die Kritiker nicht, und `abhaken.py` findet ihren Schritt nicht.
Ein Review ginge wieder ohne Kritik zur Freigabe; in Zyklus 7 fing sie vier fehlende Dateien
im Rundgang ab (3250).

**Gegenvorschlag.** Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): die Zeilen
der Kritik an der Retro (`je Kritiker`, Befehl) für das Review wiederverwenden. In
`fortschritt.py` nach „Review geschrieben“ je Kritiker der Tabelle (Fachkritiker,
Organisationsentwickler) „Kritik am Review“ ohne Fakt, mit Scheiter-Test. Geliefert mit
P5 (Läufe und Anliegenkopf), weil P5 dort schon den neu gefassten Plan mit seiner Kritik
ändert; dann ersetze ich „nur Text“ im Ablauf. Erledigt, wenn der Stand die beiden Zeilen
nach „Review geschrieben“ nennt und der Befehl sie abhakt.

**Stellungnahme.** Umgesetzt mit Retro 7, P5: `standregeln/fortschritt.py` schreibt nach „Review geschrieben“ die Zeilen „Kritik am Review“ für Fachkritiker und Organisationsentwickler; der Befehl hakt sie ab. Test: `standregeln/fortschrittTest.py` (`testNachDemReviewFolgtJeKritikerDieKritikAmReviewVorDerFreigabe`); Regel in [Standregeln](../../prozess/regeln/standregeln.md). „nur Text“ im Ablauf ersetzt der Organisationsentwickler.
