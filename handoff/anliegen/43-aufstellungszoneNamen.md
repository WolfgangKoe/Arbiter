# AUF-1: Die Werte der Aufstellungszone sind nicht benannt

43 · Kritik · von Implementierer (Technik) → Anforderungsautor (Domäne) · Runde 1/3 · angenommen

## Runde 1
**Befund.** AUF-1 und das Glossar kennen zwei *Aufstellungszonen*, aber keine Namen. Die Tests
unterscheiden sie nur durch `list(Aufstellungszone)`. Ich habe `nord` und `süd` gesetzt, ohne
Quelle.

**Kosten.** Erfundene Namen, die später in Karte und Oberfläche wandern.

**Gegenvorschlag.** Die Namen aus der Mission (Deployment Map) im Glossar festlegen, oder
bestätigen, dass `nord`/`süd` vorläufig reichen.

**Stellungnahme.** Befund stimmt: Die Regel nennt keine Namen, die Mission zeigt die Zonen nur
als Bild (`core_rules.txt:2182`, `:2322`); auch `nord`/`süd` als vorläufig zu bestätigen wäre
erfunden. Der Stakeholder hat in [58](58-namenDerAufstellungszonen.md) entschieden: keine
Namen, die Zonen gibt die Mission vor, und Only War benennt sie nicht. Glossar und Kriterien
bleiben ohne Namen. Die Folge für den Code steht in [63](63-zonenOhneErfundeneNamen.md).
