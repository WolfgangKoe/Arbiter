# Itemtext nennt AUF-5.5 und verlangt damit einen Test

323 · Kritik · von Testautor (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.** [Auswählen in der Ablage](../../domaene/items/auswaehlenInDerAblage.md) schreibt
„AUF-5.5 erst ab drei *Einheiten* je *Armee* (320 B)“. `kriterienregeln/rueckverfolgung.py`
liest jede Nennung der Kennung als Umfang und meldet `auf5Test.py: AUF-5.5 hat keinen Test`
(`testDasRepoHältDieRückverfolgung` rot). Ein Test ist nicht möglich: Jede *Armee* hat zwei
*Einheiten*, eine dritte *Einheit* gibt es nicht ([Plan 4](../plan.md), Anliegen 320 B).

**Kosten.** Solange der Text die Kennung nennt, bleibt die Prüfung rot, auch wenn Plan und
Tests stimmen. Die Änderung ist eine Zeile.

**Gegenvorschlag.** Die Kennung aus dem Itemtext nehmen („die Verdrängung einer dritten
*Einheit* erst ab drei *Einheiten* je *Armee*“); die Planzeile „AUF-5.5 … nicht im Umfang“
nennt sie ebenfalls und ist von der Prüfung nicht erfasst, solange kein Item sie nennt.

Erledigt, wenn `python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung`
AUF-5.5 nicht mehr meldet.

**Stellungnahme.** Angenommen. [Auswählen in der Ablage](../../domaene/items/auswaehlenInDerAblage.md)
nennt die Kennung nicht mehr, sondern „ohne dritte *ausgewählte* *Einheit* (320 B)“; der
Umfang ist unverändert. `python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung`
meldet nichts mehr. Die Planzeile zu AUF-5.5 bleibt: Plan 4 ist freigegeben, die Prüfung liest
nur Itemtexte.
