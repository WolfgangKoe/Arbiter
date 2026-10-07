# Anliegen: Formen, Züge, wartet auf und Legende

274 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 254 (Runde 2) entschieden; die Regel steht in
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen). `anliegenregeln/anliegen.py` und
`statusrecht.py` kennen noch die alte Fassung:
1. `typWerte` hat `Anliegen` statt `Auftrag`; Anliegen 246 trägt noch `Anliegen`.
2. `statusWerte` hat `beantwortet`, aber nicht `rückfrage`; `beantwortetDurchFreigabe` macht
   nach einer Freigabe den Absender zuständig, der Stakeholder setzt den Status jetzt selbst.
3. Die Kopfzeile endet am Status; `· wartet auf <nr>` (auch mehrere, durch Komma) bricht sie.
4. Die Legende unter dem Kopf prüft niemand.

**Kosten.** Setzt der Stakeholder `rückfrage` oder eine Rolle `wartet auf` in den Kopf, ist
der Lauf der Prüfungen rot; der Stand nennt nach jeder Freigabe den falschen Zuständigen.

**Gegenvorschlag.** Erledigt, wenn, je mit Scheiter-Test:
1. Formen `Kritik`, `Fragen`, `Auftrag`; `Anliegen` ist rot. Den Kopf von 246 stellst du um.
2. Status nach der Tabelle im Ablauf: `rückfrage` setzt nur der Empfänger, danach ist der
   Absender dran; von `rückfrage` auf `offen` nur der Absender, ohne neue Runde. `beantwortet`
   ist rot, `beantwortetDurchFreigabe` und sein Eintrag in `prozess/regeln.md` entfallen.
3. Der Kopf darf `· wartet auf <nr>[, <nr>]` tragen; jede Nummer muss als Datei bestehen.
   Der Stand zeigt solche Anliegen als wartend, nicht beim Empfänger als dran.
4. Ist der Stakeholder Absender oder Empfänger, steht in Zeile 5 die Legende wörtlich aus dem
   Ablauf (eine Konstante); fehlt sie, ist es rot. In bestehende Anliegen fügst du sie ein.
Danach ersetze ich „nur Text, bis Anliegen 274“ im Ablauf.

**Stellungnahme.**

Stellungnahme: Entfällt mit dem Rückbau.
