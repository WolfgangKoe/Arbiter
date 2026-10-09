# Ein Unit-Test der Domäne lädt Flask über die Handgriffe

342 · Kritik · von Reviewer (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Geprüft: c1416e2. `testEineAufgestellteEinheitAuswählenIstEineVorbedingungsverletzung`
in [aufstellenTest.py](../../technik/tests/einheit/domaene/phasen/aufstellenTest.py) holt
`alleEinheitenAufstellen` aus `tests.akzeptanz.handgriffe`. Die Handgriffe importieren
`tests.akzeptanz.dienst`, der Dienst `arbiter.web.anwendung`. Nachgeprüft: Nach
`import tests.einheit.domaene.phasen.aufstellenTest` stehen `flask` und
`arbiter.web.anwendung` in `sys.modules`. Die übrigen Tests der Datei bauen ihren Zustand
selbst (`spielerMitEinerEinheit`, `aufstellungVon`).

**Kosten.** Der Test der Domäne, die „weder Flask noch die Datenbank“ kennt (CLAUDE.md,
Technik-Rahmen), fällt um, wenn `web/` oder der Dienst der Akzeptanztests nicht importierbar
ist, und hängt an jedem Umbau dort. Der läuft gerade (Anliegen 337, Punkt 1, an den
Testautor). Auch nach 337 bliebe ein Unit-Test an das Gerüst der Akzeptanztests gebunden.

**Gegenvorschlag.** Der Test stellt die *Einheit* mit Handlungen der Domäne selbst auf, wie
die Nachbartests: `gewinnerWählen`, `aufstellungszoneWählen`, für den *Spieler* an der Reihe
`modellSetzen` an einer *Stelle* in seiner *Aufstellungszone*, `aufstellenDerEinheitBeenden`.
Wird das in der Datei mehrfach gebraucht, ein lokaler Helfer neben `aufstellungVon`. Der Import
aus `tests.akzeptanz` entfällt.

Erledigt, wenn `grep -n "tests.akzeptanz" technik/tests/einheit/domaene/` leer ist.

**Stellungnahme.**
Angenommen. Der Test stellt die Einheit mit `modellSetzen` und `aufstellenDerEinheitBeenden` selbst auf; kein Import aus `tests.akzeptanz` mehr.
