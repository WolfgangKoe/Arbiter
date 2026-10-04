# Moderation

Stand: Zyklus 3, Domänenphase; [Plan 3](plan.md) wartet auf Mockups, Kritik des Architekten und Freigabe. 21 Anliegen offen.

## Dran
Blockiert Plan 3 (DoR in [Ablauf](../prozess/ablauf.md#dor-item-bereit)):
- DoR 5, beide Items: Mockups zu QUE-2 und AUF-4 fehlen; Platz laut Anliegen 151 F2 (offen).
- DoR 4, beide Items: 195 ist beantwortet (F3: A); der Anforderungsautor schließt es.
- Vor dem Testautor: Aufbau aus [153](anliegen/153-frontendBackendUndDatenbank.md) und Anliegen 212 (Architekt, Technikphase).

Je Rolle:
- UX: Mockups zu QUE-2 und AUF-4, höchstens 8.000 Zeichen je Datei; Prüfung dazu in Anliegen 200.
- Anforderungsautor: 195 abschließen.
- Architekt: Kritik an Plan 3 und den Mockups; 212 nachprüfen.
- Regelumsetzer, nichts davon blockiert ein Item, Reihenfolge:
  1. Anliegen 200, vor den Mockups.
  2. Anliegen 210 mit Anliegen 213: `freigegebenerZyklus` aus 213 Punkt 6 ist die Funktion aus 210; 213 danach, denn 168 wartet darauf.
  3. [208](anliegen/208-freigabeReviewBeantwortetFragen.md) (`freigabeKommentare.py`, `gitAufruf.py` wie 210).
  4. [211](anliegen/211-hoechstmassDerArchitektur.md) (`hoechstmassTest.py` wie 200).
  5. [214](anliegen/214-prozessItemsKommentarUndVerweis.md): klein, schließt 173 ab; vor 205 (beide `phasenfolge.py`).
  6. [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md) Teil A (a); nach 213, beide ändern `bashPositivliste.py`.
  7. [202](anliegen/202-histogrammTestUndAchsenmarke.md) bis [206](anliegen/206-absenderpruefungNachschliff.md); 206 nach 213 und 207 (`statusrecht.py`, Absenderregel).
- Organisationsentwickler: Anliegen 207, [107](anliegen/107-kritikAnDenPruefungen.md), [138](anliegen/138-anliegenPerSkriptAmBashSchutzVorbei.md) (wartet auf 139), [150](anliegen/150-sonarlintAbdeckungUndToterCode.md); Nachprüfung 139, 151, 173, Anliegen 168 (erst nach 213).
- Reviewer: Code zu b2a5221 ist geprüft (213); Code zu 4792298 ebenso (214); als Nächstes die Commits zu 210/213.
- Testautor: wartet (AUF-4, QUE-2).

## Vorschläge
- Planer: [Plan 3](plan.md) nachziehen (195 und 151 F2 stimmen nicht mehr; 155, 159 sind erledigt), erst nach den Mockups.
- Zusammen (Regelumsetzer): 210 mit 213; 208 mit 210; 204 mit 205 (`agenten.py`, `pfade.py`); 200 mit 211. Je Lauf ein Anliegen bleibt (Belegung).
- 207 (Ablauf) vor 206.
- Schließen: 195 (Anforderungsautor), 212 (Architekt nach Nachprüfung), 173 nach 214 (Organisationsentwickler setzt `erledigt`). 107 folgt 114; 150 erledigt der Organisationsentwickler nach P1 und P2.

## Fragen an dich
Die Freigabe von Plan 3 beantwortet jede mit der Empfehlung.
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1: Datenbank erst mit der ersten Handlung (A); Aufbau prüfst du vor der Technik.
- Anliegen 151 F2: UX schreibt einbaufähig nach `domaene/mockups/` (A).
- Anliegen 139 F2: Sandbox als Versuch (A); 138 wartet darauf.
- Hinweis zu [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md) F1: Deine Ausnahmeerlaubnis (a) soll nach der Abnahme entfallen; der Regelumsetzer schreibt das nicht von selbst.
