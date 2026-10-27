# Block im Normal Move sperrt sich an den eigenen Modellen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (Ich 3: eine *Sperre* greift zu Unrecht, Schritt 3 des Happy Path).
Seit der Nachbesserung zu Anliegen 4260 verweist
[BEW-1.1](../../domaene/anforderungen/phasen/bewegung/normalMove.md) nicht mehr auf AUF-21.1.
Damit gilt [AUF-24.2](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md) im
*Normal Move* nicht mehr („Wenn AUF-21.1 oder 21.2 die *Modelle* einer *Einheit* *setzt*,
sperrt QUE-1.2 keines davon wegen eines *Modells* derselben *Einheit*, weder an dessen
voriger noch an dessen neuer *Stelle*“). BEW-1.1 lässt QUE-1 sperren. Zieht man die Boyz als
Block 5″ geradeaus, landet ein *Modell* dort, wo ein anderes der Boyz vor dem Zug stand
(Abstand in der Reihe gut 2″). Wer QUE-1.2 gegen die vorigen *Stellen* prüft, sperrt ‚Base
überdeckt‘. BEW-2.2 klärt das nur für den Weg (fremd nach AUF-29.3), nicht für die neue
*Stelle*. Die Regel verbietet nur, eine *Base* über andere zu ziehen (`core_rules.txt:729`); dass
die *Modelle* der eigenen *Einheit* sich als Block nicht sperren, hat der Stakeholder für
das Aufstellen schon so entschieden (AUF-24.2).

**Kosten.** Ohne Satz entscheidet der Implementierer. Prüft er wie beim *Setzen* einzeln,
lässt sich eine *Einheit* als Block kaum je weiter als ihre eigene Tiefe ziehen. Das wäre
Schritt 3 von Plan 8 mit zehn Boyz. Nachbessern: ein Kriterium.

**Gegenvorschlag.** In [BEW-2](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md),
dort ist Platz (BEW-1 steht bei 1.167 Zeichen): **Wenn** BEW-1.1 die ganze *Einheit* als
*Ebene* *setzt*, **dann** sperrt QUE-1.2 keines ihrer *Modelle* wegen eines *Modells*
derselben *Einheit*, weder an dessen voriger noch an dessen neuer *Stelle* (wie AUF-24.2,
Vorbild `ArbiterMap/…/movement_service.py:450`).

**Stellungnahme.** Angenommen. [BEW-2.4](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md):
„**Gegeben** die *Ebene* ist die ganze *Einheit*, **dann** sperrt QUE-1.2 in BEW-1.1 kein
*Modell* wegen eines anderen derselben *Einheit* an dessen voriger oder neuer *Stelle* (wie
AUF-24.2).“ Kürzer als dein Wortlaut, damit BEW-2 unter 1.200 Zeichen bleibt; das Vorbild
steht in AUF-24.2.
