# Handoff — Übergabe & Stakeholder-Mailbox

Dieser Ordner ist der gemeinsame Übergabe-Ort des Multi-Agenten-Modells
([ADR-0007](../governance/decisions/0007-duenner-koordinator-und-datei-kanal.md)). Er trägt zwei
Dinge, damit der **dünne Koordinator** keine vollen Inhalte in seinen Kontext ziehen muss:

1. **Ergebnis-Übergabe** — ein Subagent legt voluminöse/dauerhafte Ergebnisse hier ab und gibt dem
   Koordinator nur **Pfad + Kernbefunde** zurück ([ADR-0006](../governance/decisions/0006-subagent-grossausgaben-als-datei.md)).
2. **Stakeholder-Mailbox (asynchron)** — ein Subagent kann nicht blockierend auf den Stakeholder
   warten. Er schreibt seine Entscheidungsfrage hierher, **beendet seinen Lauf**, und wird später
   per `SendMessage` mit intaktem Kontext wieder geweckt.

## Status-Marker (Kopfzeile jeder Datei)

Jede Handoff-Datei deklariert in ihrer **ersten Zeile** einen Status:

| Marker | Bedeutung | Wer handelt als Nächstes |
|---|---|---|
| `STATUS: DONE` | Ergebnis fertig → Erkenntnisse in Backlog/Spec überführen, **Datei löschen** (DoD Punkt 7) | wer den Marker setzt, löscht im selben Schritt |
| `STATUS: NEEDS-APPROVAL` | Planungs-Entwurf der laufenden Session — vom Stakeholder freizugeben/freigegeben; bleibt bis zum Session-Abschluss, dann ANSWERED setzen und im selben Abschluss löschen (Inhalt vorher in briefing/backlog überführt) | Koordinator legt vor → Stakeholder freigeben → Abschluss löscht |
| `STATUS: NEEDS-DECISION` | Subagent braucht eine Stakeholder-Entscheidung | Koordinator legt vor → Stakeholder antwortet |
| `STATUS: ANSWERED` | Stakeholder hat geantwortet (Antwort steht in der Datei) | Koordinator weckt den Subagenten per `SendMessage` **oder** überführt die Antwort direkt in Backlog/Spec — dann **im selben Abschluss löschen** (kein „behalten bis X" mehr, S156-Retro Maßnahme 7) |
| `STATUS: IN-PROGRESS` | Subagent arbeitet noch / mehrteilig — nur **während** eines Laufs; vor Lauf-Ende auf einen der drei anderen Marker setzen (der Wächter akzeptiert nur diese) | — |
| `STATUS: STANDING` | Dauerhafter Eingangskanal (z. B. Stakeholder-Beobachtungen) — Datei wird **nie gelöscht**, auch nicht leer; Inhalt wird bei Bedarf in Backlog/Spec überführt, die Datei selbst bleibt (S134-Stakeholder-Entscheid) | wer den Inhalt überführt, leert die Datei — löscht sie nicht |
| `STATUS: AWAITING-VERIFICATION` | Ergebnis fertig, aber Render-Code ist nicht von der Coverage erfasst (`CLAUDE.md`) → wartet auf die manuelle Stakeholder-Sichtprüfung des UI-Effekts (DoD Punkt 6). Keine Entscheidungsfrage — ersetzt die bisherige Fehlnutzung von `NEEDS-DECISION` für reine Sichtprüfungen (Retro-M1, S160/S161). | Stakeholder führt den in der Datei genannten Klickpfad aus, trägt Ergebnis ein → Koordinator setzt `ANSWERED` (bei Nacharbeit) oder direkt `DONE` (bei reiner Bestätigung) und löscht im selben Abschluss (bestehende ANSWERED/DONE-Konvention) |

**Wächter (S120, verschärft S156-Retro Maßnahme 7):** `tests/docs/test_handoff_hygiene.py`
bricht den Build, wenn Zeile 1 nicht mit `STATUS:` + `NEEDS-DECISION`/`ANSWERED`/`DONE`/
`STANDING`/`NEEDS-APPROVAL`/`AWAITING-VERIFICATION` beginnt — oder wenn ein `DONE`- **oder**
`ANSWERED`-Handoff liegen bleibt. `DONE` und `ANSWERED` sind damit beide **Durchgangszustände**
(Setzen + Löschen im selben Abschluss), kein Ablagezustand mehr — der Wächter erzwingt das
absichtlich, statt einen Bug zu markieren. `AWAITING-VERIFICATION` ist dagegen **nicht**
stale-pflichtig wie `DONE`/`ANSWERED` — er darf über Sessions hinweg liegen bleiben, weil er auf
den Stakeholder wartet (analog `NEEDS-DECISION`); wer den Folgemarker (`ANSWERED`/`DONE`) setzt,
löscht im selben Schritt.

**UI-Verifikations-Befunde überleben die Löschung:** Bevor eine `AWAITING-VERIFICATION`-Datei
(bzw. ihr Folgemarker `ANSWERED`/`DONE`) gelöscht wird, wandert ihr **Befund** (Datum · Roster ·
Klickpfad/Ergebnis · Quelle) als neuer Abschnitt nach `docs/spec/ui_verification_log.md` — ein
dauerhaftes, append-only Nachschlagewerk. Die Handoff-Datei selbst folgt weiterhin unverändert
ihrer normalen Lebenszyklus-Pflicht (Setzen + Löschen im selben Abschluss); nur der Befund wird
vorher ausgelagert, statt beim Löschen verloren zu gehen (Stakeholder-Entscheid S179, Option (a)).

## Mailbox-Round-Trip (Ablauf)

1. Subagent stößt auf eine Entscheidungsfrage → schreibt sie hierher, Marker `NEEDS-DECISION`,
   **beendet den Lauf** (gibt dem Koordinator nur Pfad + Marker zurück).
2. Koordinator reicht die Frage **wortgleich** an den Stakeholder durch (Herkunft nennen).
3. Stakeholder schreibt die Antwort in dieselbe Datei (oder sagt sie dem Koordinator, der sie
   einträgt) → Marker `ANSWERED`.
4. Koordinator weckt **denselben** Subagenten per `SendMessage` → er liest die Datei und macht weiter.

## Datei-Konvention

- **Name:** `<thema-oder-agent>-S<NN>.md` (z. B. `context-audit-S91.md`, `reviewer-plan025-S102.md`).
- **Lebensdauer (Pflicht, [ADR-0006](../governance/decisions/0006-subagent-grossausgaben-als-datei.md)):**
  jede Datei deklariert im Kopf **dauerhaft** oder **temporär**; temporäre nennen ihr
  **Lösch-Kriterium** explizit („löschen nach Umsetzung von X").
- **Lebenszyklus:** lesen → arbeiten → auslagern → **löschen**. Erledigte temporäre Handoffs werden
  entfernt, nicht angesammelt — der Ordner bleibt klein.
