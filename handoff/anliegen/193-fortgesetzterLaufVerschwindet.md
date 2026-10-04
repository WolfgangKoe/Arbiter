# Lauf-Log: Ein fortgesetzter Lauf verschluckt seine früheren Aufträge

193 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 3/3 · angenommen

## Runde 1
Kritik am Code von Commit d8f68f7. `python3 -m pytest prozess/pruefungen` ist grün (534),
ruff und complexipy auch. Zwei Befunde:

**B1 · Ein fortgesetzter Lauf zählt einmal und trägt den ersten Auftrag.** Der Koordinator
gibt einer laufenden Rolle neue Aufträge (dieser Reviewer-Lauf hat drei bekommen: c11c3b0,
ed9a2c8, d8f68f7). Jeder Auftrag endet mit SubagentStop unter derselben `agent_id`.
`läufeLesen` behält je `agent_id` nur den letzten Eintrag, das war mein Vorschlag aus 189 B2
und ist zu grob: Er trifft nicht nur den geblockten Stopp, sondern auch jeden fortgesetzten
Lauf. Dazu nimmt `zielUndModell` (`laufLog.py`) die erste Nachricht der Rolle. Im echten Log
steht für diesen Lauf deshalb eine einzige Säule mit dem Auftrag „Kritik am Code von Commit
c11c3b0 …“, obwohl die Rolle zuletzt d8f68f7 geprüft hat.
Kosten: Die Tabelle nennt einen falschen Auftrag, und frühere Stände desselben Laufs fehlen
in Säulen, Mittel und Verteilung. Genau das sollte die Spalte Auftrag nach 191 leisten.
Gegenvorschlag: `stop_hook_active` in den Eintrag schreiben. `läufeLesen` verwirft einen
Eintrag nur dann, wenn der nächste derselben `agent_id` `stop_hook_active` trägt. Als Auftrag
die jüngste Nachricht des Koordinators seit dem vorigen Stopp nehmen, nicht die erste. Dazu
ein Test mit zwei Aufträgen im selben Transkript.

**B2 · Der Auftrag bricht mitten im Wort ab.** `zielLänge = 80` schneidet hart ab, im Log
steht „… (Status a“.
Kosten: Der Stakeholder liest einen verstümmelten Auftrag.
Gegenvorschlag: am letzten Leerzeichen vor der Grenze kürzen und „…“ anhängen.

**Stellungnahme.**
B1 und B2 umgesetzt wie vorgeschlagen: `stopp_wiederholt` im Eintrag, Auftrag aus der jüngsten
Nachricht, Kürzen am Wort. Tests `testGeblocktesStoppWirdVerworfenFortgesetzterLaufBleibt`,
`testJüngsterAuftragImTranskriptGiltUndKürztAmWort`. Altlast im Log bleibt.

## Runde 2
Nachprüfung an 83f884b: B2 und das Verwerfen aus B1 erledigt. Offen:

**B3 · Als Auftrag gilt jede Nachricht der Rolle `user`.** Im echten Log steht der erste
Lauf nach dem Commit (Regelumsetzer zu 193) mit dem Auftrag „<system-reminder>“. Im
Transkript sind die Hinweise des Harness (`isMeta: true`) die jüngsten, und das gilt auch
für Skill-Texte. Ein Folgeauftrag beginnt mit „The coordinator sent a message while you were
working:“. `nachrichten` verwirft `isMeta`, der Test kennt nur saubere Nachrichten.
Kosten: Die Spalte Auftrag aus 191 zeigt Rauschen statt des Auftrags.
Gegenvorschlag: Als Auftrag gilt die jüngste Nachricht ohne `isMeta` oder mit dem Vorspann
des Koordinators, und der Vorspann fällt weg. Der Test nimmt Zeilen in der Form des echten
Transkripts.

**B4 · `läufeLesen` wächst quadratisch.** `wiederholtDanach` durchsucht für jeden Eintrag
den Rest des Logs. Das Log wächst ohne Ende und wird bei jedem SubagentStop gelesen; der
Hook hat 10 s.
Gegenvorschlag: ein Durchlauf von hinten, der sich je `agent_id` merkt, ob der spätere
Eintrag wiederholt war.

**Stellungnahme.**
B3 und B4 umgesetzt: `isMeta`, Hinweisblöcke und Vorspann fallen weg; `läufeLesen` läuft einmal
von hinten, auch Ketten wiederholter Stopps geben den Auftrag weiter. Tests
`testHinweiseUndVorspannSindKeinAuftrag`, `testKetteWiederholterStoppsGibtDenAuftragDesErstenWeiter`.

## Runde 3
B4 erledigt. **B5 · Folgeaufträge haben `isMeta: true`** und fallen in `nachrichten` weg; der
Test lässt das Feld weg. `zielUndModell` auf das Transkript dieses Reviewer-Laufs (5 Aufträge)
liefert c11c3b0. Gegenvorschlag: `isMeta` nur verwerfen ohne Vorspann; Test mit `isMeta`.

**Stellungnahme.**
B5 umgesetzt: `isMeta`-Zeilen mit Vorspann bleiben, nur Hinweise fallen weg. Test
`testHinweiseUndVorspannSindKeinAuftrag` trägt `isMeta` am Folgeauftrag.
