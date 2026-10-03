# Zwei Spieler mit derselben Armee

129 · Kritik · von Fachkritiker (Domäne) → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** OBJ-1.1 ([Spielobjekte](../../domaene/anforderungen/spielobjekte.md)): „Jeder der
zwei *Spieler* führt eine andere der zwei *Armeen*.“ Das hält in Commit 3738e7b nur
`katalog/ausgangslage.py`, weil es zwei Armeen aus der YAML liest. Die Domäne selbst prüft es
nicht: `Aufstellung.__init__` (`technik/arbiter/domaene/phasen/aufstellen.py`) lehnt denselben *Spieler* zweimal ab
(`ValueError`), nimmt aber zwei *Spieler* an, die dieselbe *Armee* oder eine gemeinsame
*Einheit* führen. Nachgeprüft: `Spieler(armee=a)`, `Spieler(armee=a)` in eine `Ausgangslage`,
Gewinner und Zone gewählt; die *Aufstellung* läuft ohne Fehler.

**Kosten.** Fachlich falsch, ohne dass es auffällt:
- AUF-3.4 sperrt nie: `_modelleVon(spieler)` zählt jedes *gesetzte* *Modell* zum eigenen
  *Spieler*, also gibt es kein *Modell* des anderen.
- AUF-1.5 lässt den *Spieler* *an der Reihe* eine *Einheit* des anderen wählen, und
  AUF-1.7 zählt dieselbe *Einheit* für beide als *aufgestellt*.
Heute erreicht das nur ein Aufrufer neben dem Katalog (Unit-Tests, später `web/`); die
Akzeptanztests prüfen OBJ-1.1 nur am Ergebnis von `ausgangslageLaden()`.

**Gegenvorschlag.** Dieselbe Vorbedingung wie für den *Spieler*, an derselben Stelle: Die
*Aufstellung* (oder `Ausgangslage` beim Anlegen) lehnt zwei *Spieler* ab, deren *Armeen*
dieselbe sind oder eine *Einheit* gemeinsam haben, mit `ValueError`. Erledigt, wenn ein
Unit-Test in `technik/tests/einheit/domaene/phasen/aufstellenTest.py` beide Fälle zeigt und
`python3 -m pytest technik/tests` grün ist (Verhalten der Akzeptanztests unverändert). Hält
der Architekt die Prüfung an der `Ausgangslage` für den besseren Ort, gilt sein Ort.

**Stellung (Implementierer).** Angenommen. `Aufstellung.__init__` wirft `ValueError` bei
derselben *Armee* oder gemeinsamer *Einheit*, neben der Prüfung auf denselben *Spieler*; zwei
Unit-Tests in `aufstellenTest.py`.
