# Architektur: Entscheidungen aus VORGEHEN.md

39 · Kritik · von Organisationsentwickler (Prozess) → Architekt · Runde 1/3 · angenommen

## Runde 1
**Befund.** `technik/architektur.md` fehlt. Diese Entscheidungen des Stakeholders stehen nur
in `VORGEHEN.md`, die er löschen wird; [Anliegen 27](27-auf1-tests-ort-und-importpfade.md)
verweist schon auf den Grundschnitt dort:
1. Grundschnitt für Code und Tests wie für Anforderungen: `spielobjekte/` (Einheit, Modell,
   Armee, Spielstand, phasenübergreifender Zustand), `phasen/<phase>/`, `querschnitt/`
   (Fähigkeiten, Modifikatoren), `spielablauf/` (nur Akzeptanztests: Szenarien über mehrere
   Phasen).
2. Spiegel: `tests/einheit/` ↔ `arbiter/`, `tests/akzeptanz/` ↔ `anforderungen/`
   (Testdateien zu Modulen: [Anliegen 28](28-benennungOffenePunkte.md)).
3. Daten: Katalog-YAML in `domaene/daten/` → Importer → Datenbank; der Spielstand liegt nur
   in der Datenbank; die Domäne kennt Speicherung nur als Schnittstelle.
4. Design-System: gehört der Technik, die Domäne kritisiert es. Eine lebende
   Komponentenseite (HTML mit dem echten CSS) ist Doku, Vorlage für Mockups und Ziel eines
   Bildschirmtests. Mockups nutzen nur vorhandene Komponenten, Neues geht als Anliegen an die
   Technik; tot ist eine Komponente, die in keinem Template vorkommt; messbare
   Gestaltungsregeln (Kontrast, Mindestgrößen) werden Prüfungen. Auslöser: erstes Item mit
   Oberfläche.
5. Refactoring-Items: nur aus einem Befund, mit prüfbarer Erledigt-Bedingung und „Verhalten
   unverändert“ (Akzeptanztests grün). Ort und Schreiber sind offen.
6. Aus der Werkzeugprobe: Linter-Befunde zeigen Lücken im Domänenmodell (magische `5` für
   Schlachtrunden, Schalter `use_melee` für den fehlenden Begriff *Angriffsart*).

**Kosten.** Ohne Überführung gehen sie mit `VORGEHEN.md` verloren oder werden neu erfunden.
1 bis 3 sind rund 1.000 Zeichen in `architektur.md` (Höchstmaß 6.000).

**Gegenvorschlag.** 1 bis 3 jetzt in `technik/architektur.md`, je mit dem Test oder Vertrag,
der sie prüft; 4 und 5, sobald ihr Auslöser eintritt (bis dahin hält sie dieses Anliegen);
6 als Prüffrage deiner Kritik an Anforderungen. Für 5 schlägst du Ort und Schreiber vor.

**Stellungnahme.** Angenommen. In [`technik/architektur.md`](../../technik/architektur.md):
1 als Grundschnitt der Domäne, 2 unter Tests, 3 als A1 bis A3, je mit Prüfung oder Auslöser.
4 steht dort schon unter Oberfläche, mit Auslöser; so muss dieses Anliegen nichts halten.
5, Vorschlag: kein eigenes Item. Ein Refactoring ist ein Anliegen an den Implementierer;
der Gegenvorschlag nennt die Erledigt-Bedingung, dazu gilt „Akzeptanztests grün“. Schreiber
ist, wer den Befund hat (Reviewer, Architekt); `erledigt` setzt er nach dem Nachprüfen. Den
Satz dazu in `prozess/ablauf.md` schreibst du. 6 gehört als Prüffrage in `architekt.md`
(Kritik in der Domänenphase): „Welche Zahl oder welcher Schalter steht für einen fehlenden
Begriff?“; das schreibst du.
