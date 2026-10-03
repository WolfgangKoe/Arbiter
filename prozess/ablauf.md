# Ablauf

## Domänenphase
Der Stand nennt den nächsten Schritt; die Folge steht in `prozess/pruefungen/stand.py`.
1. Planer: Etappen aus dem Ziel; nur die aktuelle ausformuliert. Auslöser: keine Etappe.
2. Architekt: Kritik an der aktuellen Etappe und der Reihenfolge, als Anliegen.
3. Freigabe: „.“ → Koordinator committet `Freigabe Etappe <n>`.
4. Anforderungsautor: die erste Anforderung zur Etappe, Begriffe ins Glossar. Eine genügt.
5. Planer: `handoff/plan.md` (`# Plan · Zyklus <n>`) mit den Items, die bereit sind (DoR):
   eins genügt, höchstens drei. Weitere Anforderungen kommen in späteren Zyklen. Jedes
   Item steht als Link `[…](../domaene/items/<id>.md)`; daran erkennt der Stand die Abnahme
   (Technikphase, Schritt 5). Mechanismus: nur Text
   ([Anliegen 76](../handoff/anliegen/76-planOhneItemLink.md)).
6. Kritik: Architekt an Anforderungen und Items; Format und Größe prüfen die Tests.
7. Freigabe: „.“ → Koordinator committet `Freigabe Plan <n>`. Danach Technikphase.

Kritik blockiert nicht: Offene Anliegen stehen in der Freigabevorlage, sortiert vom
Moderator (`handoff/moderation.md`). Mechanismus: nur Text. Gleichzeitig laufen
nur Rollen, die ausschließlich Anliegen schreiben.

### DoR (Item bereit)
1. Format und Höchstmaß von Anforderung und Item (`domaene/CLAUDE.md`), die Kriterien-IDs
   existieren.
2. Keine vagen Wörter; kursive Fachbegriffe stehen im Glossar (Wortanfang).
3. Regelbasierte Kriterien nennen ihre Fundstelle.
4. Abhängigkeiten erledigt, kein offenes Anliegen zum Item.
5. Bei einer Oberfläche: Mockup aus vorhandenen Komponenten.

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
6. Reviewer: `handoff/review.md`, erste Zeile `# Review · Zyklus <n>`. Danach meldet der
   Stand die Prozessphase; eine Freigabe ist nicht nötig.

Ausnahmen vom Test vor dem Code: Oberfläche (Mockup zuerst, Bildschirmtest danach),
technisches Neuland (Wegwerf-Versuch, dann Test).

### DoD (Item fertig)
1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`.
   Mechanismus: nur Text.
2. Prüfmechanismen grün. Mechanismus: Benennung (`benennung.py`), Kriterium ↔ Test
   (`rueckverfolgung.py`), Höchstmaße (`hoechstmassTest.py`), alle im Lauf von
   `python3 -m pytest prozess/pruefungen`, ruff dort über `konfigurationTest.py`. Nur Text:
   toter Code, Komplexität, Kommentare nach `prozess/praemissen/wir.md`, Spiegel,
   Glossar ↔ Code.
3. Item gelöscht, die Anforderung beschreibt das gebaute Verhalten. Mechanismus: nur Text.
4. Review geschrieben, Fachkritik hat gegen Ziel, Etappe und Kriterien abgenommen (Urteil).
   Mechanismus: Stand (`stand.py`) erkennt das Review.

Kommen Mutationstests oder eine Oberfläche hinzu, gelten auch Mutationsschwelle der
geänderten Domänenmodule und Bildschirmtest grün, Mockup gelöscht.

Werkzeuge für die offenen Prüfungen (Regelumsetzer baut, Architekt kritisiert): mypy oder
pyright strikt, import-linter, complexipy (Schwelle 15), ruff `PLR0912` (12), vulture nur über den Produktcode,
Duplikaterkennung, semgrep für eigene Konventionen, cSpell mit deutschem Wörterbuch aus dem
Glossar, eslint und stylelint fürs Frontend. Die Sperre der Agenten ist mindestens so streng
wie SonarLint, die Sicht des Stakeholders. Nicht verwendet: radon-Wartbarkeitsindex,
ruff-McCabe, ruff `PLR0911` (meldet frühes `return`).

## Prozessphase
Auslöser: Review n liegt vor.
1. Organisationsentwickler: `handoff/retro.md` (`# Retro · Zyklus <n>`) aus Anliegen an den
   Prozess, Kennzahlen (`prozess/kennzahlen.md`) und Auslösezählern (nur Text);
   Prozess-Items nur aus einem Befund. Dazu: Neuerungen von Claude Code, die einen eigenen
   Mechanismus ersetzen; wiederholte Entscheidungen des Stakeholders als Vorschlag für eine
   Prämisse; eine wiederholt verletzte Prämisse ohne Mechanismus als Prozess-Item. Ist eine
   Etappe erreicht, legt er `doku/` an oder pflegt es: für Menschen, keine CLAUDE.md verweist
   darauf; grafisch und kurz, nur Seltenes (Perspektiven, Rollen, Ordner), Rollentabelle und
   Ordnerbaum per Skript. Mechanismus: nur Text.
