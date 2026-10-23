# Mockup que-7 zeigt „zurück“ und „gemeinsam übergehen“ bei ‚keine Kohärenz‘

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund (wartet auf die Domänenphase).** Ich habe das Item
[aufraeumenUndFesteAdresse](../../domaene/items/aufraeumenUndFesteAdresse.md) abgenommen.
Dabei ist mir aufgefallen: In [que-7.html](../../domaene/mockups/que-7.html), Zeilen 45 bis 51,
stehen unter dem *Grund* ‚keine Kohärenz‘ die Knöpfe „zurück“, „gemeinsam übergehen“ und
„Aufstellen der Einheit beenden“.
1. „zurück“ gibt es nicht mehr. AUF-17 ist samt Test entfallen (Anliegen 2410), das Gebaute
   zeigt den Knopf nicht mehr ([anfragen.js](../../technik/frontend/anfragen.js)). Neben
   „Aufstellen der Einheit beenden“ steht jetzt „Einheit zurücklegen“
   ([AUF-23](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md),
   [auf-23-vorher.html](../../domaene/mockups/auf-23-vorher.html)).
2. Bei ‚keine Kohärenz‘ bietet Arbiter *gemeinsam übergehen* nicht an
   ([QUE-5.5](../../domaene/anforderungen/querschnitt/uebergehen.md), Anliegen 2361 F1 A).

Das Mockup gehört zum Item [ruhigeKarte](../../domaene/items/ruhigeKarte.md) (Etappe 2).
Kein Schritt des Happy Path von Plan 7 ist betroffen, darum wartet der Befund nach
[Ich 3](../../prozess/praemissen/ich.md). Die Namen der *Griffe* behandelt schon Anliegen 2920.

**Kosten.** Ohne Änderung baut der Implementierer nach O3 aus diesem Markup einen Knopf,
den es nicht mehr gibt, und ein *Übergehen*, das QUE-5.5 verbietet. Die Änderung selbst sind
drei Zeilen in einer Datei.

**Gegenvorschlag.** In que-7.html steht ein *Grund*, der übergangen werden kann, etwa
‚nicht ganz in der Zone‘. Die Knöpfe sind dann „Einheit zurücklegen“, „gemeinsam übergehen“
und „Aufstellen der Einheit beenden“, so wie in auf-23-vorher.html und QUE-7.1. Wenn
‚keine Kohärenz‘ bleiben soll, entfällt „gemeinsam übergehen“. Dann zeigt das Mockup aber
nicht mehr, dass die *Karte* stehen bleibt, wenn dieser Knopf erscheint (QUE-7.1).

Erledigt, wenn que-7.html weder „zurück“ zeigt noch *gemeinsam übergehen* bei
‚keine Kohärenz‘ anbietet.

**Stellungnahme.**
