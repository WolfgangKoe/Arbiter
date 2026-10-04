# Zählen deine Antworten gegen das Höchstmaß eines Anliegens?

161 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** [145](145-ersteOberflaecheImBrowser.md) hatte mit deinen Antworten 4.063 Zeichen,
`hoechstmassTest.py` war rot und hätte den Commit der Freigabe gesperrt. Der Absender kann
nicht wissen, wie lang du antwortest. Für 145 habe ich den Text des Planers um 150 Zeichen
gekürzt, ohne Aussage zu verlieren (`git diff`); deine Antworten sind unverändert. Die Regel
steht in [`prozess/ablauf.md`](../../prozess/ablauf.md#anliegen): „höchstens 4.000 Zeichen“.

**Kosten.** Ohne Regel wiederholt sich das bei jeder ausführlichen Antwort; dann kürzt jemand
fremden Text unter Zeitdruck, oder du kürzt deine Antwort selbst.

**F1 · Wie zählen deine Antworten?**
- A: Gar nicht. Gezählt wird die Datei, jede Zeile `Antwort:` mit dem Wert `Antwort: .`.
  Der Absender hält 4.000 Zeichen für seinen Text; deine Antworten dürfen beliebig lang sein.
  Nach `beantwortet` arbeitet der Absender sie ein, bis `erledigt` stehen sie in der Datei.
- B: Voll, mit Reserve. Ein Anliegen mit Fragen an dich hat beim Anlegen höchstens 3.500
  Zeichen; die übrigen 500 gehören deinen Antworten. Reicht das nicht, kürzt der Absender.
- C: Voll, wie heute. Läuft eine Datei über, kürzt der Absender, bevor die Freigabe committet
  wird; dafür wird er eigens beauftragt.

Empfehlung: A. Deine Antworten sind die Entscheidung, sie sollen nicht wegen einer Zählung
knapp ausfallen, und niemand muss fremden Text kürzen. B begrenzt dich doch, nur später,
und nimmt jedem Anliegen 500 Zeichen. C kostet je Überlauf einen Rollenlauf vor dem Commit.
Kosten von A: Eine Datei kann über 4.000 Zeichen haben; der Koordinator liest sie dann nicht
(`lesegrenze.py`), er reicht ohnehin nur den Pfad weiter.

Antwort: .

Bei A wird der Satz im Ablauf: „höchstens 4.000 Zeichen; jede Zeile `Antwort:` zählt als
`Antwort: .`“. Den Mechanismus beschreibt [162](162-antwortenNichtZaehlen.md); er gilt nach
deiner Antwort. Bei B oder C passe ich 162 an.
