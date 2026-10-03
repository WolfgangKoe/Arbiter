# Ausgangslage.tiefen ist ein veränderliches dict in einem frozen Spielobjekt

136 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · offen

## Runde 1
Gegenstand: 6566da4 (Kritik am Code), `Ausgangslage.tiefen` in
`technik/arbiter/domaene/phasen/aufstellen.py`. Den Typ `dict` hatte ich in 130
vorgeschlagen; der Fehler liegt also bei mir, nicht bei der Umsetzung.

**Befund.** `Ausgangslage` ist `frozen`, aber `tiefen: dict[Aufstellungszone, Fraction]`
lässt sich von außen ändern: `ausgangslage.tiefen[Aufstellungszone.erste] = Fraction(30)`
läuft ohne Fehler durch. Danach misst `_grenzenInX` die Zone mit 30″, ohne Handlung, ohne
Sperre und ohne Protokoll. D3 (`technik/architektur.md`) verlangt unveränderliche
Sammlungen. Ich habe D3 um `MappingProxyType` ergänzt, das unveränderliche `dict` der
Standardbibliothek.

**Kosten.** Heute gering, weil nur der Katalog und die Tests eine Ausgangslage bauen. Mit
`web/` liest auch eine Anfrage die Ausgangslage, und dann ist der Fehler still. Ein Tupel
wie bei `Armee.einheiten` schützt dort; hier fehlt dieser Schutz.

**Gegenvorschlag.**
- In `Ausgangslage`: `tiefen: Mapping[Aufstellungszone, Fraction]` (`collections.abc`).
- Im Katalog: `tiefen=MappingProxyType(tiefen)` (`types`).
- Ein Einheitstest in `tests/einheit/katalog/ausgangslageTest.py`: die Zuweisung an
  `ausgangslageLaden().tiefen[zone]` wirft `TypeError`.

**Erledigt, wenn:** der Test grün ist, `tiefen` als `Mapping` annotiert ist und die
Akzeptanztests unverändert grün sind.
