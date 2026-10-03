# Aufstellungszonen ohne erfundene Namen

63 · Kritik · von Anforderungsautor (Domäne) → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** `Aufstellungszone` in
[`aufstellen.py`](../../technik/arbiter/domaene/phasen/aufstellen.py) hat die Werte `nord` und
`süd`. Der Stakeholder hat in [58](58-namenDerAufstellungszonen.md) entschieden: Konkrete Namen
sind regeltechnisch falsch, die Zonen gibt die Mission vor. Only War nennt ihre zwei Zonen
nicht (`core_rules.txt:2322`); ein Name steht deshalb weder im Glossar noch in einem
Kriterium.

**Kosten.** Die erfundenen Namen wandern sonst in Karte, Protokoll und Oberfläche, und ein
späteres Missionsmodell muss sie wieder herauslösen.

**Gegenvorschlag.** Die zwei Zonen ohne fachlichen Namen führen; wie, entscheidest du mit dem
Architekten. Fachlich nötig ist nur: Es gibt zwei, sie sind unterscheidbar, eine gehört dem
*Gewinner*, die andere dem anderen *Spieler* (AUF-1.1). Die Akzeptanztests greifen schon nur
über `list(Aufstellungszone)` zu; bleibt dieser Zugriff, hat der Testautor nichts zu tun. Ob
Mission und Aufstellungskarte Begriffe werden, ist F2 in 58 und noch offen; darauf muss diese
Änderung nicht warten.

**Stellungnahme.**
