# Akzeptanztests lesen *gesetzt* und *aufgestellt* über die Aufstellung

54 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** Aus [Anliegen 49](49-zustandDerAufstellungInSpielobjekten.md) (Reviewer) folgt
Regel D3 in [`technik/architektur.md`](../../technik/architektur.md): Zustand ändern nur
Handlungen; Spielobjekte sind unveränderlich; was die Aufstellung einführt, hält und zeigt die
`Aufstellung`. [`aufstellenTest.py`](../../technik/tests/akzeptanz/phasen/aufstellenTest.py)
liest es heute am Spielobjekt (`assert erstesModell.gesetzt`, `assert ersteEinheit.aufgestellt`,
sechs Stellen), und [`conftest.py`](../../technik/tests/akzeptanz/conftest.py) baut Einheiten
und Armeen aus Listen. Damit legen die Tests eine Schnittstelle fest, über die jeder
`modell.gesetzt = True` schreiben und so jede *Sperre* umgehen kann.

**Kosten.** Bleiben die Tests, muss der Implementierer den Zustand am Spielobjekt lassen; D3
gälte dann nur auf dem Papier. Die Änderung trifft nur die Prüfzeilen, keine Vorgeschichte.

**Gegenvorschlag.**
1. Lesen über die Abfrage der Phase, nach dem Muster von `aufstellung.aufstellungszone(spieler)`:
   `assert aufstellung.gesetzt(erstesModell)`, `assert not aufstellung.aufgestellt(zweiteEinheit)`.
   Die Bezeichner `gesetzt` und `aufgestellt` bleiben wörtlich.
2. `conftest.py`: Einheiten und Modelle als Tupel (`Einheit(modelle=tuple(…))`,
   `Armee(einheiten=tuple(…))`).
3. `gewinner`, `anDerReihe`, `einheitInAufstellung`, `beendet` bleiben lesbar wie heute;
   kein Test weist ihnen etwas zu.
4. Zusammen mit [Anliegen 48](48-sperrtestsOhneUnveraendertenZustand.md): Die nachgezogenen
   Prüfungen des unveränderten Zustands nutzen gleich die Form aus Nr. 1.

Danach sind die betroffenen Tests rot, bis der Implementierer
[Anliegen 55](55-zustandInDerAufstellung.md) umsetzt.

**Stellungnahme.** Angenommen, alle vier Punkte. `gesetzt(modell)` und `aufgestellt(einheit)`
werden an der `Aufstellung` gelesen, `conftest.py` baut Tupel. Sechs Tests sind rot, bis der
Implementierer [Anliegen 55](55-zustandInDerAufstellung.md) umsetzt. Zu 47: Fremder Spieler und
leere Armee stehen in keinem Kriterium von AUF-1; ohne Kriterium schreibe ich keinen Test.
