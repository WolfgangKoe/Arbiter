# AUF-3.6 und AUF-3.7 in Item „Sperren beim Setzen“

104 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Item 2](../../domaene/items/sperren-beim-setzen.md) umfasst AUF-3.1 bis AUF-3.3,
nicht die neuen AUF-3.6 und AUF-3.7 ([Aufstellen](../../domaene/anforderungen/phasen/aufstellen.md),
aus Anliegen 103, git). Beide Fälle entstehen aber genau mit Item 2: Erst dann bekommt
`modellSetzen` eine *Stelle*. Dann muss der Implementierer entscheiden, ob die Stelle geprüft
wird, wenn AUF-1.4 sperrt (AUF-3.6), und was mit einem *gesetzten* *Modell* geschieht, das
noch einmal gesetzt wird (AUF-3.7). Heute nimmt der Code das zweite ohne Prüfung hin; mit
Stelle würde es das Modell ungeprüft versetzen.

**Kosten.** Ohne die beiden im Item baut der Implementierer ein Verhalten ohne Test, oder er
erfindet eins. Mit ihnen: zwei bis drei Akzeptanztests mehr, kaum Code. AUF-3.6 ist die
Reihenfolge der Prüfungen, die Item 2 ohnehin festlegt, AUF-3.7 dieselben Prüfungen ohne die
Bedingung „nicht gesetzt“. Nach D2 bleibt ein gesperrt umgesetztes Modell an seiner alten
Stelle; das deckt die Grenze im Plan schon ab.

**Gegenvorschlag.** Umfang von Item 2: AUF-3.1 bis AUF-3.3, AUF-3.6 und AUF-3.7. Die
AUF-3.4-Teile bleiben bei `nahkampfreichweite-beim-setzen`.

**Stellungnahme.** Angenommen. Item 2 umfasst AUF-3.6 und AUF-3.7, aber nicht den Teil zu
AUF-3.4; diesen trägt `nahkampfreichweite-beim-setzen`. Im Plan sind die Grenzen angepasst:
Umsetzen von der vorigen Stelle gehört jetzt zu Item 2. Ein gesperrtes Modell bleibt ungesetzt
oder an seiner vorigen Stelle.
