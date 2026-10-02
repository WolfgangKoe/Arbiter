# Etappe 1: ungeregelte Fälle im Erreicht-Kriterium

02 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen, vom Stakeholder entschieden

## Runde 1
**Befund.** Ohne diese Festlegungen ist das Kriterium nicht prüfbar:
1. *Weg oder Luftlinie?* Die Regel erlaubt jeden Weg, gemessen wird entlang des Wegs
   (`core_rules.txt:729`). Eine Luftlinie verbietet erlaubte Umwege um ein Gegnermodell.
2. *Über andere Modelle* darf keine Base gezogen werden (`core_rules.txt:729`); das fehlt.
3. *Wann ist „am Ende“?* Modelle werden einzeln gezogen, dazwischen darf die Einheit
   inkohärent sein. Es fehlt „Bewegung der Einheit beenden“ und die Folge einer Sperre dort.
4. *Spieler am Zug, einmal je Bewegungsphase* braucht einen Zugwechsel vor Etappe 2 (Frage 2).
5. *Übergehen:* Wie stimmen zwei Spieler an einem Gerät zu, was wird übergangen (eine Sperre
   oder der Zug), was steht im Protokoll? Darf eine Einheit, die danach in Engagement Range
   steht, noch einen Normal Move machen (`core_rules.txt:724`)?

**Kosten.** Altbestand `movement_service.py:269-285`: Die Prüfung wechselte über Sitzungen
zwischen „nur Endpunkt“ und „gerade Strecke“, weil Punkt 1 nie entschieden war; jede Umkehr
traf Fachlogik, Dienst und Oberfläche.

**Gegenvorschlag.**
1. Ein Modell darf während der Bewegung seiner Einheit mehrfach gezogen werden; jeder Zug ist
   eine gerade Teilstrecke, die Summe höchstens M, Engagement Range, Kante und fremde Bases
   gelten je Teilstrecke. Regeltreu für runde Bases und billig.
2. In Etappe 1 aufnehmen; technisch dieselbe Abstandsprüfung wie Engagement Range.
3. „Bewegung der Einheit beenden“ prüft Kohärenz; bei Sperre bleibt die Einheit in Bewegung.
4. Minimaler Zugwechsel: „Bewegungsphase beenden“ übergibt an den anderen Spieler.
5. Entscheidung des Stakeholders, vom Anforderungsautor in Kriterien gefasst.

**Stellungnahme.** Alle fünf angenommen, 1, 3, 5 vom Stakeholder entschieden (F5 bis F7) wie
dein Gegenvorschlag; Übergehen: je Sperre, Bestätigung beider Spieler, Protokoll, danach gelten die
Regeln weiter (`core_rules.txt:724`). Weil Aufstellen jetzt vorn steht (F3 abgelehnt), stehen 1 bis 4
in [Etappe 2](../../domaene/etappen/02-bewegen.md), das Übergehen schon in [Etappe 1](../../domaene/etappen/01-aufstellen.md).
