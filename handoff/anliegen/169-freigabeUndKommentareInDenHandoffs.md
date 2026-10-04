# Freigabe und Kommentare in Plan, Review und Retro

169 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Dein Wunsch steht im [Ablauf, Freigabe und
Kommentare](../../prozess/ablauf.md#freigabe-und-kommentare). Kurz: Plan, Review und Retro
enden mit `## Freigabe`. Du setzt `Freigabe: ja` und schreibst überall eigene Zeilen
`Kommentar: …`. Der Autor arbeitet jeden Kommentar ein und schreibt `Stellungnahme:` darunter
(Nachkorrektur), auch nach der Freigabe. „.“ im Chat heißt „durchgesehen“; committet wird nur
bei `ja`. Das Review bekommt `## Nächstes Vorgehen` (Produktziel, Etappenziel, Zyklusziel)
und eine eigene Freigabe vor der Retro; Plan n+1 baut auf dem Zyklusziel auf. Retro 2 trägt
`Freigabe: ja` nach `12819fb`; du kannst sie schon jetzt kommentieren. Mechanismen:
[167](167-freigabefeldKommentareImStand.md), [168](168-freigabefeldAendertNurDerStakeholder.md).
Zwei Punkte entscheidet keine Regel.

**Kosten.** Ohne Entscheidung schreibt der Reviewer das Vorgehen (F1 A) und Kommentare gibt es
nur in den drei Dateien (F2 A).

**F1 · Wer schreibt im Review das nächste Vorgehen?**
- A: Der Reviewer, wie jetzt im Ablauf. Vorteil: eine Datei, ein Autor, kein neues Recht;
  deine Kommentare im Review gehen an eine Rolle. Nachteil: Er ist Technik; Produkt- und
  Etappenziel fasst er aus der Abnahme des Fachkritikers und dem Plan zusammen, statt selbst
  fachlich zu urteilen.
- B: Der Planer schreibt den Abschnitt (neuer Schreibpfad `handoff/review.md`). Vorteil: Die
  Rolle, die Etappen und Items schneidet, sagt, wie es weitergeht. Nachteil: zwei Autoren in
  einer Datei, die Schreibgrenze kennt nur Dateien, nicht Abschnitte; Kommentare gehen je
  nach Abschnitt an verschiedene Rollen; ein Lauf mehr je Zyklus.
- C: Der Fachkritiker, gleich nach seiner Abnahme. Vorteil: Er prüft ohnehin gegen Ziel und
  Etappe. Nachteil: wie B, dazu schreibt eine prüfende Rolle Empfehlungen.
Empfehlung: A. Entscheiden tust du mit der Freigabe des Reviews, schneiden tut der Planer im
nächsten Plan; der Abschnitt ist die Vorlage dafür. Korrigieren deine Kommentare das
Vorgehen wiederholt fachlich, ist das der Befund für B.

Antwort: .

**F2 · Wo kommentierst du?**
- A: In Plan, Review und Retro; in Anliegen wie bisher mit `Antwort:`. Zu anderen Dateien
  (Etappe, Anforderung, Architektur) schreibst du den Kommentar in Plan, Review oder Retro
  neben den Link; der Autor macht ein Anliegen an den Besitzer daraus. Vorteil: wenige Orte;
  Formatprüfungen und Höchstmaße der Fachdateien bleiben unberührt. Nachteil: ein Umweg über
  den Autor.
- B: In jeder Markdown-Datei unter `domaene/`, `technik/`, `prozess/`; dran ist der Besitzer
  nach den Schreibpfaden. Vorteil: direkt an der Stelle. Nachteil: Jede Formatprüfung
  (Anforderung, Glossar, Etappe) muss Kommentarzeilen überspringen, der Stand liest alle
  Dateien; mehr Mechanismus bei 52 % Prozesslast ([Retro 2](../retro.md), Befund 2).
Empfehlung: A; B, wenn der Umweg dich wiederholt stört.

Antwort: .
