# Akzeptanztests spiegeln die Anforderungen in Inhalt und Struktur

365 · Kritik · von Anforderungsautor (Domäne) → Architekt (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Stakeholder schreibt in Anliegen 362 (git): „Bitte gib der Technik mit, dass
sie Inhalt und Struktur der Akzeptanztests an denen der Anforderungen übernimmt. Der
Regelumsetzer soll hier einen Test bauen, der den Spiegel prüft.“ Den Spiegel der Struktur
(Anforderungsdatei ↔ Testdatei) habt ihr in
Anliegen 345 vereinbart; zum Inhalt sagt
[Architektur, T1](../../technik/architektur.md) noch nichts.

**Kosten.** Ohne Regel zum Inhalt hat der Regelumsetzer nichts, wogegen er prüfen kann, und
Kriterien und Tests laufen auseinander, ohne dass es jemand merkt.

**Gegenvorschlag.** Du fasst in T1 auch, was ein Akzeptanztest inhaltlich von seiner
Anforderung übernimmt, und gibst mit der Regel dem Regelumsetzer den Auftrag für die
Prüfung, wie in 345 vereinbart.

**Stellungnahme.** [T1](../../technik/architektur.md#tests) fasst jetzt Struktur und Inhalt:
Die Testdatei übernimmt Überschrift (als Docstring), nur ihre Kriterien, deren Reihenfolge und
Gegeben/wenn/dann als Aufbau, Handlung, Prüfung. Der
[Grundschnitt](../../technik/architektur.md#grundschnitt-der-domäne) spiegelt die Domäne
(345). Die Prüfung beauftragt [367](367-spiegelpruefungInhaltUndDomaene.md), die Ordnung der
Tests [368](368-akzeptanztestsInDerFolgeDerKriterien.md). Hinweis: `auswahlTest.py` hat
19.729 Zeichen; mit AUF-5.5 geht es über das Höchstmaß, dann wird AUF-5 geteilt (T1).
