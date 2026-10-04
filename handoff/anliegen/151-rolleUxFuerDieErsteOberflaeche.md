# Rolle UX für die erste Oberfläche

151 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Plan 3 bringt voraussichtlich das erste Item mit Oberfläche
([145](145-ersteOberflaecheImBrowser.md), F2). Das ist der Auslöser der Rolle UX
([Ablauf, Rollen mit Auslöser](../../prozess/ablauf.md#rollen-mit-auslöser)), und DoR 5
verlangt bei einer Oberfläche ein Mockup, bevor das Item bereit ist. Heute schreibt niemand
Mockups.

**Kosten.** Ohne die Rolle ist Plan 3 nicht bereit, oder das Item geht ohne Mockup in die
Technikphase: Dann entscheidet der Implementierer über Aufbau und Aussehen, und du siehst es
erst gebaut.

**Gegenvorschlag.** Rolle `ux`, Perspektive Domäne, ausführend, Modell sonnet:
- Je Anforderung mit Oberfläche ein Mockup: statisches HTML mit dem echten CSS, ohne
  JS-Logik, nur Inhalte aus Kriterien oder Katalogdaten; gelöscht nach dem Einbau.
- Nur Komponenten der Komponentenseite ([Architektur, Oberfläche](../../technik/architektur.md));
  eine neue Komponente ist ein Anliegen an die Technik. Für die erste Oberfläche gibt es
  noch keine; wie das erste Mockup zu seinem CSS kommt, regelt
  [DoR 5](../../prozess/ablauf.md#dor-item-bereit).
- ArbiterMap ist Vorbild für das Bild, nicht Vorlage für Code (145, F1).
- Schreibpfade: `domaene/mockups/` und `handoff/anliegen/`.
- Im Ablauf: Domänenphase zwischen Anforderungen (4) und Plan (5); du siehst das Mockup vor
  der Freigabe des Plans. Kritik: Fachkritiker (Mockup gegen Kriterien), Architekt
  (nur vorhandene Komponenten).
Nach deiner Antwort schreibe ich die Definition und den Ablauf, der Koordinator bekommt die
Rolle in seine Liste.

**F1 · Rolle UX einsetzen?**
- A: Ja, wie oben, sobald 145 F2 mit A beantwortet ist.
- B: Nein, das Mockup schreibt der Anforderungsautor.
Empfehlung: A. Gestaltung ist eine eigene Sicht; der Anforderungsautor schreibt Kriterien,
kein HTML.

Antwort: .
