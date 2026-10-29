# Wie das Frontend gebaut ist und ob die Ordner den Schnitt zeigen

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 2/3
Status: angenommen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Deine Frage: Baut Python die Oberfläche, liegen Dateien des Frontends im Backend,
passt die Ordnerstruktur? Python baut keine Oberfläche. Das Frontend ist
[`technik/frontend/`](../../technik/frontend/): eine HTML-Seite mit Vorlagen, ein Stylesheet,
JavaScript-Module ohne Framework und Build-Schritt. Das Backend ist
[`technik/arbiter/`](../../technik/arbiter/): Es liefert diese Dateien aus und beantwortet
`/api/` mit dem Spielstand als JSON; HTML erzeugt es nicht
([W1](../../technik/architektur/web.md)), anders als ArbiterMap. *Auswahl*, *Ebene* und
Anklicken in der Domäne sind Anforderungen (AUF-5, AUF-20, AUF-25), keine Oberfläche. Drei
Befunde:
1. Der Name zeigt den Schnitt nicht: `arbiter/` ist das Backend, `web/` darin der Anschluss
   für HTTP, nicht die Oberfläche.
2. [`web/anwendung.py`](../../technik/arbiter/web/anwendung.py) enthält Ablauf der geplanten
   Schicht `anwendung/`; der Umzug ist beschlossen
   ([Anwendung, Umbau](../../technik/architektur/anwendung.md)).
3. Eine Regel steht nur in `web/`: *Ebene* wird nur ein *gesetztes* *Modell*; die Domäne
   (`Aufstellung.ebeneWählen`) nimmt jedes *Modell* der *ausgewählten* *Einheit*.

**Kosten.** Am Bildschirm ändert keine Option etwas. Umbenennen berührt 32 Dateien mit 75
Pfaden; Token: ein mittlerer Auftrag.

**Gegenvorschlag.** Den Schnitt im Ordnernamen zeigen, mit dem Umbau zu `anwendung/`
(Anliegen 692).

**Stellungnahme.**

**F1 · Sollen die Ordner Frontend und Backend heißen?**
A: `technik/arbiter/` wird `technik/backend/arbiter/` (ArbiterMap).
B: Bleibt; die [Architektur](../../technik/architektur.md) nennt `arbiter/` das Backend
(Architektur W1).
C: Das Frontend ins Paket, `arbiter/web/static/` (neu).
Empfehlung: A, nach Anliegen 4140.
Antwort: .

**F2 · Wann kommt die Regel aus Befund 3 in die Domäne?**
A: Mit dem Umbau zu `anwendung/` (Anwendung, Umbau). B: Als Item in der nächsten
Technikphase (neu, Grund: Ziel, Regelkonformität).
Empfehlung: A, heute fängt `web/` den Fall ab.
Antwort: .
Kommentar: Ich möchte nicht, dass du irgendetwas umbenennst. Es ist okay, wenn der "backend"-Ordner auch "arbiter" heißt. Ich habe nur die Sorge, dass Frontend-Komponenten dort gebaut werden und nicht im Frontend-Ordner. Wir haben ja jetzt eine Anforderung, für die sich der Bau einer Frontendkomponente lohnen könnte. (Kreise für Bewegung, Aura, Fähigkeiten,...) Würde diese wirklich im Frontend platziert sein? Sei hier gerne kritisch. Ich möchte nur, dass wir einen ordentlichen Aufbau haben und im Frontend Ordner sehe ich eben noch nicht viel, das wie ein Frontend aussieht.

## Runde 2
**Befund.** Zu deinem Kommentar: Nichts wird umbenannt, F1 gilt als B. Ja, der *Grenzkreis*
läge im Frontend, nur die Regel dahinter nicht. Am Beispiel BEW-11:
- Domäne: welche *Modelle* einen *Grenzkreis* bekommen und wie weit er reicht; Regel wie
  `messen.py`.
- `web/darstellung.py`: reicht je Kreis *Stelle*, *Base* und *Abstand* in *Zoll* weiter,
  keine Zeichnung.
- Frontend: zeichnet daraus den Kreis eines *Modells* oder die Einhüllende einer *Einheit*;
  Farbe, Linienart und -dicke stehen in `komponenten.css`.

