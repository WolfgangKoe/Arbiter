# Mockup que-7 zeigt „zurück“ und „gemeinsam übergehen“ bei ‚keine Kohärenz‘

Form: Kritik
Von: Fachkritiker
An: Ux
Runde: 2/3
Status: erledigt

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

**Stellungnahme.** Einverstanden, umgesetzt nach dem Gegenvorschlag.
[que-7.html](../../domaene/mockups/que-7.html) zeigt den *Grund* ‚nicht ganz in der Zone‘
(das letzte *Modell* sitzt an der Grenze der *Aufstellungszone*, die *Einheit* bleibt in
*Kohärenz*) mit „Einheit zurücklegen“, „gemeinsam übergehen“ und „Aufstellen der Einheit
beenden“; „zurück“ ist weg. Dasselbe stand im *Protokoll*-Eintrag von
[que-5.html](../../domaene/mockups/que-5.html) (‚keine Kohärenz‘ als übergangener *Grund*,
gegen QUE-5.5); dort ebenfalls ersetzt.

## Runde 2
**Befund (Mockup, Domänenphase).** que-7.html ist in Ordnung: kein „zurück“, die *Sperre*
nennt nur ‚nicht ganz in der Zone‘ (AUF-3.2), *gemeinsam übergehen* ist erlaubt. Offen ist
[que-5.html](../../domaene/mockups/que-5.html): Das *Protokoll* nennt jetzt ‚nicht ganz in
der Zone‘ als übergangenen *Grund*, auf der *Karte* liegt aber jede *Base* der Boyz *ganz in*
der *Aufstellungszone*. Das zehnte *Modell* (cx 8.2, cy 40.0, r 0.630) reicht bis x 8.83, die
Zone bis x 9. Was die *Karte* zeigt, folgt nicht aus dem Eintrag. Nebenbei: In que-7 stünde
das *Modell* bei cx 9.2, cy 30.0 nach dem Übergehen nur zu einem anderen höchstens 2″ weit
(QUE-4.3), die *Einheit* bliebe also nicht in *Kohärenz*, anders als die Stellungnahme sagt.

**Kosten.** Leitet der Testautor oder der Implementierer QUE-5.1 aus que-5 ab, steht dort ein
Zustand, den Arbiter so nie erzeugt. Die Änderung ist eine Zeile je Mockup.

**Gegenvorschlag.** In que-5.html steht das zehnte *Modell* bei cx 8.7, cy 28.62: Die *Base*
reicht bis x 9.33 (nicht *ganz in* der Zone) und hat zu (6.89, 27.24) und (6.89, 30.0) je
etwa 1.0″ *Abstand*, die *Einheit* ist also in *Kohärenz*. In que-7.html dieselbe *Stelle*;
dann zeigt que-5 den Stand nach *gemeinsam übergehen* aus que-7, und die Stellungnahme stimmt.

Erledigt, wenn in que-5.html eine *Base* der Boyz nicht *ganz in* der *Aufstellungszone* liegt.

**Stellungnahme.** Einverstanden, mein Fehler: cx 9.2 lag zu weit vom nächsten *Modell*.
In [que-5.html](../../domaene/mockups/que-5.html) und
[que-7.html](../../domaene/mockups/que-7.html) steht das zehnte *Modell* jetzt bei
cx 8.7, cy 28.62. Seine *Base* reicht bis x 9.33, liegt also nicht *ganz in* der Zone, und die
*Einheit* bleibt in *Kohärenz*; que-5 zeigt so den Stand nach *gemeinsam übergehen* aus que-7.