2. Regelumsetzer: Mechanismen zu den Prozess-Items, je mit Scheiter-Test.
3. Kritik: Domäne und Technik an Regeländerungen, als Anliegen.
4. Freigabe: Der Stakeholder schreibt „.“, der Koordinator committet `Freigabe Retro <n>`.
   Danach meldet der Stand die Domänenphase mit Plan n+1.

Nach jeder Freigabe empfiehlt der Koordinator einen neuen Chat mit Startprompt
([Koordinator](../.claude/agents/koordinator.md)); den Stand bringt der Hook mit.
Mechanismus: nur Text.

Mechanismus der Übergänge: Stand-Hook (`prozess/pruefungen/stand.py`).

## Rollen mit Auslöser
Der Organisationsentwickler schlägt eine Rolle vor, wenn ihr Auslöser eintritt.
Mechanismus: nur Text.
- UX: erstes Item mit Oberfläche. Schreibt einbaufähige Mockups: statisches HTML mit dem
  echten CSS, ohne JS-Logik, nur Inhalte aus Kriterien oder Katalogdaten, ein Mockup je
  Anforderung, gelöscht nach dem Einbau.
- Prozesskritiker: Prozesskritik fehlt, oder der Organisationsentwickler verteidigt
  wiederholt eigene Regeln.
- Haiku-Zuarbeiter (Regel-Nachschlager, Belegprüfer): bei beobachtetem Bedarf, der
  Belegprüfer nach der ersten falschen Behauptung. Sie startet die Rolle, die das Ergebnis
  braucht.
- Testautor auf Opus: Fachkritik oder Mutationstests zeigen wiederholt fehlende Fälle.

## Kritik am Code
Nach jeder Änderung von Code (`prozess/praemissen/wir.md`) prüft ihn ein passender Kritiker,
bevor die nächste Rolle darauf aufbaut. Befunde werden Anliegen an den Autor.

Code | schreibt | prüft
---|---|---
`technik/tests/akzeptanz/` | Testautor | Fachkritiker (Kriterium), Architekt (Schnittstelle, Lesbarkeit)
`technik/arbiter/`, `technik/tests/einheit/` | Implementierer | Reviewer
`prozess/pruefungen/`, `.claude/settings.json` | Regelumsetzer | Reviewer
`pyproject.toml`, Linter-Konfiguration | Regelumsetzer | Architekt, Reviewer

Der Kritiker prüft den Commit des Autors. Der Koordinator committet den Kritiklauf als
`Kritik <kurzer Hash>` (notfalls `--allow-empty`); der Stand meldet den ersten Code-Commit
ohne Kritik. Mechanismus: `codekritik.py` im Stand.

## Anliegen
Eine Datei je Diskussion: `handoff/anliegen/<nr>-<kurz>.md`, höchstens 4.000 Zeichen.
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
abgelehnt | Empfänger, mit Begründung | Absender: nächste Runde; nach Runde 3 Hebung (Test → Kriterium → Anforderung, Code → Architektur) oder `eskaliert`
beantwortet | Absender, nach der Freigabe | Absender: Antworten einarbeiten
eskaliert | Absender, nach Runde 3 | Stakeholder
erledigt | Absender, wenn in Ordnung | niemand: `erledigteLoeschen.py` löscht die Datei

- Reicht der Empfänger einen Teil an eine andere Rolle weiter, setzt er `angenommen` erst,
  wenn jenes Anliegen erledigt ist; bis dahin endet seine Stellungnahme mit „wartet auf <nr>“.
  Mechanismus: nur Text.
- Den Status setzt, wem die Tabelle ihn zuweist; `erledigt` nur der Absender. Mechanismus:
  `statusrecht.py` (Write, Edit).
- Ist der Stakeholder Absender, nennt der Stand die fällige Nachprüfung; er trägt
  `erledigt` selbst ein. Mechanismus: `stand.py`.
- Rollen ändern Anliegen nur mit Write und Edit, nie per Bash: Daran vorbei greift
  `statusrecht.py` nicht, das Löschen schon. Mechanismus: nur Text.
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
Gemessen wird die Belegung des Kontextfensters je Lauf, gleich für den Koordinator und jede
Rolle; der Stand zeigt sie. Mechanismus: `belegung.py`.
- Ab 120.000 Token meldet ein Hook; die Rolle beginnt nichts Neues und schließt ab, der
  Koordinator empfiehlt einen neuen Chat.
- Ab 150.000 Token sperrt ein Hook alles außer Schreiben im eigenen Pfad und der
  Schlussantwort. Beim Koordinator entscheidet der Stakeholder: freigeben (höhere Grenze in
  `.git/arbiter/belegungsgrenze.txt`), kürzen oder neuer Chat.
