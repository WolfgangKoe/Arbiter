# Ablauf

## Domänenphase
Der Stand nennt den nächsten Schritt; die Folge steht in `prozess/pruefungen/stand.py`.
1. Planer: Etappen aus dem Ziel; nur die aktuelle ausformuliert. Auslöser: keine Etappe.
2. Architekt: Kritik an der aktuellen Etappe und der Reihenfolge, als Anliegen.
3. Freigabe: „.“ → Koordinator committet `Freigabe Etappe <n>`.
4. Anforderungsautor, in jedem Zyklus: Anforderungen zum nächsten Schnitt, in Zyklus 1 zur
   Etappe, danach zum Zyklusziel des freigegebenen Reviews samt Kommentaren (ohne dieses zum
   Abschnitt „Danach“ des vorigen Plans); Begriffe ins Glossar. Eine genügt. Auslöser:
   kein Kriterium ohne Akzeptanztest. Bei einer Oberfläche danach
   [UX](../.claude/agents/ux.md): ein Mockup je Anforderung (DoR 5); das Item verlinkt es.
   Mechanismus: nur Text (der Stand nennt UX nicht).
5. Planer: `handoff/plan.md` (`# Plan · Zyklus <n>`) mit den Items, die bereit sind (DoR):
   eins genügt, höchstens drei; weicht er vom Zyklusziel des Reviews ab, begründet er es.
   Am Ende der Abschnitt `## Freigabe` ([Freigabe und Kommentare](#freigabe-und-kommentare)).
   Weitere Anforderungen kommen in späteren Zyklen. Jedes Item steht als Link
   `[…](../domaene/items/<id>.md)`; daran erkennt der Stand die Abnahme (Technikphase,
   Schritt 5). Mechanismus: `plan.py` (`itemsOhneLink`), `stand.py` nennt
   den Planer, solange der Link fehlt. Jedes Item nennt Kriterien ohne Test (`AUF-1.4`)
   oder ihre Anforderung; bis dahin ist der Plan nicht zur Freigabe bereit, der Stand nennt
   den Anforderungsautor, wenn es kein Kriterium ohne Test gibt, sonst den Planer.
   Mechanismus für 4 und diesen Satz: `stand.py` (`domänenphase`, `planOhneFreigabe`).
6. Kritik: Architekt an Anforderungen und Items; Format und Größe prüfen die Tests. Am
   Mockup: Fachkritiker (gegen die Kriterien), Architekt (nur vorhandene Komponenten).
7. Freigabe ([Freigabe und Kommentare](#freigabe-und-kommentare)) → Koordinator committet
   `Freigabe Plan <n>`. Danach Technikphase.

Kritik blockiert nicht: Offene Anliegen stehen in der Freigabevorlage, sortiert vom
Moderator (`handoff/moderation.md`). Mechanismus: nur Text. Gleichzeitig laufen
nur Rollen, die ausschließlich Anliegen schreiben.

### DoR (Item bereit)
1. Format und Höchstmaß von Anforderung und Item (`domaene/CLAUDE.md`), die Kriterien-IDs
   existieren.
2. Keine vagen Wörter; kursive Fachbegriffe stehen im Glossar (Wortanfang).
3. Regelbasierte Kriterien nennen ihre Fundstelle.
4. Abhängigkeiten erledigt, kein offenes Anliegen zum Item.
5. Bei einer Oberfläche: Mockup aus vorhandenen Komponenten. Gibt es noch keine
   Komponentenseite, bringt das Mockup sein CSS als Vorschlag mit; die Technikphase baut
   daraus die Komponentenseite.

Mechanismus für 1 bis 5: nur Text. Fachliche Vollständigkeit ist Urteil (Schritt 6) und
zeigt sich spätestens an den roten Tests.

## Technikphase
Auslöser: Stand „Technikphase“ nach `Freigabe Plan <n>`. Fehlen Rollen, schlägt der
Organisationsentwickler sie vor.
1. Testautor: Akzeptanztests je Kriterium der Items, rot.
2. Kritik: Fachkritiker (trifft der Test das Kriterium?), Architekt (Schnittstelle).
   Ein bemängelter Test geht nicht in die Umsetzung, bis das Anliegen geklärt ist;
   widerspricht der Testautor, wird es an den Anforderungsautor zum Kriterium gehoben. Der
   Rest läuft weiter. Mechanismus: nur Text.
3. Implementierer: macht die Tests grün. Refactoring nur aus einem Befund, als Anliegen an
   ihn von dem, der den Befund hat; der Gegenvorschlag nennt die Erledigt-Bedingung, dazu gilt
   „Verhalten unverändert“ (Akzeptanztests grün). Nach jedem Lauf prüft der Reviewer (Kritik
   am Code). Mechanismus: nur Text.
4. Reviewer: DoD über das Inkrement, `/code-review`, Wiederverwendung, Vereinfachung,
   Effizienz, Flughöhe.
5. Fachkritiker: fachliche Abnahme gegen Kriterien und Etappe. Danach löscht der Planer
   die abgenommenen Items. Mechanismus: `stand.py` nennt den Schritt, solange ein Item des
   Plans in `domaene/items/` liegt, auch wenn `review.md` schon Zyklus n trägt.
6. Reviewer: `handoff/review.md`, erste Zeile `# Review · Zyklus <n>`, vor dem Abschnitt
   `## Freigabe` der Abschnitt `## Nächstes Vorgehen` mit drei Punkten, je mit Beleg:
   - Produktziel: welche Etappen erreicht sind, was dem Ziel am meisten fehlt.
   - Etappenziel: was zur aktuellen Etappe fehlt, nach der Abnahme des Fachkritikers und dem
     Abschnitt „Danach“ des Plans; in wie vielen Zyklen sie erreichbar ist.
   - Zyklusziel: Empfehlung für Plan n+1, mit den technischen Voraussetzungen und Schulden,
     die vorher weg müssen.
   Der Reviewer fasst zusammen und empfiehlt; der Stakeholder entscheidet mit Freigabe und
   Kommentaren, der Planer schneidet die Items. Mechanismus: `freigabeFormat.py` (Abschnitt
   und drei Punkte); Inhalt und Beleg nur Text.
7. Freigabe ([Freigabe und Kommentare](#freigabe-und-kommentare)) → Koordinator committet
   `Freigabe Review <n>`. Danach meldet der Stand die Prozessphase. Mechanismus:
   `phasenfolge.py` (`lage`).

Ausnahmen vom Test vor dem Code: Oberfläche (Mockup zuerst, Bildschirmtest danach),
technisches Neuland (Wegwerf-Versuch, dann Test).

### DoD (Item fertig)
1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`;
   Zeilen und Zweige mindestens 95 % für `technik/arbiter` und, als eigene Meldung, für
   `prozess/pruefungen`. Mechanismus: `abdeckung.py`, für `technik/arbiter` im Lauf von
   `python3 -m pytest prozess/pruefungen`, für die Prüfskripte mit
   `python3 prozess/pruefungen/abdeckung.py` ([Regelumsetzer](../.claude/agents/regelumsetzer.md)).
2. Prüfmechanismen grün. Mechanismus: Benennung und Spiegel (`benennung.py`), Kriterium ↔
   Test (`rueckverfolgung.py`: Kennung höchstens einmal je Datei; ein Kriterium ohne Test ist
   rot, sobald ein offenes Item eines freigegebenen Plans es nennt, vorher nennt es der
   Stand), Höchstmaße (`hoechstmassTest.py`), Komplexität (`komplexitaetTest.py`), Code →
   Glossar (`glossar.py`), Kommentare und Docstrings nach `prozess/praemissen/wir.md` 8
   (`kommentare.py`), toter Code (vulture über `technik/arbiter` und
   `technik/tests/akzeptanz`, ohne Einheitstests: `unbenutzterCode` in `abdeckung.py`), alle
   im Lauf von `python3 -m pytest prozess/pruefungen`, ruff dort über `konfigurationTest.py`;
   SonarLint (Standardprofil ohne Namensregeln, Ordner nach [regeln.md](regeln.md)) mit
   `python3 prozess/pruefungen/sonarlint.py`, beim Commit auch als Hook. Urteil: Zeilen,
   die nur Einheitstests erreichen, beurteilt der Reviewer (Vorbedingung, fehlendes
   Kriterium oder tot); Glossar → Code.
3. Item gelöscht, die Anforderung beschreibt das gebaute Verhalten. Mechanismus: nur Text.
4. Review geschrieben, Fachkritik hat gegen Ziel, Etappe und Kriterien abgenommen (Urteil).
   Mechanismus: Stand (`stand.py`) erkennt das Review.

Kommen Mutationstests oder eine Oberfläche hinzu, gelten auch Mutationsschwelle der
geänderten Domänenmodule und Bildschirmtest grün, Mockup gelöscht.

Werkzeuge für die offenen Prüfungen (Regelumsetzer baut, Architekt kritisiert): mypy oder
pyright strikt, import-linter, complexipy (Schwelle 15), ruff (Stil, ARG, PLR2004, PLR0913,
FBT, ERA, `PLR0912` mit 12), Duplikaterkennung, semgrep für eigene Konventionen, cSpell mit deutschem Wörterbuch aus dem
Glossar, eslint und stylelint fürs Frontend. Die Sperre der Agenten ist mindestens so streng
wie SonarLint, die Sicht des Stakeholders; Mechanismus: `sonarlint.py` (DoD 2). Nicht verwendet: radon-Wartbarkeitsindex,
ruff-McCabe, ruff `PLR0911` (meldet frühes `return`).

## Prozessphase
Auslöser: `Freigabe Review <n>`.
1. Organisationsentwickler: `handoff/retro.md` (`# Retro · Zyklus <n>`) aus Anliegen an den
   Prozess, Kennzahlen (`prozess/kennzahlen.md`) und Auslösezählern (nur Text);
   Prozess-Items nur aus einem Befund. Dazu: Neuerungen von Claude Code, die einen eigenen
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
   `Freigabe Retro <n>` (auch als `Retro <n> P<k>: …`), meldet der Stand die Domänenphase
   mit Plan n+1, sonst das erste offene Item. Mechanismus: `phasenfolge.py`
   (`offenesProzessItem`, Anliegen 173).

Nach jeder Freigabe empfiehlt der Koordinator einen neuen Chat mit Startprompt
([Koordinator](../.claude/agents/koordinator.md)); den Stand bringt der Hook mit.
Mechanismus: nur Text.

Mechanismus der Übergänge: Stand-Hook (`prozess/pruefungen/stand.py`).

## Freigabe und Kommentare
Plan, Review und Retro enden mit diesem Abschnitt; der Autor legt ihn so an (Mechanismus:
`freigabeFormat.py`):
```
## Freigabe
Freigabe: offen
Kommentar: .
```
- Der Stakeholder kommentiert überall in der Datei: eine eigene Zeile `Kommentar: <Text>`
  unter der Stelle, die er meint; die letzte Zeile ist für Allgemeines. Zu anderen Dateien
  kommentiert er neben ihrem Link in Plan, Review oder Retro, in Anliegen mit `Antwort:`. Er gibt frei mit
  `Freigabe: ja`. Diese Zeilen ändert nur er. Mechanismus: nur Text (Anliegen 168).
- Nachkorrektur: Der Autor (Plan: Planer, Review: Reviewer, Retro: Organisationsentwickler)
  ändert die Datei nach dem Kommentar und schreibt darunter eine Zeile `Stellungnahme: <was,
  wo>`. Betrifft der Kommentar ein fremdes Artefakt oder braucht er eine Entscheidung, wird
  daraus ein Anliegen; die Stellungnahme nennt dessen Nummer. Solange ein Kommentar ohne
  Stellungnahme steht, ist der Autor dran, auch nach der Freigabe. Mechanismus:
  `freigabeKommentare.py`, `stand.py`; Anliegen und Inhalt der Stellungnahme nur Text.
- „.“ im Chat heißt: Die Datei ist durchgesehen. Steht `Freigabe: ja`, committet der
  Koordinator `Freigabe <Plan|Review|Retro> <n>`, auch wenn Kommentare offen sind; die
  Nachkorrektur folgt danach. Steht `Freigabe: offen`, beauftragt er den Autor und legt die
  Datei danach wieder vor. Mechanismus: `stand.py` nennt den Commit als nächsten Schritt;
  nur bei `Freigabe: ja` committen ist nur Text (Anliegen 168).
- Kommentare und Stellungnahmen bleiben, bis der Autor die Datei im nächsten Zyklus neu
  schreibt; Höchstmaß: [Kennzahlen](kennzahlen.md).
- Die Etappe gibt der Stakeholder mit „.“ im Chat frei.

## Rollen mit Auslöser
Der Organisationsentwickler schlägt eine Rolle vor, wenn ihr Auslöser eintritt.
Mechanismus: nur Text.
- Frontend-Implementierer: Der Reviewer findet wiederholt, dass ein Mockup beim Einbau
  umgeschrieben wurde (Anliegen 151).
- Prozesskritiker: Prozesskritik fehlt, oder der Organisationsentwickler verteidigt
  wiederholt eigene Regeln.
- Haiku-Zuarbeiter (Regel-Nachschlager, Belegprüfer): bei beobachtetem Bedarf, der
  Belegprüfer nach der ersten falschen Behauptung. Sie startet die Rolle, die das Ergebnis
  braucht.
- Testautor auf Opus: Fachkritik oder Mutationstests zeigen wiederholt fehlende Fälle.

## Kritik am Code
Nach jeder Änderung von Code (`prozess/praemissen/wir.md`) prüfen ihn alle Kritiker der
getroffenen Pfade, bevor die nächste Rolle darauf aufbaut. Befunde werden Anliegen an den Autor.

Code | schreibt | prüft
---|---|---
`technik/tests/akzeptanz/` | Testautor | Fachkritiker (Kriterium), Architekt (Schnittstelle, Lesbarkeit)
`technik/arbiter/`, `technik/tests/einheit/` | Implementierer | Reviewer
`prozess/pruefungen/`, `prozess/dashboard/`, `dashboard.html`, `.claude/settings.json` | Regelumsetzer | Reviewer
`pyproject.toml`, Linter-Konfiguration | Regelumsetzer | Architekt, Reviewer

Der Kritiker prüft den Commit des Autors. Der Koordinator committet den Kritiklauf, der
Betreff beginnt mit `Kritik` und nennt die kurzen Hashes der geprüften Commits
(`Kritik <a> <b>`, notfalls `--allow-empty`). Jeder andere Commit, der Code ändert, wird
geprüft, auch wenn sein Betreff „Kritik“ enthält; der Stand meldet den ersten seit der
letzten Freigabe ohne Kritik. Mechanismus: `codekritik.py` im Stand.

## Anliegen
Eine Datei je Diskussion: `handoff/anliegen/<nr>-<kurz>.md`, höchstens 4.000 Zeichen; jede
Zeile `Antwort:` zählt als `Antwort: .` (Anliegen 161). Mechanismus:
`hoechstmassTest.py` (`zeichenOhneAntworten`).
Erste Zeile `# <Titel>`, dritte Zeile der Kopf:
`<nr> · <Typ> · von <Rolle> → <Rolle> · Runde <n>/3 · <Status>`.
Typ: Kritik, Fragen oder Anliegen (Notiz des Stakeholders). Rolle: Name aus `.claude/agents/`
oder Stakeholder, dahinter darf die Perspektive in Klammern stehen. Je Runde Befund, Kosten,
Gegenvorschlag, Stellungnahme. Mechanismus: `anliegen.py`, `hoechstmassTest.py`.
Unter jeder Frage an den Stakeholder (`**F<n> · …**`) steht eine eigene Zeile `Antwort: .`;
„.“ heißt, die Empfehlung gilt. Die Freigabe beantwortet jede Frage, die in der
Freigabevorlage steht: mit der Zeile `Antwort:`, sonst mit der Empfehlung. Mechanismus: nur
Text.

Status | setzt | danach dran
---|---|---
offen | Absender, beim Anlegen und je neuer Runde | Empfänger: Stellung nehmen oder antworten
angenommen | Empfänger, nach der Umsetzung | Absender: nachprüfen
abgelehnt | Empfänger, mit Begründung | Absender: nächste Runde; nach Runde 3 `eskaliert`
beantwortet | Absender, nach der Freigabe | Absender: Antworten einarbeiten
eskaliert | Absender, wenn nach Runde 3/3 eine weitere Runde nötig wäre | Stakeholder: entscheidet
erledigt | Absender, wenn in Ordnung | niemand: `erledigteLoeschen.py` löscht die Datei

- Runde 3/3 ist die letzte: Der Zähler verhindert, dass zwei Rollen endlos diskutieren.
  Wäre danach eine weitere Runde nötig, setzt der Absender `eskaliert`; auch eine Hebung
  wählt dann der Stakeholder. Er schreibt seine Entscheidung ins Anliegen: zurück auf
  `Runde 1/3 · offen` oder eine andere Anweisung. Die Runde senkt und `eskaliert` ändert nur
  er; mit seiner Entscheidung setzt er auch den Kopf, sonst bleibt er dran. Mechanismus:
  `anliegen.py` (Runde höchstens 3, bei `eskaliert` ist der Stakeholder dran),
  `statusrecht.py` (Rollen senken keine Runde, ändern `eskaliert` nicht und setzen in
  Runde 3/3 nach `abgelehnt` nur `eskaliert` oder `erledigt`).
- Reicht der Empfänger einen Teil an eine andere Rolle weiter, setzt er `angenommen` erst,
  wenn jenes Anliegen erledigt ist; bis dahin endet seine Stellungnahme mit „wartet auf <nr>“.
  Mechanismus: nur Text.
- Den Status setzt, wem die Tabelle ihn zuweist; `erledigt` nur der Absender. Mechanismus:
  `statusrecht.py` (Write, Edit).
- Ist der Stakeholder Absender, nennt der Stand die fällige Nachprüfung; er trägt
  `erledigt` selbst ein. Mechanismus: `stand.py`.
- Ein Anliegen an den Stakeholder mit Status `offen`, das im Commit der letzten Freigabe
  (Betreff `Freigabe …`) schon in derselben Runde `offen` war, hat die Freigabe beantwortet:
  Dran ist der Absender, er setzt `beantwortet` und arbeitet die Antworten ein. Notizen und
  ersetzte Links ändern daran nichts, erst eine neue Runde des Absenders. Mechanismus:
  `anliegen.py` (`beantwortetDurchFreigabe`, `wartetAuf`), `gitAufruf.py` (`letzteFreigabe`).
- Rollen ändern Anliegen nur mit Write und Edit, nie per Bash: Daran vorbei greift
  `statusrecht.py` nicht, das Löschen schon. Mechanismus: `bashPositivliste.py`, eine
  Heuristik (Umleitung, `rm`, `mv`, `cp`, `sed -i`, `tee`). Sie erkennt keine Skripte
  (Heredoc, `python3 -c`) und kein `cd <pfad> && …`; dort, und ebenso für die nur lesbaren
  Pfade, gilt die Regel als nur Text (Anliegen 138).
- Niemand löscht ein Anliegen von Hand; git ist das Archiv. Mechanismus:
  `erledigteLoeschen.py`.
- Nach jedem Rollenlauf meldet ein Hook dem Koordinator die geänderten Status und wer dran
  ist, mit dessen Belegung. Mechanismus: nur Text (heute nennt der Stand beim Start die
  fälligen Nachprüfungen mit Rolle).
- Der Koordinator beauftragt die Rolle, die dran ist: Lief sie in diesem Chat und liegt ihre
  Belegung unter 120.000 Token, setzt er sie mit `SendMessage` fort, sonst startet er sie
  neu. Anliegen an eine Perspektive, deren Phase nicht läuft, warten, außer sie blockieren
  das Inkrement. Mechanismus: nur Text.

## Budget
Gemessen wird nur die Belegung des Kontextfensters je Lauf, gleich für den Koordinator und
jede Rolle; der Stand zeigt sie. Die Zahl der Rollenläufe ist weder Budget noch Kennzahl.
Mechanismus: `belegung.py`; der Stand nennt keine Rollenläufe (`standTest.py`).
- Ab 120.000 Token meldet ein Hook; die Rolle beginnt nichts Neues und schließt ab, der
  Koordinator empfiehlt einen neuen Chat.
- Ab 150.000 Token sperrt ein Hook alles außer Schreiben im eigenen Pfad und der
  Schlussantwort. Beim Koordinator entscheidet der Stakeholder: freigeben (höhere Grenze in
  `.git/arbiter/belegungsgrenze.txt`), kürzen oder neuer Chat.
