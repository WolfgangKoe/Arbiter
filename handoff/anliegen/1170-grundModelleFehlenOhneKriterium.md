# Grund „Modelle fehlen“ ohne Kriterium

1170 · Kritik · von Anforderungsautor → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, denn eine Prüfung ist rot.
[setzenPerKlick](../../domaene/items/setzenPerKlick.md) streicht AUF-10.2 mit seinem Test, und
nach [1121](1121-entfalleneKriterienStehenNoch.md) steht das Kriterium nicht mehr in
[beenden.md](../../domaene/anforderungen/phasen/aufstellen/beenden.md). Kein anderes Kriterium
nennt die *Sperre* ‚Modelle fehlen‘. Der Code hat sie noch: `Grund.modelleFehlen` in
`technik/arbiter/domaene/sperre.py` und die Prüfung dazu in
`technik/arbiter/domaene/phasen/aufstellen/beenden.py`. Deshalb ist
`formregeln/glossar.py` rot.

**Kosten.** Rot bleibt der Commit gesperrt. Ein Eintrag im Glossar wäre kein Ausweg, denn
der Begriff hätte kein Kriterium. Das wäre erfunden.

**Gegenvorschlag.** Den *Grund* ‚Modelle fehlen‘ und seine Prüfung beim *Aufstellen der
Einheit beenden* aus dem Code nehmen. *Beenden* sperrt dann nur nach AUF-10.3.

Erledigt, wenn `python3 -m pytest prozess/pruefungen/formregeln/glossarTest.py` grün ist.

**Stellungnahme.** Angenommen und umgesetzt: `Grund.modelleFehlen` und seine Prüfung sind aus
dem Code, *Beenden* sperrt nur nach AUF-10.3. `glossarTest.py` ist grün.
