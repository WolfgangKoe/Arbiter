# 0006 — Subagenten geben Großausgaben als Datei zurück, nicht in den Hauptkontext

**Datum:** 2026-06-22
**Status:** angenommen

## Kontext

Subagenten ([ADR-0005](0005-stehende-subagent-freigabe.md)) laufen in isoliertem
Kontext, damit Fleißarbeit das Opus-Hauptfenster schlank hält. Das Sparziel wird
aber **unterlaufen, wenn der Subagent sein Ergebnis als langen Text in den Chat
zurückgibt** — denn diese Rückgabe landet vollständig im Hauptkontext.

In S86 lieferten zwei Subagenten (Drift-Sweep + Arkana-Recherche) zusammen ~13k
Token an Digest direkt in den Chat zurück. Das trieb den Kontext über den
135k-Korridor — genau der Effekt, den die Subagent-Auslagerung verhindern soll.
Verwandt ist [ADR-0004](0004-skill-fetch-nur-per-subagent.md) (Skill-Fetch nur
per Subagent), das dieselbe Wurzel adressiert: große Inhalte dürfen den
Hauptkontext nicht fluten.

## Entscheidung

**Subagenten, die voluminöse oder dauerhaft nützliche Inhalte erzeugen
(Recherche-Digests, Schema-Entwürfe, lange Listen, gefetchte Inhalte), schreiben
diese in eine Datei und geben dem Orchestrator nur einen kurzen Verweis +
Kernbefunde zurück** — nicht den vollen Inhalt. Der Orchestrator liest die Datei
nur bei Bedarf und gezielt.

**Pflicht-Konvention je erzeugter Datei:** Der Subagent-Auftrag legt fest und die
Datei deklariert in ihrem Kopf, ob sie **dauerhaft** oder **temporär** ist:

- **Dauerhaft** — bleibt als Referenz/Artefakt (z. B. ein Plan-Companion wie
  `docs/audit/plans/archive/024-arkana-research-digest.md`). Lebt unter `docs/`.
- **Temporär** — Wegwerf-Zwischenstand; die Datei nennt **explizit das
  Lösch-Kriterium** („löschen nach Umsetzung von Plan 024 Step 6" o. ä.). Lebt
  unter einem klar temporären Pfad (z. B. `/tmp/` oder `docs/inbox/`), nie
  vermischt mit dauerhaften Artefakten.

Ohne diese Deklaration gilt die Datei als unklar und ist nachzubessern — kein
Artefakt ohne bekannte Lebensdauer.

## Konsequenzen

- Subagent-Briefs für Fleißarbeit enthalten künftig die Anweisung: „Ergebnis in
  Datei `<pfad>` schreiben; nur kurzen Verweis + Kernbefunde zurückgeben" plus
  die Permanent/Temporär-Festlegung samt Lösch-Kriterium.
- Der Token-Vorteil der Auslagerung bleibt auch bei großen Ergebnissen erhalten.
- Temporäre Dateien driften nicht zu Altlasten, weil ihr Lösch-Kriterium
  mitgeschrieben ist.
- `CLAUDE.md` (Token-Disziplin, Subagent-Muster) verweist auf diesen ADR.

## Review-Termin

Nächste Retrospektive, in der ein Subagent eine Großausgabe erzeugt — prüfen, ob
Verweis-statt-Volltext und die Lebensdauer-Deklaration eingehalten wurden.
