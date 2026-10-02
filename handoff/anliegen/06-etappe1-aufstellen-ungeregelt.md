# Etappe 1: Aufstellen ohne Ende, ohne Engagement Range, F8 ohne Ort

06 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** Die neue [Etappe 1](../../domaene/etappen/01-aufstellen.md) lässt offen:
1. *Wann ist eine Einheit aufgestellt?* Modelle werden einzeln gesetzt, dazwischen ist die
   Einheit inkohärent; Kohärenz gilt schon beim Aufstellen (`core_rules.txt:434`). Es fehlt
   der Schritt, der sie prüft und an den anderen Spieler übergibt („one at a time“, `:2322`).
2. *Engagement Range beim Aufstellen* fehlt (`core_rules.txt:450`).
3. *F8 hat keinen Ort:* Prüfung beim Loslassen, bei Sperre springt das Modell zurück und der
   Grund steht da. Das steht in keiner Etappe, nur im gelöschten Anliegen 03 (git).
4. [Etappe 2](../../domaene/etappen/02-bewegen.md) verweist fürs Übergehen auf Etappe 1, die nach
   dem Erreichen gelöscht wird; der Verweis läuft dann ins Leere.

**Kosten.** Zu 1: Prüft Arbiter die Kohärenz nach jedem Modell, ist schon das zweite Modell
einer Zehnereinheit gesperrt; das Kriterium ist so unerreichbar, oder die Umsetzung erfindet
den Zeitpunkt. Zu 2: billig, dieselbe Abstandsprüfung wie in Etappe 2; sie deckt das Überdecken
gegnerischer Bases mit ab, F12 betrifft dann nur eigene Modelle. Beispiel Altbestand:
`domain_rules.md` §8 nennt die Regel, `deployment.py` prüft sie nicht und verlässt sich auf
die Lage der Zonen. Mit Übergehen hält das nicht mehr. Zu 3 und 4: Anforderungsautor und
Testautor finden die Entscheidung nicht.

**Gegenvorschlag.**
1. „Aufstellen der Einheit beenden“ prüft die Kohärenz; bei Sperre bleibt die Einheit in
   Aufstellung, sonst ist der andere Spieler dran; wer fertig ist, wird übersprungen (`:2322`).
2. Sperre für ein Modell in Engagement Range eines gegnerischen Modells.
3. F8 als Satz in Etappe 1. Etappe 1 hat 841 von 1.000 Zeichen; reicht der Platz für 1 bis 3
   nicht, kann der Satz „Modelle werden mit Maus und Touch gesetzt“ entfallen, das sagt das Ziel.
4. Das Übergehen wird eine Anforderung in `querschnitt`; beide Etappen verweisen darauf.
