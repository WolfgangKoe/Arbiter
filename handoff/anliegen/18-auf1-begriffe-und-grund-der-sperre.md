# AUF-1: fehlende Begriffe und der Grund der Sperre

18 · Kritik · von Architekt (Technik) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.**
1. Drei Begriffe tragen den Zustand von [AUF-1](../../domaene/anforderungen/phasen/aufstellen.md),
   stehen aber weder kursiv noch im [Glossar](../../domaene/glossar.md): an der Reihe (1.2,
   1.3, 1.5 bis 1.7), setzen eines *Modells* (1.4), aufgestellt (1.5 bis 1.7). Es fehlt auch
   die Stelle, an die gesetzt wird; der [Plan](../plan.md) nennt sie schon.
2. AUF-1.4 sagt „folgt eine *Sperre*“, nennt aber keinen Grund, obwohl das Glossar einen
   verlangt.

**Kosten.** Ohne Glossarzeile erfindet der Implementierer Bezeichner (`aktiver_spieler`,
`am_zug`, `platziere`, `position`), und die Prüfung Glossar ↔ Code greift nicht, weil die
Wörter nicht kursiv stehen. Ohne benannten Grund prüft der Test entweder einen Text (bricht bei
jeder Umformulierung) oder nur „gesperrt“ (eine Sperre aus falschem Grund bleibt grün, sobald
Zone und Kohärenz eigene Sperren bringen).
Beispiel aus dem Altbestand: `ArbiterMap/backend/app/domain/rule_checks.py` liefert Befunde als
eigene Typen (`CoherencyViolation`, `EngagementRangeContact`), nicht als Text. Der Test fragt
den Typ ab, die Oberfläche formuliert den Satz für die Spieler.

**Gegenvorschlag.**
1. Glossarzeilen für an der Reihe, setzen, aufgestellt und Stelle, in AUF-1 kursiv. Ob
   „Stelle“ oder „Position“, wählst du; wichtig ist ein Wort für alle Dateien.
2. Jedes Kriterium mit *Sperre* nennt ihren Grund mit einem kurzen Namen, etwa AUF-1.4:
   „… eine *Sperre* mit dem Grund ‚nicht in Aufstellung‘“. Der Test prüft den Grund, den
   Wortlaut für die Spieler legt er nicht fest.

**Stellungnahme.**
Angenommen, umgesetzt in [AUF-1](../../domaene/anforderungen/phasen/aufstellen.md) und im
[Glossar](../../domaene/glossar.md).
1. Neue Zeilen *an der Reihe*, *aufgestellt*, *setzen* (gesetzt), *Stelle*, dazu *Gewinner*
   und *Grund*. „Stelle“ wie in Etappe 1 und Plan; AUF-1 prüft sie nicht, sie steht nur in der
   Definition von *setzen*. Freigabe beim Stakeholder in [21](21-auf1-neue-begriffe.md).
2. Jede *Sperre* nennt ihren *Grund*: ‚nicht wählbar‘ (1.2, 1.5), ‚Einheit begonnen‘ (1.6),
   ‚nicht in Aufstellung‘ (1.4). Der Test prüft den Namen, nicht den Satz für die Spieler.
