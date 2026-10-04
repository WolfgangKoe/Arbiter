# Rolle UX für die erste Oberfläche

151 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 2/3 · erledigt

## Runde 1
**Befund.** Plan 3 bringt voraussichtlich das erste Item mit Oberfläche
(Anliegen 145, F2). Das ist der Auslöser der Rolle UX
([Ablauf, Rollen mit Auslöser](../../prozess/ablauf.md#rollen-mit-auslöser)), und DoR 5
verlangt bei einer Oberfläche ein Mockup, bevor das Item bereit ist. Heute schreibt niemand
Mockups.

**Kosten.** Ohne die Rolle ist Plan 3 nicht bereit, oder das Item geht ohne Mockup in die
Technikphase: Dann entscheidet der Implementierer über Aufbau und Aussehen, und du siehst es
erst gebaut.

**Gegenvorschlag.** Rolle `ux`, Perspektive Domäne, ausführend, Modell sonnet:
- Je Anforderung mit Oberfläche ein Mockup: statisches HTML mit dem echten CSS, ohne
  JS-Logik, nur Inhalte aus Kriterien oder Katalogdaten; gelöscht nach dem Einbau.
- Nur Komponenten der Komponentenseite ([Architektur, Oberfläche](../../technik/architektur.md));
  eine neue Komponente ist ein Anliegen an die Technik. Für die erste Oberfläche gibt es
  noch keine; wie das erste Mockup zu seinem CSS kommt, regelt
  [DoR 5](../../prozess/ablauf.md#dor-item-bereit).
- ArbiterMap ist Vorbild für das Bild, nicht Vorlage für Code (145, F1).
- Schreibpfade: `domaene/mockups/` und `handoff/anliegen/`.
- Im Ablauf: Domänenphase zwischen Anforderungen (4) und Plan (5); du siehst das Mockup vor
  der Freigabe des Plans. Kritik: Fachkritiker (Mockup gegen Kriterien), Architekt
  (nur vorhandene Komponenten).
Nach deiner Antwort schreibe ich die Definition und den Ablauf, der Koordinator bekommt die
Rolle in seine Liste.

**F1 · Rolle UX einsetzen?**
- A: Ja, wie oben, sobald 145 F2 mit A beantwortet ist.
- B: Nein, das Mockup schreibt der Anforderungsautor.
Empfehlung: A. Gestaltung ist eine eigene Sicht; der Anforderungsautor schreibt Kriterien,
kein HTML.

Antwort: Ja, gehe ich mit. Ergänzung, weil ich es hier nicht sehe, bitte die konkreten Leitplanken für die UX-Rolle vorlegen. Schau dir die Mockups in ArbiterMap als Negativbeispiel an. Ich finde es grundsätzlich gut, wenn ich mehrere Optionen sehen kann, es wäre mir aber wichtig, dass das erstellte Mockup idealerweise direkt in das Software-INkrement eingebaut werden könnte. Außerdem standen in den Mockups ganz viele Komentare und unnötige Boxen, die mich Token kosten und eine redundante Wiederholung von Anforderungen oder Anliegen waren. Der Mehrwart war faktisch Zero und der Verlust war mir zu hoch. Wir haben Anforderungen, die auf die UX-Funktionalität irgendwie verlinken sollten und die Anliegen entsprechend auf das Mockup. In diesen Textdateien sollte schon alles wesentliche stehen. Also muss es in dem Mockup nicht nochmal stehen. Ggf. sollte das der Implementiere in der Technik bauen oder es braucht da auch noch eine weitere Rolle. Bitte meinen Vorschlag kritsch prüfen. 

## Runde 2
**Befund.** Deine Antwort zu F1 ist eingearbeitet: Rolle [ux](../../.claude/agents/ux.md),
die Leitplanken stehen dort unter „Grenzen“; im
[Ablauf](../../prozess/ablauf.md#domänenphase) Schritt 4 und 6; in der Liste des
Koordinators. Höchstmaß 8.000 Zeichen je Datei ([Kennzahlen](../../prozess/kennzahlen.md)),
die Prüfung baut der Regelumsetzer ([200](200-pruefungDerMockups.md)). UX kann jetzt die
Mockups zu QUE-2 und AUF-4 schreiben, du siehst sie mit Plan 3.

**Stellungnahme zu deinem Vorschlag.**
- Einbaufähig: Das Frontend ist HTML, CSS und JS ohne Vorlagen und ohne Build
  ([153](153-frontendBackendUndDatenbank.md)). Ein statisches Mockup mit den Klassen der
  Komponenten und dem echten CSS ist darum schon die spätere Seite; der Implementierer
  ersetzt nur Beispielinhalte durch Daten.
- Implementierer statt UX: Er arbeitet erst in der Technikphase gegen rote Tests. Du sähest
  das Aussehen erst gebaut, und er entschiede Gestaltung nebenbei, während er Tests grün
  macht. Plan 3 bliebe ohne DoR 5.
- Weitere Rolle: noch kein beobachteter Bedarf. Auslöser
  ([Rollen mit Auslöser](../../prozess/ablauf.md#rollen-mit-auslöser)): Ein Mockup wird beim
  Einbau wiederholt umgeschrieben.
- Optionen: nur, wo der Plan eine sichtbare Entscheidung offenlässt, höchstens drei, je eine
  Datei; die Frage steht im Anliegen, nicht im Mockup.
- Verlinken: Item und Anliegen verlinken das Mockup, nicht die Anforderung. Die Anforderung
  bleibt nach dem Einbau, das Mockup nicht (DoD); ihr Link wäre dann tot.

**F2 · Wer baut das Mockup ein?**
- A: UX schreibt einbaufähig nach `domaene/mockups/`, der Implementierer übernimmt Markup und
  CSS ohne Umschreiben.
- B: UX schreibt direkt ins Frontend unter `technik/`: kein Übernehmen, aber Code vor der
  Freigabe und vor den Tests, verworfene Optionen liegen im Produkt.
- C: Keine UX, der Implementierer baut die Oberfläche in der Technikphase; DoR 5 entfällt.
Empfehlung: A.

Antwort: .
