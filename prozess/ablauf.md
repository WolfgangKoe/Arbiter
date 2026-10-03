# Ablauf

## Domänenphase
Der Stand nennt den nächsten Schritt; die Folge steht in `prozess/pruefungen/stand.py`.
1. Planer: Etappen aus dem Ziel; nur die aktuelle ausformuliert. Auslöser: keine Etappe.
2. Architekt: Kritik an der aktuellen Etappe und der Reihenfolge, als Anliegen.
3. Freigabe: „.“ → Koordinator committet `Freigabe Etappe <n>`.
4. Anforderungsautor: die erste Anforderung zur Etappe, Begriffe ins Glossar. Eine genügt.
5. Planer: `handoff/plan.md` (`# Plan · Zyklus <n>`) mit den Items, die bereit sind:
   eins genügt, höchstens drei. Weitere Anforderungen kommen in späteren Zyklen.
6. Kritik: Architekt an Anforderungen und Items; Format und Größe prüfen die Tests.
7. Freigabe: „.“ → Koordinator committet `Freigabe Plan <n>`. Danach Technikphase.

Kritik blockiert nicht: Offene Anliegen stehen in der Freigabevorlage. Gleichzeitig laufen
nur Rollen, die ausschließlich Anliegen schreiben.

## Technikphase
Auslöser: Stand „Technikphase“ nach `Freigabe Plan <n>`. Fehlen Rollen, schlägt der
Organisationsentwickler sie vor.
1. Testautor: Akzeptanztests je Kriterium der Items, rot.
2. Kritik: Fachkritiker (trifft der Test das Kriterium?), Architekt (Schnittstelle).
   Ein bemängelter Test geht nicht in die Umsetzung, bis das Anliegen geklärt ist;
   widerspricht der Testautor, wird es an den Anforderungsautor zum Kriterium gehoben. Der
   Rest läuft weiter. Mechanismus: nur Text.
3. Implementierer: macht die Tests grün; Refactoring nur aus einem Befund. Nach jedem Lauf
   prüft der Reviewer (Kritik am Code).
4. Reviewer: DoD über das Inkrement, `/code-review`, Wiederverwendung, Vereinfachung,
   Effizienz, Flughöhe.
5. Fachkritiker: fachliche Abnahme gegen Kriterien und Etappe. Danach löscht der Planer
   die abgenommenen Items.
6. Reviewer: `handoff/review.md`, erste Zeile `# Review · Zyklus <n>`. Danach meldet der
   Stand die Prozessphase; eine Freigabe ist nicht nötig.

### DoD (Item fertig)
1. Akzeptanz-, Gesamt- und Architekturtests grün: `python3 -m pytest technik/tests`.
   Mechanismus: nur Text.
2. Prüfmechanismen grün: ruff, Benennung (`prozess/praemissen/wir.md`), toter Code,
   Komplexität, Kommentaranteil, Spiegel, Glossar ↔ Code, Höchstmaße, Rückverfolgung.
   Mechanismus: nur Text.
3. Item gelöscht, die Anforderung beschreibt das gebaute Verhalten. Mechanismus: nur Text.
4. Review geschrieben, Fachkritik hat gegen Ziel, Etappe und Kriterien abgenommen (Urteil).
   Mechanismus: Stand (`stand.py`) erkennt das Review.

Kommen Mutationstests oder eine Oberfläche hinzu, gelten auch Mutationsschwelle der
geänderten Domänenmodule und Bildschirmtest grün, Mockup gelöscht.

## Prozessphase
Auslöser: Review n liegt vor.
1. Organisationsentwickler: `handoff/retro.md` (`# Retro · Zyklus <n>`) aus Anliegen an den
   Prozess, Kennzahlen und Auslösezählern; Prozess-Items nur aus einem Befund.
2. Regelumsetzer: Mechanismen zu den Prozess-Items, je mit Scheiter-Test.
3. Kritik: Domäne und Technik an Regeländerungen, als Anliegen.
4. Freigabe: Der Stakeholder schreibt „.“, der Koordinator committet `Freigabe Retro <n>`.
   Danach meldet der Stand die Domänenphase mit Plan n+1.

Nach jeder Freigabe empfiehlt der Koordinator einen neuen Chat; den Stand bringt der Hook mit.

Mechanismus der Übergänge: Stand-Hook (`prozess/pruefungen/stand.py`).

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
ohne Kritik. Mechanismus: nur Text.

## Anliegen
Eine Datei je Diskussion: `handoff/anliegen/<nr>-<kurz>.md`, höchstens 4.000 Zeichen
(Mechanismus: `test_hoechstmasse.py`, Wert noch 2.400). Erste Zeile `# <Titel>`, dritte Zeile
der Kopf, maschinenlesbar: `<nr> · <Typ> · von <Rolle> → <Rolle> · Runde <n>/3 · <Status>`.
Typ: Kritik, Fragen oder Anliegen (Notiz des Stakeholders). Rolle: Name aus `.claude/agents/`
oder Stakeholder, dahinter darf die Perspektive in Klammern stehen. Je Runde Befund, Kosten,
Gegenvorschlag, Stellungnahme. Mechanismus: nur Text.

Status | setzt | danach dran
---|---|---
offen | Absender, beim Anlegen und je neuer Runde | Empfänger: Stellung nehmen oder antworten
angenommen | Empfänger, nach der Umsetzung | Absender: nachprüfen
abgelehnt | Empfänger, mit Begründung | Absender: nächste Runde; nach Runde 3 Hebung oder `eskaliert`
beantwortet | Stakeholder | Absender: Antworten einarbeiten
eskaliert | Absender, nach Runde 3 | Stakeholder
erledigt | Absender, wenn in Ordnung | niemand: Datei im selben Lauf löschen

- Jede Rolle setzt den Status der Anliegen, die sie schreibt oder empfängt. Ist der
  Stakeholder Absender, prüft er bei der nächsten Freigabe nach; „.“ heißt erledigt, dann
  löscht der Empfänger. Mechanismus: nur Text.
- Ein Anliegen mit Status `erledigt` hält `python3 -m pytest prozess/pruefungen` rot, bis es
  gelöscht ist; git ist das Archiv. Mechanismus: nur Text.
- Nach jedem Rollenlauf meldet ein Hook dem Koordinator die geänderten Status und wer dran
  ist, mit dessen Belegung. Mechanismus: nur Text.
- Der Koordinator beauftragt die Rolle, die dran ist: Lief sie in diesem Chat und liegt ihre
  Belegung unter 120.000 Token, setzt er sie mit `SendMessage` fort, sonst startet er sie
  neu. Anliegen an eine Perspektive, deren Phase nicht läuft, warten, außer sie blockieren
  das Inkrement. Mechanismus: nur Text.

## Budget
Gemessen wird die Belegung des Kontextfensters je Lauf, gleich für den Koordinator und jede
Rolle ([Anliegen 22](../handoff/anliegen/22-dashboard-und-budget-am-kontextfenster.md)):
- Ab 120.000 Token beginnt die Rolle nichts Neues und schließt ab; der Koordinator empfiehlt
  einen neuen Chat. Mechanismus: nur Text.
- Bei 150.000 Token sperrt ein Hook alles außer Schreiben im eigenen Pfad und der
  Schlussantwort. Beim Koordinator entscheidet der Stakeholder: freigeben, kürzen oder neuer
  Chat. Mechanismus: nur Text.

Rollenläufe je Phase bleiben Kennzahl (`rollenzaehler.py`, Domäne 8, Technik 10, Prozess 5);
bis die Messung steht, zeigt der Stand sie als Budget.
