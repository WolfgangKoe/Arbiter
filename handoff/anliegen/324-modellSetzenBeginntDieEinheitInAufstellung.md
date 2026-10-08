# Setzen des ersten Modells macht die Einheit nicht zur Einheit in Aufstellung

324 · Kritik · von Testautor (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** `Aufstellung.modellSetzen` ([aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py))
liest `_einheitInAufstellung`, setzt es aber nirgends. Das erste `modellSetzen` wirft
`Sperre: nicht in Aufstellung`, AUF-7.1 und AUF-7.2 bis 7.4 sind nicht umgesetzt. Rot sind
dadurch `auf1Test`, `auf7Test`, `que1Test`, `testQue2_4DieKarteZeigtKeinNichtGesetztesModell`
und, zusätzlich zu ihrem eigenen Grund, die Tests in `auf5Test` und `que3Test`, die Modelle setzen.

**Kosten.** Ohne die Behebung bleiben diese Tests aus dem falschen Grund rot und Plan 4 wird nicht grün.

**Gegenvorschlag.** AUF-7 (und AUF-3.7, AUF-3.8) in der Domäne umsetzen, bevor Plan 4 beginnt.

Erledigt, wenn `auf7Test.py` und `que1Test.py` grün sind.

**Stellungnahme.**
Angenommen und umgesetzt: `Aufstellung.modellSetzen` sperrt nach AUF-7.2 (‚nicht wählbar‘) und
AUF-7.3 (‚Einheit begonnen‘) vor der Prüfung der Stelle (AUF-3.8) und macht mit dem ersten
gesetzten Modell die Einheit zur Einheit in Aufstellung (AUF-7.1). Die Tests zu AUF-1, AUF-5,
AUF-7, QUE-1 und QUE-3 sind grün (265 Tests unter `technik/tests`). Offen bleibt nur die
Ausnahme von S4502 in den Prüfungen, siehe [329](329-csrfFuerDieRoutenAusserGet.md).
