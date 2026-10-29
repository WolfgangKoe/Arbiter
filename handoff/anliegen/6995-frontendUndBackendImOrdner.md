# Wie das Frontend gebaut ist und ob die Ordner den Schnitt zeigen

Form: Fragen
Von: Architekt
An: Stakeholder
Runde: 2/3
Status: offen

## Runde 1
**Befund.** Deine Frage: Baut Python die Oberfläche, liegen Dateien des Frontends im Backend,
passt die Ordnerstruktur? Python baut keine Oberfläche. Das Frontend ist
[`technik/frontend/`](../../technik/frontend/): eine HTML-Seite mit Vorlagen, ein Stylesheet,
vier JavaScript-Module (Einstieg, Bedienung, Anfragen, Zeichnen), ohne Framework und
Build-Schritt. Das Backend ist [`technik/arbiter/`](../../technik/arbiter/), das Python-Paket:
Es liefert diese Dateien unverändert aus und beantwortet Anfragen unter `/api/` mit dem
Spielstand als JSON; HTML erzeugt es nicht ([W1](../../technik/architektur/web.md)). Anders
ArbiterMap: Dort setzt Python die Seite aus Vorlagen zusammen.

Datei für Datei: Im Frontend steht nichts vom Backend, im Backend keine Datei nur fürs
Frontend. `web/` ist die Backend-Seite der Schnittstelle: Server, Pfade, Spielstand als JSON,
Nummern für *Spieler* und *Einheiten*. *Auswahl*, *Ebene* und Anklicken in der Domäne klingen
nach Oberfläche, sind aber Anforderungen (AUF-5, AUF-20, AUF-25) und bestimmen, was Ziehen
bewegt; sie gehören dorthin. Drei Befunde:
1. Der Name zeigt den Schnitt nicht: `arbiter/` ist das Backend, du hast es fürs Frontend
   gehalten. Darin klingt `web/` nach Oberfläche und ist der Anschluss für HTTP.
2. [`web/anwendung.py`](../../technik/arbiter/web/anwendung.py) enthält Ablauf, der in die
   geplante Schicht `anwendung/` gehört: wann die *Schlacht* beginnt, ob „Phase beenden“ die
   laufende *Phase* meint. Der Umzug ist beschlossen
   ([Anwendung, Umbau](../../technik/architektur/anwendung.md)), die Datei heißt dann
   `routen.py`.
3. Eine Regel steht nur dort: *Ebene* wird nur ein *gesetztes* *Modell*. Die Domäne
   (`Aufstellung.ebeneWählen`) nimmt jedes *Modell* der *ausgewählten* *Einheit*; die Seite
   bekommt heute trotzdem die richtige Antwort.

**Kosten.** Am Bildschirm ändert keine Option etwas. Umbenennen berührt 32 Dateien mit 75
Pfaden, 15 davon in Prüfungen und Agentendefinitionen, dazu drei Zeilen in `pyproject.toml`;
der Regelumsetzer baut gerade den Reiter Architektur (Anliegen 4140), der die Ordner liest.
Token: ein mittlerer Auftrag, je ein Zug von Regelumsetzer und Architekt.

**Gegenvorschlag.** Den Schnitt im Ordnernamen zeigen, zusammen mit dem Umbau zu
`anwendung/` (Anliegen 692) in einer Technikphase.

**Stellungnahme.**

**F1 · Sollen die Ordner Frontend und Backend heißen?**
A: `technik/arbiter/` wird `technik/backend/arbiter/`, neben `technik/frontend/`, wie
`backend/` und `frontend/` in ArbiterMap (ArbiterMap). Befehl und Paketname `arbiter`
bleiben. Nachteil: Kosten oben. Rückweg: zurückschieben. Nicht an einer Kopie erprobt.
B: Bleibt; die [Architektur](../../technik/architektur.md) nennt `arbiter/` ausdrücklich das
Backend (Architektur W1). Eine Zeile, der Name bleibt missverständlich.
C: Das Frontend ins Paket (`arbiter/web/static/`), wie Flask es anbietet (neu). Verwischt die
Trennung von Frontend und Backend aus dem Technik-Rahmen.
Empfehlung: A, nach Anliegen 4140. Hast du den Ordner missverstanden, tut es jeder neue Leser.
Antwort: .

