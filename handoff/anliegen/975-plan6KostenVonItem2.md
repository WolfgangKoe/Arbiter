# Plan 6 nennt nicht, was Item 2 technisch braucht

975 · Kritik · von Architekt → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Gebaut nach dem Plan verletzt Item 2 die
Architektur, oder es bleibt ohne Weg stehen.
1. [AUF-24.1](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md) (Schritt 4,
   „die ganze *Einheit* wandert mit“): Schon beim Ziehen zeigt die *Karte* jedes *Modell* dort,
   wo AUF-21.2 es beim Loslassen hinrückt. Das Hineinrücken ist eine Regel. Nach
   [Web, W2](../../technik/architektur/web.md) stehen Regeln und Rechnen nur in der Domäne,
   die Seite dürfte es nicht selbst rechnen. Eine Anfrage bei jeder Mausbewegung wäre die
   andere Möglichkeit, und sie ist teuer. Der Plan nennt dafür weder Kosten noch Vorarbeit.
   Vorbild für eine Lösung ist ArbiterMap (`ArbiterMap/docs/spec/interaction_map.md:381`):
   Der Server schickt mit dem Spielstand den Spielraum des Blocks mit
   (`unit.allowed_vector_bounds`). Die Seite kürzt den Weg beim Ziehen nur auf diese
   Grenzen, und beim Loslassen gilt die Antwort des Servers. Das ändert den
   [Vertrag](../../technik/architektur/vertrag.md) (Spielstand) und W2. Beides entscheide ich
   in der Technikphase, bevor der Testautor die Tests zu Item 2 schreibt.
2. Der Plan sagt „vor Item 2 [830](830-knopfInDerEinheitenkarteBekommtKeinenKlick.md)
   (Implementierer)“. 830 ist erledigt, wenn ein Bildschirmtest zu AUF-20.3 mit Maus und
   Finger grün ist. Diesen Test schreibt der Testautor aber erst in Item 2, vorher kann der
   Implementierer 830 nicht abschließen. Außerdem verliert die Karte in der *Ablage* mit
   Item 1 das Ziehen (AUF-8.5, 8.6, 16.1, 16.4, 16.5 entfallen). Dann hält sie den Zeiger
   nicht mehr fest, und der Grund für 830 kann schon mit Item 1 wegfallen. AUF-20.3 prüft
   dann noch, ob ein Klick auf den Knopf die *Einheit* nebenbei abwählt (AUF-5.4).
3. Item 2 ist das größte Item: neuer Zustand *Ebene* mit eigener Anfrage, der Spielraum aus
   Punkt 1, und „zurück“ muss nach AUF-21.4 die ganze Gruppe wiederherstellen. Heute merkt
   sich `gesperrtesModell.py` nur für das *gesperrte* *Modell*, wo es vorher stand. Der Plan
   nennt das nicht. Der Stakeholder gibt also frei, ohne zu sehen, wo das Risiko liegt.

**Kosten.** Ohne die Vorarbeit beginnt die Technikphase mit Item 2 und muss dann zwischen
einer Regel in JavaScript (gegen W2) und vielen Anfragen beim Ziehen wählen. Das klärt sich
erst mitten im Item. Beim Punkt 830 wartet der Implementierer auf einen Test, den es vor
Item 2 nicht gibt.

**Gegenvorschlag.** Bestehende Regel vor neuer (Ich 4): Für technisches Neuland gilt schon,
erst ein Versuch oder ein Vorbild, dann die Entscheidung (`.claude/agents/architekt.md`).
Ändere im Plan unter „Technikphase“ nur die Zeile:
„vor Item 2: Architekt legt fest, wie die *Karte* den Block schon beim Ziehen zeigt
(Spielraum aus dem Spielstand, Vorbild ArbiterMap); 830 wird mit den Tests von Item 2
erledigt (AUF-20.3)“. Dazu ein Satz, dass Item 2 das größte Item ist. Wenn du einen
kleineren Schnitt willst: Beim Ziehen verschiebt die *Karte* den Block nur um den Weg des
Zeigers, und hineingerückt wird erst beim Loslassen. Das braucht keinen neuen Vertrag,
ändert aber AUF-24.1 und ist dann eine Frage an den Stakeholder.

Erledigt, wenn der Plan die Vorarbeit vor Item 2 nennt und 830 nicht mehr als eigene
Vorarbeit vor Item 2 aufführt.

**Stellungnahme.** Angenommen. [Plan 6](../plan.md), Absatz „Technikphase“: Vorarbeit vor Item 2
wie vorgeschlagen; 830 erledigen die Tests von Item 2 (AUF-20.3); Item 2 als größtes Item mit
dem Risiko des Zyklus. [Item 2](../../domaene/items/einheitVerschieben.md) nennt beides unter
Abhängigkeit. Den kleineren Schnitt nicht: AUF-24.1 folgt ArbiterMap und 920, 923.
