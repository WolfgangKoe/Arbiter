# AUF-1: Wer ist an der Reihe, wenn der Gewinner gewählt ist, die Aufstellungszone nicht

25 · Kritik · von Testautor (Technik) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** [AUF-1.3](../../domaene/anforderungen/phasen/aufstellen.md) sagt „Vor dieser
Wahl ist keiner *an der Reihe*, danach, wer nicht *Gewinner* ist“. AUF-1.2 trennt die Wahl in
zwei Schritte. Ob „Wahl“ den *Gewinner*, die *Aufstellungszone* oder beide meint, steht nicht
da; im Zwischenzustand (*Gewinner* gewählt, Zone offen) ist der Fall ungeregelt.

**Kosten.** Ohne Antwort schreibe ich keinen Test dazu; der Implementierer wählt frei, und die
Wahl ist später nicht mehr von einer Regel zu trennen.

**Gegenvorschlag.** AUF-1.3: „Bis die *Aufstellungszone* gewählt ist, ist keiner *an der
Reihe*, danach, wer nicht *Gewinner* ist.“ Getestet sind bisher nur Anfang und Ende.

**Stellungnahme.** Angenommen. AUF-1.3 lautet jetzt „Bis zur Wahl der *Aufstellungszone* ist
keiner *an der Reihe*, danach, wer nicht *Gewinner* ist.“ Inhaltlich dein Vorschlag, kürzer
gefasst wegen des Höchstmaßes; aus demselben Grund steht in AUF-1.7 „hat er alle *aufgestellt*“
ohne „*Einheiten*“, mit gleicher Bedeutung. Die Regel trägt das: Abwechselnd aufgestellt wird
erst, nachdem der *Gewinner* die Zone gewählt hat, beginnend mit dem, der nicht gewählt hat
(`core_rules.txt:2322`). Die Kennung bleibt AUF-1.3: Die bestehenden Tests zu Anfang und Ende
gelten unverändert, neu geregelt ist nur der Zwischenzustand.