**F2 · Wann kommt die Regel aus Befund 3 in die Domäne?**
A: Mit dem Umbau zu `anwendung/` (Anwendung, Umbau): Erst dann ruft ein zweiter Weg die
Domäne, das Wiederholen gespeicherter Handlungen (Speicher, P2). Ein Einheitstest, wenige
Zeilen.
B: Jetzt als eigenes Item in der nächsten Technikphase (neu, Grund: Ziel,
Regelkonformität). Gleich viel Arbeit, früher sicher.
Empfehlung: A, heute fängt `web/` den Fall ab.
Antwort: .
Kommentar: Ich möchte nicht, dass du irgendetwas umbenennst. Es ist okay, wenn der "backend"-Ordner auch "arbiter" heißt. Ich habe nur die Sorge, dass Frontend-Komponenten dort gebaut werden und nicht im Frontend-Ordner. Wir haben ja jetzt eine Anforderung, für die sich der Bau einer Frontendkomponente lohnen könnte. (Kreise für Bewegung, Aura, Fähigkeiten,...) Würde diese wirklich im Frontend platziert sein? Sei hier gerne kritisch. Ich möchte nur, dass wir einen ordentlichen Aufbau haben und im Frontend Ordner sehe ich eben noch nicht viel, das wie ein Frontend aussieht.

## Runde 2
**Befund.** Zu deinem Kommentar: Nichts wird umbenannt, F1 gilt als B. Ja, der *Grenzkreis*
läge im Frontend, nur die Regel dahinter nicht. Am Beispiel BEW-11 in drei Teilen:
- Domäne: welche *Modelle* einen *Grenzkreis* bekommen und wie weit er reicht
  (*Bewegungsphase*, *ausgewählt*, *am Zug*, *Bewegungsweite*). Das ist Regel, wie `messen.py`.
- `web/darstellung.py`: reicht je Kreis *Stelle*, *Base* und *Abstand* als Zahlen in *Zoll*
  weiter, keine Zeichnung.
- Frontend: zeichnet daraus den Kreis eines *Modells* oder die Einhüllende einer *Einheit*;
  Farbe, Linienart und -dicke je Art stehen in `komponenten.css`.

Deine Verallgemeinerung trägt, weil die Regeln von der nächsten Stelle der *Base* messen
(`core_rules.txt:464`): *Nahkampfreichweite*, Aura, *Bewegungsweite*, „innerhalb x″ der
*Aufstellungszone*“ sind jedes Mal alle Punkte höchstens x″ von Formen. Eine Komponente
„Bereich um Formen“ deckt alle ab, auch ovale *Bases*. Wegwerf-Versuch (Bild:
`/tmp/bereichProbe/probe.png`): Der Browser zeichnet die Einhüllende dreier Kreise und eine
Zone plus 3″ selbst, per SVG-Maske, ohne eine Zeile Geometrie. ArbiterMap hätte die Kontur
gerechnet (`acos`, `ArbiterMap/steering/backlog/items/013-spike-reichweiten-darstellung.md:98`);
das wäre Zeichnen im Backend, deine Sorge.

Kritisch, drei Punkte:
1. Du hast recht, im Ordner sieht man keine Komponente. Eine liegt heute in drei Dateien:
   Vorlage in `index.html`, Stil in `komponenten.css`, Füllen in `zeichnen.js`, und
   [`zeichnen.js`](../../technik/frontend/zeichnen.js) füllt alle: Kopfzeile, *Armeeliste*,
   Sperrmeldung, Knöpfe, *Karte*. Der *Grenzkreis* käme dazu.
2. Nichts verhindert, dass `web/` Zeichnung rechnet; W1 sperrt nur HTML.
3. Bei der Bewegung zeigt die Einhüllende einer *Einheit* mehr, als ein *Modell* darf: Ein
   Boy links erreicht den rechten Rand nicht. Harmlos, Arbiter hält ihn an seiner
   *Bewegungsweite* an (BEW-3.1): Das Bild zeigt, die Domäne entscheidet.

Akzeptanztest: Er bleibt bei der Anforderung ([T1](../../technik/architektur/tests.md)) und
prüft am Bildschirm, also schon das Frontend; welche Kreise, prüft dazu ein Einheitstest der
Domäne.

**Kosten.** Am Bildschirm gleich bei A und B. A: ein Ordner, ein Modul, eine Zeile in O5;
bestehende Teile ziehen erst um, wenn ein Item sie ändert. B: nichts, aber `zeichnen.js`
wächst mit jeder Art gegen 8.000 Zeichen. Bildschirmtests prüfen Formen und *Abstand* im
Markup wie heute die *Modelle* (QUE-2.7); die Linie selbst siehst du im Review.

**Gegenvorschlag.** In der Technikphase 9 schreibe ich in die
[Architektur](../../technik/architektur.md): `arbiter/` ist das Backend (F1 B); in W2
„`web/` liefert Formen und *Abstände* in *Zoll*, keine Zeichnung“ (Urteil des Reviewers);
O5 nach F3.

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
C: Ein eigenes HTML-Element des Browsers (Custom Element) (neu). Komponente ohne Framework,
aber ihr Stil läge abseits von `komponenten.css`, und O1 fiele („kein Modul erzeugt
Elemente“).
Empfehlung: A. Man sieht sie im Ordner, sie kennt keine Regel, nur Formen, *Abstand* und Art.
Annahme: A.
Antwort: .

**Stellungnahme.**
