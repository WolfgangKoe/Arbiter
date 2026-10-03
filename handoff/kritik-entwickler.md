## 1. Konkrete Befunde am Softwareprodukt

- **Die Software ist grundsätzlich brauchbar.** Sie zeigt, dass mit KI auch bei wenig klassischer Software-Engineering-Erfahrung ein funktionierendes Softwareprodukt entstehen kann.
- **Der Code wird ab einem gewissen Detailgrad schwer lesbar.** Auffällig sind unter anderem sehr kurze oder einbuchstabige Variablennamen. Sprechende Namen und klarere Strukturen könnten die Verständlichkeit erhöhen.
- **`if`-/`else`-Kaskaden sind nicht grundsätzlich problematisch.** Kleine Fallunterscheidungen oder frühe `return`s können gut lesbar sein. Bei vielen Verzweigungen kann dagegen Polymorphie sinnvoller werden. Entscheidend ist die Verständlichkeit, nicht die Form.
- **Das Domänenmodell ist teilweise zu implizit.** Fachliche Konzepte, Beziehungen und Verantwortlichkeiten könnten klarer benannt und modelliert werden, bevor sie technisch umgesetzt werden.
- **Die zentrale Steuerung durch `CLAUDE.md` ist zu umfangreich.** Viele Regeln könnten besser über gezielte Skills, Plan Mode oder spezialisierte Subagenten bereitgestellt werden.
- **Qualitätskriterien sind bisher nur teilweise maschinell operationalisiert.** Metriken wie Komplexität, Verschachtelung, Methodenlänge oder Anzahl von Verzweigungen könnten automatisiert erfasst und dem KI-System als Feedback gegeben werden.
- **Hohe Unit-Test-Coverage reicht nicht aus.** Es fehlen stärker fachlich orientierte Akzeptanztests, die komplette User Stories und Domänenverhalten prüfen.

## 2. Daraus abgeleitete Engineering-Prinzipien

- **Abstraktionen sollten nach Verständlichkeit gewählt werden.** Die konkrete Beobachtung zu `if`/`else` und Polymorphie spricht gegen dogmatische Regeln. Clean Code und SOLID sollten als Leitplanken dienen, nicht als Selbstzweck.
- **Architekturentscheidungen lassen sich teilweise messbar machen.** Die beobachteten Code-Strukturen legen nahe, Schwellenwerte oder Heuristiken für Komplexität zu definieren. Ein KI-System könnte dann bei bestimmten Werten prüfen, ob eine andere Struktur verständlicher wäre.
- **Das Domänenmodell sollte der Implementierung vorausgehen.** Wenn Fachbegriffe und Verantwortlichkeiten zuerst explizit gemacht werden, kann die KI auf einer stabileren Grundlage arbeiten und muss weniger aus technischem Kontext erraten.
- **Der Harness sollte Kontext gezielter verteilen.** Die Überlastung von `CLAUDE.md` spricht dafür, Wissen nach Aufgabe und Rolle zu strukturieren: dauerhafte Prinzipien zentral, spezialisiertes Wissen in Skills oder Subagenten.
- **Softwarequalität kann teilweise in Infrastruktur verlagert werden.** Statische Analyse, Tests, Metriken und Agentenregeln können Funktionen übernehmen, die heute stark von individueller Entwicklererfahrung abhängen.
- **Clean Code könnte auch für KI-Systeme einen ökonomischen Nutzen haben.** Klarere Namen und Strukturen kosten lokal möglicherweise mehr Tokens, könnten aber weniger Kontext, weniger Missverständnisse und weniger Korrekturschleifen erfordern. Das ist messbar.
- **Akzeptanztests werden wichtiger, wenn Implementierungsdetails zunehmend von Agenten erzeugt werden.** Je weniger Menschen jeden Codepfad selbst verstehen, desto wichtiger wird die Prüfung des fachlich erwarteten Verhaltens.

## 3. Bestätigte bzw. weiter zu prüfende übergeordnete Hypothesen

- **Das Modell aus Domäne, Prozess und Technik ist tragfähig.** Im Softwareprodukt war erkennbar, dass Annahmen in Domäne und Prozess konkrete Auswirkungen auf den Code haben und technische Entscheidungen wiederum zurückwirken. Das bestätigt die Nützlichkeit einer ganzheitlichen Betrachtung über mehrere Perspektiven und Flughöhen.
- **KI senkt die Eintrittsschwelle für Softwareentwicklung erheblich.** Die brauchbare Software trotz begrenzter klassischer Engineering-Erfahrung stützt diese Hypothese deutlich.
- **Software-Engineering-Kompetenz verschwindet nicht, sondern verlagert sich.** Wenn sie nicht beim einzelnen Entwickler liegt, muss sie in Architektur, Qualitätsmechanismen und Harness-Infrastruktur eingebaut werden. Für den Aufbau dieser Infrastruktur wird wiederum ASE-Kompetenz benötigt.
- **Die Rolle des Entwicklers könnte sich von Implementierung zu Modellierung und Steuerung verschieben.** Das Softwareprodukt deutet darauf hin, dass Domänenverständnis, Prozessgestaltung, Architektur, Constraints und Validierung wichtiger werden können als das manuelle Schreiben jedes Codeabschnitts.
- **Ob Menschen den erzeugten Code künftig vollständig lesen müssen, bleibt offen.** Wenn Agentensysteme dauerhaft verfügbar und zuverlässig genug sind, könnte menschliche Lesbarkeit an Bedeutung verlieren. Die aktuellen Probleme mit schwer lesbarem Code machen diese Frage gerade erst empirisch interessant.
- **Die nächste Untersuchungsfrage lautet nicht mehr primär „Kann KI brauchbare Software erzeugen?“** Interessanter ist nun: **Wie muss Kontext strukturiert werden, damit KI-Agenten zuverlässig, effizient und mit möglichst wenig unnötigem Kontext arbeiten?**
- **Diese Hypothese lässt sich experimentell prüfen.** Varianten von `CLAUDE.md`, Skills, Subagenten, Codestil, Domänenmodell und Kontextumfang können gegeneinander getestet werden. Gemessen werden sollten nicht nur Tokens, sondern auch Erfolgsquote, Fehler, Korrekturschleifen und Zeit bis zu einer akzeptierten Lösung.