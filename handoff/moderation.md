# Moderation

Stand: Zyklus 3, Domänenphase; [Plan 3](plan.md) wartet auf Freigabe. 31 Anliegen offen, 235 und 236 erledigt.

## Dran
Blockiert Plan 3 (DoR in [Ablauf](../prozess/ablauf.md#dor-item-bereit)):
- DoR 4 und 5, beide Items: [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) F1 (UX benennt danach um).
- Item 2: [239](anliegen/239-durchmesserInDerAblageZeigen.md) F1; [237](anliegen/237-durchmesserInDerAblage.md) wartet darauf (Kriterium AUF-4.8 oder Mockups ohne Zahl).
- Blockiert das Inkrement, nicht die Freigabe: [234](anliegen/234-flaskUndPlaywrightFehlen.md) (Regelumsetzer), [233](anliegen/233-frontendOhneAutor.md) (wartet auf [238](anliegen/238-implementiererSchreibtFrontend.md) F1), 153 (Architekt). Alle drei vor dem Wegwerf-Versuch des Architekten und dem Testautor.

Je Rolle:
- Stakeholder: Fragen unten.
- UX: 223 nach F1 umbenennen; bei 239 B die Mockups ohne Zahl.
- Anforderungsautor: 237 nach 239 (AUF-4.8 oder nicht).
- Architekt: Kritik an Plan 3 ist als 233 bis 237 eingegangen; [227](anliegen/227-pruefskriptPfadeInDerArchitektur.md); 153.
- Planer: 235 und 236 erledigt; Plan 3 nach 239 nachziehen (AUF-4.2 bis AUF-4.7).
- Regelumsetzer, Reihenfolge (215 bis 221 deine Vorgabe):
  1. [215](anliegen/215-bashSandboxAlsVersuch.md), 2. [216](anliegen/216-commitHooksWirksamMachen.md), 3. [218](anliegen/218-freigabesperreInZweiSchritten.md), 4. [220](anliegen/220-stellungnahmePruefen.md), 5. [221](anliegen/221-architekturmassZaehltNurOberste.md).
  6. [229](anliegen/229-starterNurFuerPruefskripte.md), 7. [232](anliegen/232-wurzelEinmalHerleiten.md), 8. [231](anliegen/231-pruefungenSehenUnterordnerNicht.md), 9. [228](anliegen/228-suchpfadPytestGleichStarter.md), 10. [230](anliegen/230-hooktestUebersiehtModuleNotFound.md) (Gründe: 229 nach 215, 232 nach 229, 231 nutzt 232, 230 nach 216 und 228).
  11. [114](anliegen/114-pruefskripteOrdnenUndLesbarMachen.md), danach [202](anliegen/202-histogrammTestUndAchsenmarke.md) bis [206](anliegen/206-absenderpruefungNachschliff.md).
  234 fehlt in dieser Folge (F3).
- Organisationsentwickler: 233 (nach 238), [219](anliegen/219-angenommenOhneStellungnahme.md) (nach 220), [226](anliegen/226-pruefskriptPfadeInDenDokumenten.md) (nach 227), [107](anliegen/107-kritikAnDenPruefungen.md), [138](anliegen/138-anliegenPerSkriptAmBashSchutzVorbei.md) (nach 215), [150](anliegen/150-sonarlintAbdeckungUndToterCode.md).
- Testautor: wartet (AUF-4, QUE-2).

## Vorschläge
- Zusammen (Regelumsetzer): 229 mit 232; 228 mit 230; 231 mit 232 und 234 (`konfigurationTest.py`); 204 mit 205. Je Lauf ein Anliegen bleibt (Belegung).
- 237 und 239 sind dieselbe Frage; 237 schließt der Anforderungsautor nach 239.
- Schließen: 235, 236 (Löschen nach Erledigt); 225 bei F1 a; 226 nach 227; 138 folgt 215; 107 folgt 114.

## Fragen an dich
Die Freigabe von Plan 3 beantwortet jede mit der Empfehlung.
- [223](anliegen/223-mockupsBenennungUndZonenfarbe.md) F1: deutsche Namen nach Glossar auch für Komponenten aus Arbiter-old (A); blockiert die Mockups.
- [239](anliegen/239-durchmesserInDerAblageZeigen.md) F1: Ablage zeigt den Durchmesser jedes Modells, neues Kriterium AUF-4.8 (A).
- [238](anliegen/238-implementiererSchreibtFrontend.md) F1: Der Implementierer schreibt `technik/frontend/` (A); 233 wartet darauf.
- [225](anliegen/225-pythonpathErlaubnisEntfaellt.md) F1: Ausnahme aus 114 erledigt, Erlaubnis wird nie angelegt (a).
- [153](anliegen/153-frontendBackendUndDatenbank.md) F1: Datenbank erst mit der ersten Handlung (A).
- [Moderation](moderation.md) F1: 228 bis 232 hinter 221 in der Folge 229, 232, 231, 228, 230? Empfehlung: ja.
- [Moderation](moderation.md) F2: 114 und 202 bis 206 nach 215 bis 221? Empfehlung: ja.
- [Moderation](moderation.md) F3: [234](anliegen/234-flaskUndPlaywrightFehlen.md) als Erstes nach der Freigabe, vor 215? Es blockiert das Inkrement, keines der anderen tut es. Empfehlung: ja.
