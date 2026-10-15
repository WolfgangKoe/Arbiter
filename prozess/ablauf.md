# Ablauf

Etappe, Zyklus, Phase und nächsten Schritt nennt der Stand. Mechanismus:
`standregeln/phasenfolge.py` ([Regeln](regeln.md#standregeln)).

## Domänenphase
1. Planer: Etappen aus dem Ziel; nur die aktuelle ausformuliert. Auslöser: keine Etappe.
2. Architekt: Kritik an der aktuellen Etappe und der Reihenfolge, als Anliegen.
3. Freigabe: „.“ → Koordinator committet `Freigabe Etappe <n>`.
4. Anforderungsautor, in jedem Zyklus: Anforderungen zum nächsten Schnitt, in Zyklus 1 zur
   Etappe, danach zum Zyklusziel des freigegebenen Reviews samt Kommentaren (ohne dieses zum
   Abschnitt „Danach“ des vorigen Plans); Begriffe ins Glossar. Eine genügt. Auslöser:
   kein Kriterium ohne Akzeptanztest. Bei einer Oberfläche danach
   [UX](../.claude/agents/ux.md): ein Mockup je Anforderung (DoR 5); das Item verlinkt es.
   Mechanismus: nur Text.
5. Planer: `handoff/plan.md` (`# Plan · Zyklus <n>`) mit den Items, die bereit sind (DoR):
   eins genügt, höchstens drei; weicht er vom Zyklusziel des Reviews ab, begründet er es.
   Am Ende der Abschnitt `## Freigabe` ([Freigabe und Kommentare](#freigabe-und-kommentare)).
   Weitere Anforderungen kommen in späteren Zyklen. Jedes Item steht als Link
   `[…](../domaene/items/<id>.md)`; daran erkennt die Rückverfolgung die Items des Plans
   (DoD 2). Mechanismus: `lesen/plan.py` (`offeneItems`). Jedes Item nennt Kriterien ohne
   Test (`AUF-7.3`) oder ihre Anforderung; bis dahin ist der Plan nicht zur Freigabe bereit.
   Mechanismus: nur Text; der Stand nennt die Kriterien ohne Test.
6. Kritik: Architekt an Anforderungen und Items, auch an Format und Größe. Am
   Mockup: Fachkritiker (gegen die Kriterien), Architekt (nur vorhandene Komponenten).
7. Freigabe ([Freigabe und Kommentare](#freigabe-und-kommentare)) → Koordinator committet
   `Freigabe Plan <n>`. Danach Technikphase.

Kritik blockiert nicht: Offene Anliegen stehen in der Freigabevorlage, sortiert vom
Moderator (`handoff/moderation.md`). Mechanismus: nur Text. Wer gleichzeitig läuft:
[Gleichzeitige Läufe](#gleichzeitige-läufe).

### DoR (Item bereit)
1. Format und Höchstmaß von Anforderung und Item (`domaene/CLAUDE.md`), die Kriterien-IDs
   existieren.
2. Keine vagen Wörter; kursive Fachbegriffe stehen im Glossar (Wortanfang).
3. Regelbasierte Kriterien nennen ihre Fundstelle.
4. Abhängigkeiten erledigt, kein offenes Anliegen zum Item.
5. Bei einer Oberfläche: Mockup aus vorhandenen Komponenten. Gibt es noch keine
   Komponentenseite, bringt das Mockup sein CSS als Vorschlag mit; die Technikphase baut
   daraus die Komponentenseite. Eine neue Komponente gilt als vorhanden, wenn der Architekt
   sie in einem Anliegen entschieden und UX ihre Regeln wörtlich in
   `domaene/mockups/vorschlag.css` übernommen hat; der Implementierer trägt sie in der
   Technikphase in die Komponentenseite ein (Anliegen 317).
6. Bei einer Bedienung nennt die Anforderung jede Geste (Klick, Ziehen, Auswahl) und was
   danach am Bildschirm geschieht. UX hat sie vor den Mockups mit ArbiterMap und Arbiter-old
   verglichen; jede Abweichung hat der Stakeholder als Frage entschieden (Anliegen 685).

Mechanismus für 1 bis 6: nur Text. Fachliche Vollständigkeit ist Urteil (Schritt 6) und
zeigt sich spätestens an den roten Tests.

## Technikphase
Auslöser: `Freigabe Plan <n>`. Fehlen Rollen, schlägt der
Organisationsentwickler sie vor.
1. Testautor: Akzeptanztests je Kriterium der Items, rot. Hat ein Item beide Hälften
   (Handlung über HTTP, ihre Anzeige), legt vorher der Architekt den Vertrag fest: Pfade
   und je Antwort ein JSON-Beispiel in `technik/architektur/web.md`. Daraus testet der
   Testautor das Backend mit dem Flask-Testclient, das Frontend mit einem Bildschirmtest,
   dem Playwright das Beispiel statt des Servers liefert; derselbe Bildschirmtest gegen den
   echten Server ist der Akzeptanztest des Items (Anliegen 241). Mechanismus: nur Text.
2. Kritik: Fachkritiker (trifft der Test das Kriterium?), Architekt (Schnittstelle).
   Ein bemängelter Test geht nicht in die Umsetzung, bis das Anliegen geklärt ist;
   widerspricht der Testautor, wird es an den Anforderungsautor zum Kriterium gehoben. Der
   Rest läuft weiter. Mechanismus: nur Text.
3. Implementierer: macht die Tests grün. Refactoring nur aus einem Befund, als Anliegen an
   ihn von dem, der den Befund hat; der Gegenvorschlag nennt die Erledigt-Bedingung, dazu gilt
   „Verhalten unverändert“ (Akzeptanztests grün). Nach jedem Lauf prüft der Reviewer (Kritik
   am Code). Bei einer Oberfläche übernimmt er Markup und CSS des Mockups ohne Umschreiben
   und ersetzt nur Beispielinhalte durch Daten (Anliegen 151). Mechanismus: nur Text.
   Hat das Item Vertrag und Tests beider Hälften, laufen Implementierer (Backend) und
   Frontend-Implementierer gleichzeitig ([Gleichzeitige Läufe](#gleichzeitige-läufe)).
   Mechanismus: nur Text ([Backlog](backlog.md)).
4. Reviewer: DoD über das Inkrement, `/code-review`, Wiederverwendung, Vereinfachung,
   Effizienz, Flughöhe. Dazu die Probe, ob die Tests den Code treffen: In einer Kopie in
   `/tmp` baut er Fehler einzeln in den neuen Produktcode ein und nennt im Review, wie viele
   Tests rot wurden; jede Lücke wird ein Anliegen an den Testautor (Anliegen 630).
   Mechanismus: nur Text.
5. Fachkritiker: fachliche Abnahme gegen Kriterien und Etappe. Danach löscht der Planer
   die abgenommenen Items mit `rm` ([Ich 2](praemissen/ich.md)). Mechanismus: nur Text.
6. Reviewer: `handoff/review.md`, erste Zeile `# Review · Zyklus <n>`, darunter der
   Startbefehl der App mit Link auf [Web, W5](../technik/architektur/web.md#aufbau) (auf
   Wunsch des Stakeholders auch hier, Anliegen 353). Danach der Abschnitt
   `## Am Bildschirm prüfen`: ein Satz, was insgesamt per Maus oder Finger machbar ist;
   dann als nummerierter Klickpfad mit dem erwarteten Bild je Schritt nur, was in diesem
   Zyklus neu oder anders machbar ist, Schritt 1 ist der Start. Der Reviewer geht ihn am
   laufenden Arbiter durch; was nur ein Test zeigt, steht dabei (Anliegen 355, 359). Vor
   dem Abschnitt `## Freigabe` der Abschnitt `## Nächstes Vorgehen` mit drei Punkten, je
   mit Beleg:
   - Produktziel: welche Etappen erreicht sind, was dem Ziel am meisten fehlt.
   - Etappenziel: was zur aktuellen Etappe fehlt, nach der Abnahme des Fachkritikers und dem
     Abschnitt „Danach“ des Plans; in wie vielen Zyklen sie erreichbar ist.
   - Zyklusziel: Empfehlung für Plan n+1. Zuerst, was danach am Bildschirm machbar ist und
     was noch nicht, in Worten des Spielers mit den Begriffen des Glossars (Anliegen 358);
     dann die technischen Voraussetzungen und Schulden, die vorher weg müssen.
   Der Reviewer fasst zusammen und empfiehlt; der Stakeholder entscheidet mit Freigabe und
   Kommentaren, der Planer schneidet die Items. Davor der Abschnitt `## Rundgang Prüfcode`:
   Einmal je Zyklus geht der Reviewer mit dem Stakeholder durch den Prüfcode, der seit dem
   letzten Review entstanden ist (`prozess/pruefungen/`, Hooks in `.claude/settings.json`,
   Prüfkonfiguration): die Dateien und die wesentlichen Probleme, je mit Fundstelle. Der
   Stakeholder kommentiert; was er beauftragt, wird in der Nachkorrektur ein Anliegen an den
   Regelumsetzer. Mechanismus: nur Text.
7. Freigabe ([Freigabe und Kommentare](#freigabe-und-kommentare)) → Koordinator committet
   `Freigabe Review <n>`. Danach Prozessphase. Mechanismus: nur Text.

Ausnahmen vom Test vor dem Code: Oberfläche (Mockup zuerst, Bildschirmtest danach),
technisches Neuland (Wegwerf-Versuch, dann Test).

### DoD (Item fertig)
1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`;
   Zeilen und Zweige mindestens 95 % für `technik/arbiter`. Mechanismus:
   `formregeln/abdeckung.py` im Lauf von `python3 -m pytest prozess/pruefungen`.
   Ist in `technik/tests` ein Test rot, gilt die Schwelle nicht: Die Prüfung misst nicht und
   nennt die Zahl der roten Tests (Tests vor dem Code brechen auch geteilte Fixtures).
   Mechanismus: `formregeln/abdeckung.py` (`aussetzung`, `verstoß`).
2. Prüfmechanismen grün. Mechanismus: Benennung und Spiegel (`formregeln/benennung.py`), Kriterium ↔
   Test (`kriterienregeln/rueckverfolgung.py`: Kennung höchstens einmal je Datei; ein Kriterium ohne Test ist
   rot, sobald ein offenes Item eines freigegebenen Plans es nennt, vorher nennt es der
   Stand), Komplexität (`formregeln/werkzeugaufruf.py`, `complexipyAufrufen`), Code →
   Glossar (`formregeln/glossar.py`), Kommentare und Docstrings nach `prozess/praemissen/es.md` 8
   (`formregeln/kommentare.py`), toter Code (vulture über `technik/arbiter` und
   `technik/tests/akzeptanz`, ohne Einheitstests: `unbenutzterCode` in `formregeln/abdeckung.py`), alle
   im Lauf von `python3 -m pytest prozess/pruefungen`, ruff dort über `formregeln/werkzeugaufruf.py` (`ruffAufrufen`);
   SonarLint (Standardprofil ohne Namensregeln, Ordner nach [regeln.md](regeln.md)) mit
   `python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint`, beim Commit als Hook
   `sonarlint` ([Regeln](regeln.md#formregeln), Anliegen 216); Höchstmaße nur Text ([Kennzahlen](kennzahlen.md)). Urteil: Zeilen,
   die nur Einheitstests erreichen, beurteilt der Reviewer (Vorbedingung, fehlendes
   Kriterium oder tot); Glossar → Code.
3. Item gelöscht, die Anforderung beschreibt das gebaute Verhalten. Mechanismus: nur Text.
4. Review geschrieben, Fachkritik hat gegen Ziel, Etappe und Kriterien abgenommen (Urteil).
   Mechanismus: nur Text.

Kommen Mutationstests oder eine Oberfläche hinzu, gelten auch Mutationsschwelle der
geänderten Domänenmodule und Bildschirmtest grün, Mockup gelöscht.

Werkzeuge für die offenen Prüfungen (Regelumsetzer baut, Architekt kritisiert): mypy oder
pyright strikt, import-linter, complexipy (Schwelle 15), ruff (Stil, ARG, PLR2004, PLR0913,
FBT, ERA, `PLR0912` mit 12), Duplikaterkennung, semgrep für eigene Konventionen, cSpell mit deutschem Wörterbuch aus dem
Glossar, eslint und stylelint fürs Frontend. Die Sperre der Agenten ist für Python mindestens so
streng wie SonarLint, die Sicht des Stakeholders; Mechanismus: `formregeln/sonarlint.py` (DoD 2).
SonarLint prüft nur Python, das Frontend prüfen eslint und stylelint (Anliegen 280). Nicht verwendet: radon-Wartbarkeitsindex,
ruff-McCabe, ruff `PLR0911` (meldet frühes `return`).

## Prozessphase
Auslöser: `Freigabe Review <n>`.
1. Organisationsentwickler: `handoff/retro.md` (`# Retro · Zyklus <n>`, darunter der Absatz
   „Dashboard öffnen“ aus dem vorigen Retro unverändert, Anliegen 405) aus Anliegen an den
   Prozess, Kennzahlen (`prozess/kennzahlen.md`) und Auslösezählern (nur Text). Sie beginnt
   mit dem Fortschritt des Produkts: erreichte Etappen, Kriterien mit grünem Test, was am
   Bildschirm neu geht. Höchstens zwei Prozess-Items, je aus einem Befund, der das Produkt
   aufgehalten hat (Anliegen 630). Ein Mechanismus entsteht wie eine Rolle erst bei
   beobachtetem Bedarf; Vorrang hat das Produkt: Anforderung, Akzeptanztest, grüner
   Produktcode (Retro 3). Dazu: Neuerungen von Claude Code, die einen eigenen
   Mechanismus ersetzen; wiederholte Entscheidungen des Stakeholders als Vorschlag für eine
   Prämisse; eine wiederholt verletzte Prämisse ohne Mechanismus als Prozess-Item. Ist eine
   Etappe erreicht, legt er `doku/` an oder pflegt es: für Menschen, keine CLAUDE.md verweist
   darauf; grafisch und kurz, nur Seltenes (Perspektiven, Rollen, Ordner), Rollentabelle und
   Ordnerbaum per Skript. Mechanismus: nur Text.
   Prozess-Items stehen im Abschnitt `## Prozess-Items` als `- P<k> …`; dort nur, was auf
   den nächsten Zyklus wirkt oder der Stakeholder vorher will, die übrigen im
   [Backlog](backlog.md) bis zur nächsten Prozessphase. Mechanismus: nur Text.
2. Kritik: Domäne und Technik an Regeländerungen, als Anliegen.
3. Nachkorrektur: Kommentare in der Retro und Antworten in den Anliegen, auf die sie verweist,
   arbeitet der Organisationsentwickler ein, bis Befunde, Prozess-Items und Empfehlung zu
   ihnen passen; auch nach der Freigabe ([Freigabe und Kommentare](#freigabe-und-kommentare)).
4. Freigabe ([Freigabe und Kommentare](#freigabe-und-kommentare)) → Koordinator committet
   `Freigabe Retro <n>`.
5. Regelumsetzer: Mechanismen zu den freigegebenen Prozess-Items, je mit Scheiter-Test; ein
   Item je Lauf, damit die Belegung unter 120.000 Token bleibt. Den Lauf, der ein Item
   abschließt, committet der Koordinator mit dem Betreff `P<k>: …`, einen Zwischenstand mit
   `P<k> Zwischenstand: …`. Hat jedes Item der Retro seinen Commit `P<k>:` seit
   `Freigabe Retro <n>` (auch als `Retro <n> P<k>: …`), folgt die Domänenphase mit Plan n+1.
   Mechanismus: nur Text.
6. Der Zyklus endet nach Schritt 5; dann pusht der
   [Koordinator](../.claude/agents/koordinator.md) nach `dev`. Mechanismus: nur Text.

Nach jeder Freigabe empfiehlt der Koordinator einen neuen Chat mit Startprompt
([Koordinator](../.claude/agents/koordinator.md)); den Stand bringt der Hook mit.
Mechanismus: nur Text.

## Freigabe und Kommentare
Plan, Review und Retro enden mit diesem Abschnitt; der Autor legt ihn so an (Mechanismus:
nur Text):
```
## Freigabe
Freigabe: offen
Kommentar: .
```
- Der Stakeholder kommentiert überall in der Datei: eine eigene Zeile `Kommentar: <Text>`
  unter der Stelle, die er meint; die letzte Zeile ist für Allgemeines. Zu anderen Dateien
  kommentiert er neben ihrem Link in Plan, Review oder Retro, in Anliegen mit `Antwort:` oder
`Kommentar:` ([Anliegen](#anliegen)). Er gibt frei mit
  `Freigabe: ja`. Diese Zeilen ändert nur er. Mechanismus: nur Text.
- Nachkorrektur: Der Autor (Plan: Planer, Review: Reviewer, Retro: Organisationsentwickler)
  ändert die Datei nach dem Kommentar und schreibt darunter eine Zeile `Stellungnahme: <was,
  wo>`. Betrifft der Kommentar ein fremdes Artefakt oder braucht er eine Entscheidung, wird
  daraus ein Anliegen; die Stellungnahme nennt dessen Nummer. Solange ein Kommentar ohne
  Stellungnahme steht, ist der Autor dran, auch nach der Freigabe. Mechanismus: nur Text.
- „.“ im Chat heißt: Die Datei ist durchgesehen. Steht `Freigabe: ja`, committet der
  Koordinator `Freigabe <Plan|Review|Retro> <n>`, auch wenn Kommentare offen sind; die
  Nachkorrektur folgt danach. Steht `Freigabe: offen`, beauftragt er den Autor und legt die
  Datei danach wieder vor. Mechanismus: nur Text.
- In `handoff/` heißt ein Commit mit seinem Betreff in Anführung (Commit „Freigabe Plan
  4“), nicht mit der Kennung; `git log --grep` findet ihn. Betreffe sind daher für sich
  verständlich (Anliegen 354). Mechanismus: nur Text.
- Kommentare und Stellungnahmen bleiben, bis der Autor die Datei im nächsten Zyklus neu
  schreibt; Höchstmaß: [Kennzahlen](kennzahlen.md).
- Die Etappe gibt der Stakeholder mit „.“ im Chat frei.

## Fortschritt
Wo ein Plan umgesetzt wird, zeigt der Abschnitt `## Fortschritt` vor `## Freigabe`, wie weit
die Phase ist und was sie aufhält (Anliegen 421): im Review für die Domänenphase danach (sie
setzt sein Zyklusziel um; ohne Review, in Zyklus 1, entfällt er), im Plan für die
Technikphase, in der Retro für die Prozessphase. Er wächst mit der Phase und zählt nicht zum
Höchstmaß. Ihn schreibt nur das Skript, der Autor lässt ihn beim Ändern stehen. Keine Rolle
liest ihn für ihre Arbeit: Ihre offenen Schritte nennt ihr der Hook beim Start.

Eine Zeile je Schritt nach der Tabelle, `- [ ] <Rolle>: <Schritt>`, abgehakt `- [x]`.
Darunter eingerückt, was ihn aufhält, `Hindernis: <Text> (Anliegen <nr>)`, angenommen mit
`; beseitigt: Commit „<Betreff>“`, und ein Kommentar des Stakeholders
`Kommentar: <Text> (Anliegen <nr>)`.
- Fakt: Ein Hook hakt nach jedem Rollenlauf ab, was die Tabelle als Fakt nennt.
- Befehl: Die Rolle hakt ihren Schritt am Ende ihres Laufs mit dem Befehl ab, als Kritiker,
  wenn seine Kritik umgesetzt ist. Hält sie etwas auf, meldet sie es mit dem Befehl und nennt
  die Rolle, die es beseitigen kann; das Skript legt das Anliegen an (Kritik, an den
  Stakeholder Fragen) und schreibt die Zeile `Hindernis:`.
- Dashboard: Der Stakeholder hakt jede Zeile ab oder kommentiert sie; der Kommentar wird ein
  Anliegen von ihm an die Rolle der Zeile.

Phase · Schritt | Zeile | abgehakt durch
---|---|---
Domäne 1 bis 3, nur ohne Etappe | Planer: Etappe · Architekt: Kritik an der Etappe · Stakeholder: Freigabe Etappe | Fakt: Etappendatei neu · Befehl · Fakt: Commit
Domäne 4 | Anforderungsautor: Anforderungen zum Zyklusziel · UX: Mockups, bei einer Oberfläche | Befehl
Domäne 5 | Planer: Plan geschrieben | Fakt: `# Plan · Zyklus <n>`
Domäne 6 | je Kritiker: Kritik an Anforderungen, Items und Mockups | Befehl
Domäne 7 | Stakeholder: Freigabe Plan | Fakt: Commit
Technik 1, 2 je Item | Testautor: Tests zu Item <k> · je Kritiker: Kritik daran | Fakt: jedes Kriterium des Items hat einen Test · Befehl
Technik 3 je Item | Implementierer: Tests zu Item <k> grün · Reviewer: Kritik am Code | Befehl
Technik 4 | Reviewer: DoD über das Inkrement | Befehl
Technik 5 je Item | Fachkritiker: Item <k> abgenommen · Planer: Item <k> gelöscht | Befehl · Fakt: Datei weg
Technik 6, 7 | Reviewer: Review geschrieben · Stakeholder: Freigabe Review | Fakt: `# Review · Zyklus <n>` · Fakt: Commit
Prozess 1 | Organisationsentwickler: Retro geschrieben | Fakt: `# Retro · Zyklus <n>`
Prozess 2, 3 | je Kritiker: Kritik an Regeländerungen · Organisationsentwickler: Nachkorrektur | Befehl
Prozess 4 | Stakeholder: Freigabe Retro | Fakt: Commit
Prozess 5 je Prozess-Item | Regelumsetzer: P<k> | Fakt: Commit `P<k>:`
Prozess 6 | Koordinator: nach `dev` gepusht | Fakt: `origin/dev` enthält den letzten Commit

Mechanismus: nur Text; Skript, Hook, Befehl und Dashboard baut der Regelumsetzer (Anliegen
490). Bis dahin fehlt der Abschnitt.

## Rollen mit Auslöser
Der Organisationsentwickler schlägt eine Rolle vor, wenn ihr Auslöser eintritt.
Mechanismus: nur Text.
- Frontend-Implementierer mit `technik/frontend/`, der Implementierer gibt den Pfad ab:
  Der Reviewer findet wiederholt, dass ein Mockup beim Einbau umgeschrieben wurde (Anliegen
  151), oder ein Item des freigegebenen Plans hat Vertrag und Tests beider Hälften
  (Technikphase, Schritt 1; Anliegen 241).
- Prozesskritiker: Prozesskritik fehlt, oder der Organisationsentwickler verteidigt
  wiederholt eigene Regeln.
- Haiku-Zuarbeiter (Regel-Nachschlager, Belegprüfer): bei beobachtetem Bedarf, der
  Belegprüfer nach der ersten falschen Behauptung. Sie startet die Rolle, die das Ergebnis
  braucht.
- Testautor auf Opus: Fachkritik oder Mutationstests zeigen wiederholt fehlende Fälle.

## Kritik am Code
Nach jeder Änderung von Produktcode (`prozess/praemissen/es.md`) prüfen ihn die Kritiker der
getroffenen Pfade, bevor die nächste Rolle darauf aufbaut. Befunde werden Anliegen an den Autor.
Den Code der Prüfskripte und Hooks kritisiert niemand je Commit; dafür gibt es den Rundgang
([Technikphase](#technikphase), Schritt 6). Mechanismus: nur Text.

Code | schreibt | prüft
---|---|---
`technik/tests/akzeptanz/` | Testautor | Fachkritiker (Kriterium), Architekt (Schnittstelle, Lesbarkeit)
`technik/arbiter/`, `technik/tests/einheit/`, `technik/frontend/` | Implementierer | Reviewer
`pyproject.toml`, Linter-Konfiguration | Regelumsetzer | Architekt (schränkt sie die Technik richtig ein?)

Der Kritiker prüft den Commit des Autors; sein Anliegen nennt den Betreff. Ein Kritiklauf
bekommt keinen eigenen Commit, seine Anliegen gehen mit dem nächsten (Anliegen 600).
Mechanismus: nur Text.

## Commits
Der Koordinator committet jeden Lauf mit Produktcode für sich, damit die Kritik je Commit
bleibt. Läufe nur mit Texten, die zusammen enden, Kritikläufe und gelöschte erledigte
Anliegen gehen in einen Commit. Er prüft nicht vorher selbst: Die Prüfungen laufen im
Commit-Hook, ist eine rot, scheitert der Commit und lässt alles stehen; er meldet es der
Rolle, die es beheben kann. Der Hook prüft nur, was der Commit ändern kann; alles prüfen
der Regelumsetzer, bevor er fertig meldet, und der Reviewer bei der DoD (Anliegen 600).
Mechanismus: `.pre-commit-config.yaml` ([Regeln](regeln.md#formregeln)); nur, was der
Commit ändern kann: Anliegen 601; sonst nur Text.

## Gleichzeitige Läufe
Gleichzeitig laufen Rollen, die nur Anliegen schreiben, und Läufe zu verschiedenen Anliegen
oder Items, auch derselben Rolle, wenn (Anliegen 279):
1. ihre Dateien getrennt sind, nach Befund, Gegenvorschlag und `git status`; eine eigene
   Zeile in `prozess/regeln.md` zählt als getrennt,
2. keiner auf den anderen wartet (`wartet auf`, Reihenfolge des Stakeholders),
3. höchstens einer Hook-Code ändert: Module, die `.claude/settings.json` startet, samt ihren
   Importen. Sie laufen aus demselben Arbeitsbaum als Hooks jedes Laufs.

Die Moderation nennt je Rolle die Stränge: was gleichzeitig läuft, was eine Kette bleibt.
Der Koordinator committet nach den Pfaden der Läufe ([Commits](#commits)); die Zeile eines
Nachbarn in `regeln.md` geht mit. Ist eine Prüfung nur in Dateien eines laufenden Nachbarn
rot, nennt der Lauf sie und meldet fertig; committet wird, wenn der Commit-Hook grün ist. Mechanismus: Ein Importfehler im Prüfmodul eines Nachbarn macht nur
dessen Tests rot, `pyproject.toml` ([Regeln](regeln.md#formregeln), Anliegen 304); sonst nur Text.

## Anliegen
Anliegen ist der Oberbegriff: eine Datei je Diskussion, `handoff/anliegen/<nr>-<kurz>.md`,
höchstens 4.000 Zeichen; jede Zeile `Antwort:` zählt als `Antwort: .` (Anliegen 161).
Mechanismus: nur Text.
Erste Zeile `# <Titel>`, dritte Zeile der Kopf:
`<nr> · <Form> · von <Rolle> → <Rolle> · Runde <n>/3 · <Status>`, dahinter
`· wartet auf <nr>`, solange erst ein anderes Anliegen erledigt sein muss, oder
`· wartet auf die Prozessphase`. Rolle: Name aus `.claude/agents/` oder Stakeholder, ohne
Perspektive (Anliegen 420).
Mechanismus: `anliegenregeln/anliegen.py`; es kennt `Auftrag` (im Kopf noch `Anliegen`)
und `· wartet auf` nicht und meldet sie rot (Anliegen 686); eine Perspektive in
Klammern lässt es durch, ohne Perspektive: nur Text.

Form | der Empfänger soll | Absender
---|---|---
Kritik | sein Artefakt berichtigen, es ist falsch oder veraltet | jede Rolle, Stakeholder
Fragen | entscheiden | jede Rolle
Auftrag | Neues umsetzen; er fragt nach, lehnt aber nicht ab | Stakeholder

Je Runde (`## Runde <n>`) die Absätze `**Befund.**`, `**Kosten.**`, `**Gegenvorschlag.**`,
`**Stellungnahme.**`, vor dem Punkt darf die Rolle in Klammern stehen; die Stellungnahme legt
der Absender leer an. Eine Rückfrage steht in der Stellungnahme, die Antwort des Absenders
darunter als `**Klärung.**`; beide kosten keine Runde. Unter jeder Frage an den Stakeholder
(`**F<n> · …**`) steht eine eigene Zeile `Antwort: .`; „.“ heißt bei `angenommen`: Die
Empfehlung gilt. Mechanismus: nur Text.

Der Status ist der letzte Zug; daraus folgt, wer dran ist.

Zug | setzt | Status | dann dran
---|---|---|---
stellen, neue Runde, Klärung | Absender | offen | Empfänger
nachfragen | Empfänger | rückfrage | Absender: klären
umsetzen, beantworten | Empfänger | angenommen | Absender: nachprüfen
widersprechen, Frage verwerfen | Empfänger, mit Begründung | abgelehnt | Absender: neue Runde oder `erledigt`
nach Runde 3/3 weiter uneins | Absender | eskaliert | Stakeholder: entscheidet
abschließen | Absender | erledigt | niemand: `anliegenregeln/erledigteLoeschen.py` löscht die Datei

Seine Züge in einem Anliegen setzt der Stakeholder im Formular des Dashboards: Es bietet nur
die Status an, die ihm die Tabelle zuweist, und je Frage ein Feld für die Antwort; eine
Legende im Anliegen entfällt (Anliegen 420). Mechanismus: `rollenregeln/dashboardAnliegenSeiten.py`
(`formular`), `rollenregeln/zuegeUebernehmen.py` ([Regeln](regeln.md#rollenregeln)).
Ein `Kommentar:` von ihm, der den Status nicht ändert, geht an die andere Rolle des Anliegens:
Sie antwortet mit einer Zeile `Stellungnahme:` darunter und ist bis dahin dran (Anliegen
384). Mechanismus: nur Text; der Stand nennt es noch nicht ([Backlog](backlog.md)).
Die Moderation verlinkt Fragen, er antwortet im Anliegen; ihre Vorschläge korrigiert er mit
einer Zeile `Kommentar:` darunter ([Moderator](../.claude/agents/moderator.md)). Mechanismus:
nur Text.

- Runde 3/3 ist die letzte: Der Zähler verhindert, dass zwei Rollen endlos diskutieren.
  Wäre danach eine weitere Runde nötig, setzt der Absender `eskaliert`; auch eine Hebung
  wählt dann der Stakeholder. Er schreibt seine Entscheidung ins Anliegen: zurück auf
  `Runde 1/3 · offen` oder eine andere Anweisung. Die Runde senkt und `eskaliert` ändert nur
  er; mit seiner Entscheidung setzt er auch den Kopf, sonst bleibt er dran. Mechanismus:
  `anliegenregeln/anliegen.py` (Runde höchstens 3), `anliegenregeln/anliegenDran.py` (bei
  `eskaliert` ist der Stakeholder dran); wer Runde und Status ändert, nur Text.
- Reicht der Empfänger einen Teil an eine andere Rolle weiter, setzt er `angenommen` erst,
  wenn jenes Anliegen erledigt ist; bis dahin trägt der Kopf `· wartet auf <nr>`.
  Mechanismus: nur Text.
- Den Status setzt, wem die Tabelle ihn zuweist; `erledigt` nur der Absender. Mechanismus:
  nur Text.
- Wer `angenommen`, `abgelehnt` oder `rückfrage` setzt, schreibt in der letzten Runde eine
  Stellungnahme mit Text: was umgesetzt ist und wo, die Begründung oder die Frage; dem
  Stakeholder genügen seine Antworten. Eine Stellungnahme in einer früheren Runde zählt
  nicht. Mechanismus: nur Text.
- Die Nummer ist eindeutig, der Absender eines Anliegens ändert sich nie; wer eine Nummer
  belegt vorfindet, nimmt die nächste freie. Mechanismus: nur Text.
- Ist der Stakeholder Absender, nennt der Stand die fällige Nachprüfung; er trägt
  `erledigt` selbst ein. Mechanismus: `standregeln/stand.py`.
- Den Status eines Anliegens an ihn setzt der Stakeholder selbst; die Freigabe beantwortet
  keine Frage. Mechanismus: nur Text; abweichend nennt der Stand nach einer Freigabe den
  Absender als dran (`anliegenregeln/anliegenDran.py`, `beantwortetDurchFreigabe`;
  [Backlog](backlog.md)).
- Niemand löscht ein committetes Anliegen von Hand; git ist das Archiv. Mechanismus:
  `anliegenregeln/erledigteLoeschen.py` (löscht erledigte), `rollenregeln/entfernen.py`
  (sperrt `rm` und `mv` committeter).
- Nach jedem Rollenlauf meldet ein Hook dem Koordinator die geänderten Status und wer dran
  ist, mit dessen Belegung. Mechanismus: `standregeln/stand.py` (PostToolUse auf Agent)
  nennt, wer dran ist und welche Nachprüfung fällig ist; geänderte Status und Belegung nur
  Text.
- Der Koordinator beauftragt die Rolle, die dran ist: Lief sie in diesem Chat und liegt ihre
  Belegung unter 120.000 Token, setzt er sie mit `SendMessage` fort, sonst startet er sie
  neu. Anliegen an eine Perspektive, deren Phase nicht läuft, warten, außer sie blockieren
  das Inkrement. Regelumsetzer und Organisationsentwickler laufen außerhalb der
  Prozessphase nur zu einem Anliegen, das das Produkt aufhält (eine Sperre zu Unrecht,
  Warten auf Prüfungen), oder das der Stakeholder „sofort“ nennt; die übrigen tragen
  `· wartet auf die Prozessphase` (Anliegen 630). Mechanismus: nur Text; der Stand nennt
  wartende nicht als dran: Anliegen 686.

## Budget
Gemessen wird nur die Belegung des Kontextfensters je Lauf, gleich für den Koordinator und
jede Rolle; der Stand zeigt sie. Die Zahl der Rollenläufe ist weder Budget noch Kennzahl.
Mechanismus: `standregeln/belegung.py`; der Stand nennt keine Rollenläufe (`standregeln/standTest.py`).
- Ab 120.000 Token meldet ein Hook; die Rolle beginnt nichts Neues und schließt ab, der
  Koordinator empfiehlt einen neuen Chat.
- Ab 150.000 Token sperrt ein Hook alles außer Schreiben im eigenen Pfad und der
  Schlussantwort. Beim Koordinator entscheidet der Stakeholder: freigeben (höhere Grenze in
  `.git/arbiter/belegungsgrenze.txt`), kürzen oder neuer Chat.
