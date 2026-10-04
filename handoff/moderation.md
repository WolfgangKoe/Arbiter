# Moderation

Stand: Zyklus 3, Domänenphase; [Plan 3](plan.md) wartet auf Kritik des Architekten und Freigabe. 25 Anliegen offen.

## Dran
Blockiert Plan 3 (DoR in [Ablauf](../prozess/ablauf.md#dor-item-bereit)):
- DoR 5, beide Items: [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) wartet auf deine Antwort F1; UX benennt die Mockups erst danach um (Befund 2 und 3 sind umgesetzt).
- Vor dem Testautor: Aufbau aus [153](anliegen/153-frontendBackendUndDatenbank.md) (Architekt, Technikphase).

Je Rolle:
- UX: [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) nach F1 umbenennen.
- Architekt: Kritik an Plan 3; [227](anliegen/227-pruefskriptPfadeInDerArchitektur.md) (Pfade in `architektur.md`); 153.
- Stakeholder: [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) F1, [225](anliegen/225-pythonpathErlaubnisEntfaellt.md) F1.
- Regelumsetzer, nichts davon blockiert ein Item. Reihenfolge, 215 bis 221 wie von dir vorgegeben, die neuen danach:
  1. [215](anliegen/215-bashSandboxAlsVersuch.md) Sandbox.
  2. [216](anliegen/216-commitHooksWirksamMachen.md) Commit-Hooks.
  3. [218](anliegen/218-freigabesperreInZweiSchritten.md) Freigabesperre.
  4. [220](anliegen/220-stellungnahmePruefen.md) Stellungnahme prüfen; 219 wartet darauf.
  5. [221](anliegen/221-architekturmassZaehltNurOberste.md) Höchstmaß Architektur.
  6. [229](anliegen/229-starterNurFuerPruefskripte.md) Starter prüft Eingabe; Punkt 3 ändert `bashPositivliste.py` nach 215, Punkt 1 liefert die Funktion für 232.
  7. [232](anliegen/232-wurzelEinmalHerleiten.md) Wurzel einmal; nach 229, vor 231.
  8. [231](anliegen/231-pruefungenSehenUnterordnerNicht.md) Prüfungen sehen Unterordner nicht; nutzt `prüfskripteOrdner` aus 232.
  9. [228](anliegen/228-suchpfadPytestGleichStarter.md) Suchpfad pytest gleich Starter.
  10. [230](anliegen/230-hooktestUebersiehtModuleNotFound.md) Hook-Test; nach 216 und 228 (beide Hook-Prüfung und Import).
  11. [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md), danach [202](anliegen/202-histogrammTestUndAchsenmarke.md) bis [206](anliegen/206-absenderpruefungNachschliff.md), wie zuvor.
- Organisationsentwickler: [219](anliegen/219-angenommenOhneStellungnahme.md) (nach 220), [226](anliegen/226-pruefskriptPfadeInDenDokumenten.md) (nach 227), [107](anliegen/107-kritikAnDenPruefungen.md), [138](anliegen/138-anliegenPerSkriptAmBashSchutzVorbei.md) (nach 215), [150](anliegen/150-sonarlintAbdeckungUndToterCode.md).
- Reviewer: Code zu den Commits der Regelumsetzer-Läufe.
- Testautor: wartet (AUF-4, QUE-2).

## Vorschläge
- Planer: [Plan 3](plan.md) nachziehen; 195 und 151 sind nicht mehr offen, der Verweis auf 151 F2 stimmt nicht mehr. Erst nach 223.
- Zusammen (Regelumsetzer): 229 mit 232 (`lauf.py`); 228 mit 230 (Import und Hook-Test); 231 mit 232 (`konfigurationTest.py`). 204 mit 205 (`agenten.py`, `pfade.py`). Je Lauf ein Anliegen bleibt (Belegung).
- Schließen: 225 erledigt, wenn du F1 a wählst (Stakeholder); 226 nach 227 (Organisationsentwickler); 138 und 215 sind dasselbe Thema, 138 folgt 215; 107 folgt 114.

## Fragen an dich
Die Freigabe von Plan 3 beantwortet jede mit der Empfehlung.
- [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) F1: deutsche Namen nach Glossar auch für die Komponenten aus Arbiter-old (A); blockiert die Mockups.
- [225](anliegen/225-pythonpathErlaubnisEntfaellt.md) F1: Ausnahme aus 114 ist erledigt, die Erlaubnis wird nie angelegt (a).
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1: Datenbank erst mit der ersten Handlung (A); Aufbau prüfst du vor der Technik.
- [Moderation](moderation.md) F1: Kommen 228 bis 232 hinter 221, in der Reihenfolge 229, 232, 231, 228, 230 (nach Abhängigkeit)? Empfehlung: ja.
- [Moderation](moderation.md) F2: Laufen 114 und 202 bis 206 nach 215 bis 221? Empfehlung: ja.
