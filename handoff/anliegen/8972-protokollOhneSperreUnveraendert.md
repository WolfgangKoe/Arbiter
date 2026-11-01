# Bleibt das Protokoll ohne Sperre unverändert?

Form: Kritik
Von: Reviewer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 10

## Runde 1
**Befund.** Der volle Mutationslauf von Zyklus 9 (Ausgabe in
[8970](8970-vollerMutationslauf9AlleMutanten.md)) zeigt einen ungeregelten Fall:
[schlachtrunden.py, Zeile 131](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py#L131),
`if gründe and self._amZug is not None`, `And wird Or`. Mit dem Mutanten schreibt jedes
Loslassen eines *Modells* ohne *Sperre* einen *Eintrag* ohne *Grund* ins *Protokoll*, und alle
Tests bleiben grün. [QUE-5.1](../../domaene/anforderungen/querschnitt/uebergehen.md) sagt nur,
dass ein *gemeinsam übergehen* einen *Eintrag* mehr bringt, QUE-5.3, dass das *Protokoll*
beim Start leer ist. Dass ein Loslassen ohne *Sperre* nichts einträgt, steht nur im Zweck von
QUE-5 („hält jedes Übergehen fest“), in keinem Kriterium; der Testautor hat nichts, wogegen er
prüfen kann.

**Kosten.** Am Bildschirm heute nichts. Im Code: Bricht die Bedingung, füllt sich das
*Protokoll* bei jedem Zug mit leeren *Einträgen*, und kein Test meldet es. Token: ein Kriterium,
ein Test.

**Gegenvorschlag.** Ein Kriterium in QUE-5, etwa: „**Wenn** ein *Spieler* ein *Modell* ohne
*Sperre* loslässt, **dann** hat das *Protokoll* dieselben *Einträge* wie davor.“ Ein Test dazu
fängt den Mutanten.

**Stellungnahme.**
