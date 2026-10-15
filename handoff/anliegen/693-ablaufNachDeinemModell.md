# Ablauf nach deinem Modell: was bremst, Vorbild, fehlende Entscheidung

693 · Fragen · von Organisationsentwickler → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** Dein Modell des Zyklus steht als P1 in der [Retro](../retro.md). Drei Punkte
darin ändern Prämissen; die entscheidest nur du. Sie ersetzen F1 bis F3 aus
[687](687-backlogUndVorbild.md).

**Kosten.** Ohne F1 bremst weiter Feinschliff oder rutscht ein falscher Happy Path durch.
Ohne F2 fehlt dem Fachkritiker der Maßstab. Ohne F3 erfindet eine Rolle still oder wartet.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 1 und Ich 3, Runden höchstens 3, die
Warteregel für Anliegen an eine Perspektive, deren Phase nicht läuft.

**F1 · Wann bremst etwas?**
A: Ich 3 lautet: Kritik ist nie eine Änderung. Der Kritiker ordnet jeden Befund ein, der
Autor darf widersprechen, nach drei Runden entscheidest du.
- Hält das Item auf: Der Happy Path geht aus Sicht des Spielers nicht (Schritt fehlt,
  Sperre greift zu Unrecht oder fehlt), ein Test prüft sein Kriterium nicht, neuer Code
  verletzt Architektur oder Lesbarkeit (das fiele uns später auf die Füße), eine Prüfung
  ist rot.
- Wartet als Anliegen auf die nächste Phase seiner Perspektive: Randfälle, Lücken abseits
  des Happy Path, Namen, Ablage von Hilfsfunktionen.
- Entfällt: Form und Zeichenzahl eines Anliegens, Geschmack ohne Regel.
Kein Backlog je Perspektive (deine Tendenz zu B in 687).
B: Ich 3 wie heute.
Empfehlung: A. Ein Maßstab für alle Rollen statt einer Liste von Fällen.
Antwort: A

**F2 · Für wen sind ArbiterMap und Arbiter-old Vorbild?**
A: Nur für die Domäne (Anforderungsautor, UX, Fachkritiker, Planer), als Satz in
`domaene/CLAUDE.md`: „ArbiterMap und Arbiter-old sind Reflexionsfläche, kein Maßstab: Happy
Paths aus Sicht des Spielers, Bedienung und Aussehen leiten sich von dort ab; eine
Abweichung ist eine Frage an den Stakeholder.“ Technik und Prozess nicht.
B: Nur UX wie heute.
Empfehlung: A, so wie dein Kommentar in 687.
Antwort: A

**F3 · Was tut eine Rolle, wenn ihr eine Entscheidung fehlt?**
A: Hält es den Happy Path auf, fragt sie dich und wartet. Sonst stellt sie die Frage mit
Empfehlung und arbeitet mit der Empfehlung weiter; die Moderation listet diese Annahmen
zuoberst, du siehst sie und kannst umsteuern. Ich 1 bekommt diesen Satz dazu.
B: Sie wartet immer auf dich.
Empfehlung: A. Du siehst, was angenommen wurde, und nichts steht still.
Antwort: A

**Stellungnahme.**
