# Umbenennung aus 7800 hat keinen Schritt im Fortschritt

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder hat in [7800](7800-karteUndEbeneBenennen.md) entschieden: *Karte*
heißt *Spielfeld* (F1 A), *Ebene* bleibt mit *Einheitenebene* und *Modellebene* (F2 B), als
Aufräumen am Ende einer Technikphase, ohne laufende Arbeit zu unterbrechen (F3).
[Plan 10](../plan.md) nennt es unter „Danach: Aufräumen aus Anliegen der Technikphase 10 und
7800“, der Schritt „Anforderungsautor: Anliegen 7800“ ist aber seit der Freigabe abgehakt,
und keiner der offenen Schritte benennt um. Glossar, Anforderungen und Code sagen weiter
*Karte* und *Ebene*.

**Kosten.** Ohne Schritt fällt die Umbenennung vor Review 10 aus; die Stellen wachsen mit
jedem Item (7800: damals rund 240 Stellen für *Karte*, 450 für *Ebene*). Setze ich 7800 jetzt `erledigt`,
löscht die Prüfung die Datei mit den Antworten.

**Gegenvorschlag.** Nimm nach Item ruhigeKarte und vor „Reviewer: DoD über das Inkrement“
Schritte auf: Anforderungsautor benennt Glossar und Anforderungen um, Stakeholder das
[Ziel](../../domaene/ziel.md) (F1 A), Testautor und Implementierer Tests und Code. Bis dahin
wartet 7800 auf dieses Anliegen.

**Stellungnahme.** Umgesetzt mit fünf Anliegen, die auf die Technikphase 10 warten; jedes ist
eine Zeile im [Fortschritt](../plan.md) vor der DoD und nennt, wann (nach Item ruhigeKarte):
Glossar und Anforderungen [11820](11820-umbenennenGlossarUndAnforderungen.md) (du, zuerst), dann
Tests [11821](11821-umbenennenTests.md), Code [11822](11822-umbenennenCode.md), Architektur
[11823](11823-umbenennenArchitektur.md), Ziel [11824](11824-umbenennenZiel.md) (Stakeholder).
Items und Etappen benenne ich mit 11820 um. Ein Item statt der Anliegen hätte den freigegebenen
Plan geändert und ohne Kriterium keine Zeile für Tests und Code. Lass 7800 auf 11820 statt auf
dieses Anliegen warten.
