# SonarLint rot in anwendung.py

1630 · Kritik · von Reviewer → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** DoD über das Inkrement von Plan 6 ([Ablauf, DoD 2](../../prozess/ablauf.md#dod-item-fertig)).
`python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint` endet mit 1, dreimal
`python:S6353` in [anwendung.py](../../technik/arbiter/web/anwendung.py), Zeile 26
(`_jsonZahlText`): „Use concise character class syntax '\d' instead of '[0-9]'“.
Sonst grün: `pytest technik/tests` 733, `pytest prozess/pruefungen` 743.

Nach [Ich 3](../../prozess/praemissen/ich.md) hält es auf: Eine Prüfung ist rot. Der Hook
`sonarlint` lässt den Commit des Items scheitern ([Ablauf, Commits](../../prozess/ablauf.md#commits)).

**Kosten.** Ohne Behebung kein Commit der Items einheitVerschieben und anhaltenAnBases.

**Gegenvorschlag.** `\d` mit `re.ASCII` statt `[0-9]`, etwa
`re.compile(r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?", re.ASCII)`. Ohne `re.ASCII` nähme `\d`
auch andere Ziffern an; `json.loads` lehnte sie zwar ab (`ValueError`, schon abgefangen),
aber das Muster soll V5 allein tragen. Eine Zeile in der Parametrisierung von
`testEineAbfrageDerStelleBeimLoslassenOhneZahlen…` mit einer arabisch-indischen Ziffer
belegt es.

Erledigt: SonarLint ohne Fund, Unit- und Akzeptanztests grün.

**Stellungnahme.** Angenommen. Das Muster in `_jsonZahlText` nutzt `\d` mit `re.ASCII`; in der
Parametrisierung steht eine arabisch-indische Ziffer, die 400 ergibt. Meine frühere Begründung
für `[0-9]` gilt damit weiter, ohne die Prüfung zu verletzen. Status: umgesetzt, wartet auf
den Absender.
