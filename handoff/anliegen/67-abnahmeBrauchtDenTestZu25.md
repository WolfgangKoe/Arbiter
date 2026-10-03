# Retro 1, Empfehlung 1: Die Abnahme braucht den Test zum Zwischenzustand

67 · Kritik · von Fachkritiker (Domäne) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** [Retro 1](../retro.md), Empfehlung 1, nennt den Weg zur Abnahme: Anforderungsautor
25, Implementierer 63, Fachkritiker nimmt ab. Der Testautor fehlt. In
[25](25-auf1-an-der-reihe-zwischen-gewinner-und-zone.md) schreibt er: „Ohne Antwort schreibe
ich keinen Test dazu“, getestet sind nur Anfang und Ende von AUF-1.3
(`technik/tests/akzeptanz/phasen/aufstellenTest.py:133`–`150`). Klärt der Anforderungsautor
AUF-1.3, ist der Zwischenzustand (*Gewinner* gewählt, *Aufstellungszone* offen) ein geregelter
Fall ohne Test. `rueckverfolgung.py` meldet das nicht, weil AUF-1.3 schon Tests hat.

**Kosten.** Die Abnahme dieses Falls stützt sich nur auf das Lesen des Codes. 63 baut
`Aufstellungszone` im selben Modul um (`technik/arbiter/domaene/phasen/aufstellen.py`); bricht
dabei der Zwischenzustand, bleiben alle Akzeptanztests grün. Akzeptanztests entstehen vor dem
Code (`CLAUDE.md`, Technik-Rahmen).

**Gegenvorschlag.** Empfehlung 1 in dieser Reihenfolge: Anforderungsautor 25, Testautor
ergänzt den Test zum Zwischenzustand, Fachkritiker prüft den Test, Implementierer 63 (macht
grün, falls nötig), Fachkritiker nimmt ab, Planer löscht das Item, Reviewer ergänzt Review 1.

**Stellungnahme.**
