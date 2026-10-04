# Moderation

Stand: Zyklus 3, Domänenphase; [Plan 3](plan.md) wartet auf Mockups, Kritik des Architekten und Freigabe. P1 bis P5 der [Retro](retro.md) sind durch (der Stand meldet die Domänenphase). 23 Anliegen offen.

## Dran
Abhängigkeiten, die Plan 3 betreffen (DoR in [Ablauf](../prozess/ablauf.md#dor-item-bereit)):
- DoR 5, blockiert beide Items: Mockups zu QUE-2 und AUF-4 fehlen (`domaene/mockups/` gibt es nicht). UX schreibt sie; ihr Platz ist festgelegt durch [151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md) F2 (offen) und das CSS-Angebot aus DoR 5, denn eine Komponentenseite gibt es erst in der Technikphase.
- DoR 4, blockiert beide Items: [195](anliegen/195-karteUndAblageBegriffeUndNamen.md) ist beantwortet (F3: A, AUF-4.2 gilt unverändert); der Anforderungsautor schließt es.
- Vor dem Testautor, nicht vor der Freigabe: Aufbau aus [153](anliegen/153-frontendBackendUndDatenbank.md) und Aufteilung der Architektur ([212](anliegen/212-architekturHatZeichenNichtBytes.md)); beides macht der Architekt in der Technikphase.

Je Rolle:
- UX: Mockups zu QUE-2 und AUF-4, höchstens 8.000 Zeichen je Datei. Ohne [200](anliegen/200-pruefungDerMockups.md) sind die Grenzen nur Text.
- Anforderungsautor: 195 abschließen.
- Architekt: Kritik an Plan 3 und den Mockups; 212 nachprüfen. 211 wartet nicht auf die Aufteilung.
- Regelumsetzer, in dieser Reihenfolge: 200 (vor den Mockups), [210](anliegen/210-freigabefeldNurImAbschnittLesen.md) und [208](anliegen/208-freigabeReviewBeantwortetFragen.md) (der Stand kann sonst die Freigabe falsch melden), [211](anliegen/211-hoechstmassDerArchitektur.md), [173](anliegen/173-prozessItemsVorDemNaechstenPlan.md) (scheint umgesetzt, Status klären), [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md) (Teil A freigegeben, a), dann [202](anliegen/202-histogrammTestUndAchsenmarke.md) bis [206](anliegen/206-absenderpruefungNachschliff.md). Nichts davon blockiert ein Item.
- Organisationsentwickler: [207](anliegen/207-absenderRegelImAblauf.md), [107](anliegen/107-kritikAnDenPruefungen.md), [138](anliegen/138-anliegenPerSkriptAmBashSchutzVorbei.md) (wartet auf 139), [150](anliegen/150-sonarlintAbdeckungUndToterCode.md); Nachprüfung 139, 151, 168.
- Reviewer: Kritik am Code zu b2a5221; läuft parallel an 168.
- Testautor: wartet (AUF-4, QUE-2).

## Vorschläge
- Planer: [Plan 3](plan.md) nachziehen; „Noch nicht bereit“ nennt 195 offen und die UX-Rolle wartend, die Liste der offenen Anliegen nennt 155 und 159, die erledigt sind, und nicht 151 F2. Erst nach den Mockups, sie gehören an die Items.
- Zusammen (Regelumsetzer): 208 mit 210 (`freigabeKommentare.py`, `gitAufruf.py`, Teile von 167); 204 mit 205 (Altbestand und Oberordner, `agenten.py`, `pfade.py`); 200 mit 211 (`hoechstmassTest.py`). Je Lauf ein Anliegen bleibt (Belegung).
- 206 und 207 betreffen beide die Absenderregel aus 166; 207 (Ablauf) zuerst, dann 206.
- Schließen: 195 (Anforderungsautor), 212 (Architekt, nach Nachprüfung), 173 falls umgesetzt (Regelumsetzer setzt `angenommen`, Organisationsentwickler `erledigt`). 107 folgt 114, 150 erledigst du nach P1 und P2.

## Fragen an dich
Die Freigabe von Plan 3 beantwortet jede mit der Empfehlung.
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1: Datenbank erst mit der ersten Handlung (A). Dazu prüfst du den Aufbau, bevor er in die Technik geht; ohne Runde 2 setzt der Architekt ihn so ein.
- [151](anliegen/151-rolleUxFuerDieErsteOberflaeche.md) F2: UX schreibt einbaufähig nach `domaene/mockups/` (A). Hängt an den Mockups von Plan 3.
- [139](anliegen/139-bashSandboxStattHeuristik.md) F2: Sandbox als Versuch (A). Wirkt nicht auf Plan 3; 138 wartet darauf.
- Hinweis zu [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md) F1: Deine Ausnahmeerlaubnis (a) soll nach der Abnahme entfallen; der Regelumsetzer schreibt das nicht von selbst.
