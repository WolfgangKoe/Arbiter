# Bildschirmtests: Name der Einheit und Lesbarkeit

248 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von c007cfc (Schnittstelle und Lesbarkeit,
`prozess/praemissen/wir.md`), zu [245](245-schnittstelleDerBildschirmtests.md):
1. `Einheit` bekommt das Pflichtfeld `name` (Glossar „Name“: jede *Einheit* hat einen;
   [Web](../../technik/architektur/web.md) W2). `_spielerMit` in `conftest.py` baut
   `Einheit(modelle=…)` ohne Namen; damit werden AUF-1 bis AUF-3 rot, sobald der
   Implementierer das Feld anlegt, und er darf den Test nicht ändern.
2. `len(Aufstellungszone)` steht für etwas anderes: in AUF-4.4
   (`SolangeKeinerAnDerReihe…`) für die Zahl der *Spieler*, in AUF-4.3
   (`ZeigtKeineAufgestellteEinheit`) für die Zahl der *Einheiten* von Spieler 2. Stimmt
   heute zufällig (2), der Leser muss es entschlüsseln.
3. `einheitenAufstellen(ausgangsaufstellung, 4)` in `aufstellungOhneJemandAnDerReihe`: die
   4 heißt „alle *Einheiten* beider *Armeen*“.
4. `testAuf4_5MitDerGewähltenAndererEinheitWandertDieKennzeichnung`: Satz ungrammatisch.
5. AUF-4.6 (`NachDerWahl…`): `ausgangsaufstellung = gewählteAufstellung` benennt einen
   Zustand nach der Wahl als Ausgangsaufstellung.
6. QUE-2.5 (`DieTiefeDerAufstellungszonen…`): `zone, _ = …` nimmt die erste Zone nach der
   Reihenfolge im DOM und vergleicht sie mit `tiefen[erste]`; das ist Struktur (B2). AUF-4.6
   findet die Zone richtig über ihr `x`.
7. `seiteZu`: Das `# Warum` des Imports im Fixture gilt nur, solange `web/server.py` fehlt;
   danach ist es falsch.

**Kosten.** 1 blockiert den Implementierer bei AUF-4.3 (Name in der *Ablage*), eine Zeile.
2 bis 6 je eine Zeile; ohne sie liest man Zahlen und Namen, die nicht sagen, was sie meinen.
7: eine Zeile nach dem Implementierer.

**Gegenvorschlag.**
1. Vor dem Implementierer: `_spielerMit` gibt jeder *Einheit* einen Namen, etwa
   `Einheit(name=f"Einheit {nummer}", modelle=…)`; ebenso jede andere `Einheit(…)` unter
   `tests/akzeptanz/`. Die Einheitstests passt der Implementierer an.
2. AUF-4.4: die Namen prüfen (`{"Spieler 1", "Spieler 2"}` im Text der `.kopfzeileSpieler`)
   statt zu zählen; AUF-4.3: `len(spielerZwei.armee.einheiten)`.
3. Benannte Summe der *Einheiten* beider *Armeen* aus `spielerEins` und `spielerZwei`.
4. `testAuf4_5MitDerWahlEinerAnderenEinheitWandertDieKennzeichnung`.
5. `aufstellung = gewählteAufstellung` oder den Parameter direkt nutzen.
6. Die Zone bei `x == 0` wählen, wie AUF-4.6.
7. Nach dem Lauf des Implementierers: Import nach oben, Kommentar weg.

Erledigt, wenn 1 bis 6 umgesetzt sind und AUF-1 bis AUF-3 grün bleiben; 7 nach dem
Implementierer.

**Stellungnahme.** Angenommen, 1 bis 6 umgesetzt:
1. `_spielerMit` vergibt `Einheit {nummer}`; andere `Einheit(…)` gibt es unter
   `tests/akzeptanz/` nicht.
2. AUF-4.4 prüft „Spieler 1“ und „Spieler 2“ im Text der `.kopfzeileSpieler`; AUF-4.3 zählt
   `len(spielerZwei.armee.einheiten)`.
3. `alleEinheiten` als Summe der *Einheiten* beider *Armeen*.
4. Name lautet jetzt `…MitDerWahlEinerAnderenEinheitWandert…`.
5. AUF-4.6 nutzt `gewählteAufstellung` direkt.
6. QUE-2.5 wählt die Zone bei `x == 0`.
7. Den Kommentar zum Import in `seiteZu` habe ich schon gestrichen; den Import nach oben
   setzt der Implementierer, sobald `web/` besteht.
Lauf: rot wegen `Einheit(name=…)` und fehlendem `arbiter.web`, beides fehlender Code.
