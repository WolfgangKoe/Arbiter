# Gleiten in der Bewegung weicht vom Vertrag ab

Form: Kritik
Von: Implementierer
An: Architekt
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** [Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md) sagt, Ziel des
Gleitens seien die *Stellen* nach V16 ab der *Stelle* vor dem Ziehen. Damit schlagen
testBew17_3HältDieBewegungsweiteFrüherAn…, …SpielfeldkanteFrüherAn… und
testBew17_1…SenkrechterTeilÜberDieSpielfeldkante fehl: Sie erwarten die Stelle auf der Strecke
von zuvor zum ungekürzten Ziel. Umgesetzt in `phasen/bewegung/__init__.py`: Gleiten von
zuvor zum ungekürzten Ziel mit den drei Anteilen ab zuvor; hat nichts angehalten (weder
Überdeckung noch `angehaltenAufDemWeg`), gilt V16 ab dem Beginn. Der Vertrag und das
Verhalten stimmen so nicht überein. Ferner: Die Vorlage `protokollGrund` in
`frontend/index.html` ist nicht tot (`protokoll.js` baut jeden *Grund* daraus); nur ihr
Beispieltext „über eine Base“ ist überholt. V15 sagt dazu nichts.

**Kosten.** Der Vertrag lässt Leser ein anderes Verhalten erwarten als der Code liefert.

**Gegenvorschlag.** Ziehen: Ziel des Gleitens ist das ungekürzte Ziel ab zuvor, die drei
Anteile von V16 gelten ab zuvor; V16 ab dem Beginn nur, wenn nichts anhält. Die Vorlage
`protokollGrund` bleibt, der Beispieltext darf ein anderer *Grund* sein.

**Stellungnahme.** Zum Teil angenommen, [Ziehen](../../technik/architektur/vertrag/bewegung/ziehen.md)
berichtigt: Gegleitet wird wie im Code ab zuvor zum ungekürzten Punkt mit den drei Anteilen
ab zuvor, sonst wäre 17.3 für BEW-3.1 und 6.1 leer (die Strecke zu einer *Stelle* nach V16
bleibt im Kreis und im Rechteck). Ob gegleitet wird, entscheidet aber nicht der ungekürzte
Punkt, sondern die *Stellen* nach V16 ab der *Stelle* vor dem Ziehen, bei
`angehaltenAufDemWeg` zudem nach 6.2 ab zuvor (17.4): So fragt 17.1. Am ungekürzten Punkt
geprüft, sperrt QUE-1.2 hinter einer *Base* an der *Bewegungsweite* ohne Übergehen; das ist
Punkt 1 von Anliegen 12700 (Reviewer), dort bitte nach diesem Vertrag umsetzen, nicht mit
dem Halt nach V16 als Ziel des Gleitens. Neue Fälle für die Tests: Anliegen 12682.
`protokollGrund` bleibt; den Beispieltext nimmt Anliegen 12681 mit.
