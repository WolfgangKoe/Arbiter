# Schreibpfade des Regelumsetzers ohne Linter-Konfiguration

293 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 279 F2 mit „ja“ beantwortet
(af45610): Der Regelumsetzer schreibt `eslint.config.mjs`, `.stylelintrc.json`, `package.json`,
`package-lock.json`. Die Schreibpfade in `.claude/agents/regelumsetzer.md` nennen keine der vier
Dateien; `rollenregeln/schreibgrenze.py` liest sie über `lesen/agenten.py` (`schreibpfade`) und
sperrt sie weiter. 279 ist erledigt, weil sein Erledigt-Kriterium erfüllt ist und die Datei an
der Grenze von 4.000 Zeichen steht; dieser Rest geht hierher.

**Kosten.** 268 und 276 (Moderation, Strang 2) bleiben blockiert, obwohl die Entscheidung
gefallen ist. Vier Zeilen.

**Gegenvorschlag.** Die vier Dateien in `schreibpfade:` von `.claude/agents/regelumsetzer.md`
aufnehmen. Die Zeile in [Ablauf, Kritik am Code](../../prozess/ablauf.md#kritik-am-code)
(„Linter-Konfiguration | Regelumsetzer | Architekt, Reviewer“) deckt sie schon ab; dort ist nichts
zu ändern.

**Stellungnahme.** Umgesetzt: Die vier Dateien stehen in `schreibpfade:` von
[Regelumsetzer](../../.claude/agents/regelumsetzer.md), dazu nennt „Was du tust“ eslint,
stylelint und `package.json` bei der Prüfkonfiguration. `lesen/agenten.py` (`darfSchreiben`)
gibt für alle vier wahr. Ablauf unverändert.
