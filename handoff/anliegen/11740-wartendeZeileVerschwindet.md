# Zeile eines wartenden Anliegens verschwindet aus dem Fortschritt

Form: Kritik
Von: Planer
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Im [Fortschritt](../plan.md) von Plan 10 standen „Anforderungsautor: Anliegen 10180 …“
(bis `b34f8c8`), „Anforderungsautor: Anliegen 9340 …“ und „Testautor: Anliegen 9401 …“ (bis `HEAD`).
Jetzt fehlen alle drei, keine ist abgehakt. Grund: `betrifft` in
`standregeln/wartendeSchritte.py` bildet die Zeile nur, solange der Kopf `Wartet auf: Technikphase`
trägt. Den Kopf ändern die Rollen aber nach den Regeln:
- [9340](9340-fliegenDerSpinne.md) gab einen Teil weiter und trägt `Wartet auf: 11560`
  ([Status](../../prozess/ablauf/anliegenStatus.md), „bis dahin trägt der Kopf `Wartet auf: <nr>`“).
- [10180](10180-etappe2LueckenNachPlan10.md) und [9401](9401-testZuBew19.md) sind `angenommen`;
  `Wartet auf:` fiel weg, denn es „steht, solange“ es wartet ([Anliegen](../../prozess/ablauf/anliegen.md)).
8261 und 7800 behielten `Wartet auf: Technikphase 10` und sind abgehakt. Ob eine Zeile abgehakt wird
oder verschwindet, hängt also davon ab, ob die Rolle eine Kopfzeile stehen lässt, die nach der Regel
weg muss. Der [Fortschritt](../../prozess/ablauf/fortschritt.md) „wächst mit der Phase“.

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): [Standregeln](../../prozess/regeln/standregeln.md)
Zeile 19 („… ist dort eine Zeile …, mit Haken, sobald es `angenommen` ist“); sie lässt sich anpassen.

**Kosten.** Der Stakeholder sieht nicht, dass 9340 und 10180 zur Technikphase 10 gehören und noch
offen sind; die Phase kann enden, ohne dass sie erledigt sind.

**Gegenvorschlag.** Standregeln Zeile 19 und `wartendeSchritte` ergänzen: Eine Zeile `Anliegen <nr>`,
die schon im Fortschritt der laufenden Phase steht, bleibt, auch wenn `Wartet auf:` danach eine
Nummer nennt oder wegfällt; offen, solange das Anliegen offen ist oder auf eine Nummer wartet,
abgehakt bei `angenommen`, `erledigt` oder gelöschter Datei. „Steht schon“ heißt: in der Datei oder
in ihrer Fassung im Zyklus laut git, sonst kommen die drei nicht zurück. Test dazu neben
`testEinAngenommenesWartendesAnliegenIstAbgehakt`. Dann stehen 9340 offen, 10180 und 9401 abgehakt
wieder da. Rückweg: Commit zurücknehmen. Ohne Probe in `/tmp`.

**Stellungnahme.** Angenommen und umgesetzt: `bleibendeSchritte` in
`standregeln/wartendeSchritte.py` behält jede Zeile `Anliegen <nr>`, die in der Datei oder in einer
Fassung seit der letzten Freigabe (git) steht; offen, bis das Anliegen angenommen, erledigt oder
gelöscht ist. Scheiter-Tests in `standregeln/fortschrittTest.py`, Eintrag in
[Standregeln](../../prozess/regeln/standregeln.md). Die Zeilen zu 9340, 10180 und 9401 kehren
beim nächsten Lauf des Fortschritts zurück.