Deine Verallgemeinerung trägt: Die Regeln messen von der nächsten Stelle der *Base*
(`core_rules.txt:464`); *Nahkampfreichweite*, Aura, *Bewegungsweite*, „innerhalb x″ der
*Aufstellungszone*“ sind alle Punkte höchstens x″ von Formen. Im Wegwerf-Versuch zeichnet der
Browser die Einhüllende per SVG-Maske, ohne Geometrie; ArbiterMap hätte die Kontur gerechnet
(`ArbiterMap/steering/backlog/items/013-spike-reichweiten-darstellung.md:98`), also Zeichnen
im Backend, deine Sorge.

Kritisch:
1. Im Ordner sieht man keine Komponente: Vorlage in `index.html`, Stil in `komponenten.css`,
   Füllen für alle in [`zeichnen.js`](../../technik/frontend/zeichnen.js).
2. Nichts verhindert, dass `web/` Zeichnung rechnet; W1 sperrt nur HTML.
3. Die Einhüllende einer *Einheit* zeigt mehr, als ein *Modell* darf; Arbiter hält es an
   seiner *Bewegungsweite* an (BEW-3.1). Das Bild zeigt, die Domäne entscheidet.

Akzeptanztest: bei der Anforderung ([T1](../../technik/architektur/tests.md)); er prüft am
Bildschirm, also das Frontend. Welche Kreise, prüft ein Einheitstest der Domäne.

**Kosten.** Am Bildschirm gleich. A: ein Ordner, ein Modul, eine Zeile in O5. B: nichts, aber
`zeichnen.js` wächst mit jeder Art gegen 8.000 Zeichen.

**Gegenvorschlag.** In der Technikphase 9 schreibe ich in die
[Architektur](../../technik/architektur.md): `arbiter/` ist das Backend (F1 B); in W2
„`web/` liefert Formen und *Abstände* in *Zoll*, keine Zeichnung“; O5 nach F3.

**F2 · Wann kommt die Regel aus Befund 3 (Runde 1) in die Domäne?**
A: Mit dem Umbau zu `anwendung/` (Anwendung, Umbau). B: Als Item in der Technikphase 9
(neu, Grund: Ziel, Regelkonformität).
Empfehlung: A, heute fängt `web/` den Fall ab.
Annahme: A.
Antwort: .

**F3 · Wie wird der Grenzkreis als Komponente gebaut?**
A: Je Komponente ein Modul in `technik/frontend/komponenten/`, zuerst der Bereich um Formen;
`zeichnen.js` ruft es (Anliegen 6410).
B: Eine Funktion in `zeichnen.js` wie heute (Frontend O5).
C: Ein eigenes HTML-Element des Browsers, Custom Element (neu): Sein Stil läge abseits von
`komponenten.css`, O1 fiele („kein Modul erzeugt Elemente“).
Empfehlung: A. Man sieht sie im Ordner, sie kennt keine Regel, nur Formen, *Abstand* und Art.
Annahme: A.
Antwort: .

**Stellungnahme.**
Kommentar: Ich folge deinen Empfehlungen. Bisher klingt das gut. Wenn mehrere Funktionen in "index" sind, wäre es so langsam an der Zeit, diese aufzuteilen. Wir werden noch mehr Buttons, Karten, Bereiche usw. haben. Wenn HTML nicht passt, wähle das passende. Am liebsten wäre mir eben, dass Mockups direkt eingebaut werden könnten. Aber vielleicht geht das nicht... Auch für das Frontend sollte es eine ordentliche Archtikturregelung haben.
Stellungnahme: Es gelten F1 B, F2 A, F3 A. Aufteilen: Du hast recht, `zeichnen.js` füllt heute alles. In der Technikphase 9 bitte ich den Implementierer, es aufzuteilen: je Komponente (Kopfzeile, *Armeeliste*, Sperrmeldung, Knöpfe, *Karte*) ein Modul in `frontend/komponenten/`, Verhalten unverändert; neu kommt die *Grenze* dazu (Anliegen 7004). HTML passt: Die Vorlagen in `index.html` sind kurz, eine Zeile je Komponente, und genau das Markup, das ein Mockup liefert. Mockups einbauen gilt schon: Der Implementierer übernimmt Markup und CSS eines Mockups ohne Umschreiben und ersetzt nur Beispielinhalte ([Frontend, O3](../../technik/architektur/frontend.md)). Eine Mockup-Datei selbst einbinden geht nicht, sie zeigt einen festen Augenblick mit Beispielen. Eine Architektur des Frontends gibt es dort mit O1 bis O5; in der Technikphase 9 kommt der Ordner `komponenten/` dazu, je Komponente Vorlage, Klasse und Modul. Danach setze ich `erledigt`.
