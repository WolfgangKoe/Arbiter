# Anhalten vor fremden Bases und Übergehen planen

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md) überdeckt keine *Base*
je eine fremde; Übergehen heißt, eine *Stelle* auf den Stand am Tisch zu korrigieren. Geändert:
- BEW-2 ‚über eine Base‘ samt Zurückspringen ist gestrichen; dafür hält Arbiter in der
  *Bewegungsphase* an und gleitet entlang:
  [BEW-17](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md), Etappe 2 wie
  das gestrichene BEW-2. In BEW-1.5 heißt es nur noch „es sperrt nur QUE-1“.
- [BEW-8](../../domaene/anforderungen/phasen/bewegung/uebergehenBeimZiehen.md): 8.1 und 8.2
  gestrichen, neu 8.3 bis 8.5, übergehen nach BEW-3.1 oder 6.2 (offen in [9270](9270-anhaltenUebergehenUndFormationOhneFreieStelle.md) F1).
- [QUE-1.4](../../domaene/anforderungen/querschnitt/setzen.md): ‚Base überdeckt‘ nie übergehbar.
- [AUF-31](../../domaene/anforderungen/phasen/aufstellen/aufgestellteEinheitKorrigieren.md) und
  AUF-12.9 statt 12.6: *aufgestellte* *Einheit* in der *Aufstellung* korrigieren, ohne Etappe.
- [BEW-18](../../domaene/anforderungen/phasen/bewegung/fliegen.md) *Fliegen*, ohne Etappe: die
  *Datenblätter* nennen bisher kein Schlüsselwort.

**Kosten.** [Etappe 2](../../domaene/etappen/02-bewegen.md) sagt noch „sperrt über fremde Bases“
und „Jede Sperre … gemeinsam übergehen“; AUF-29 (Anhalten in der *Aufstellung*) steht in
Etappe 3. Bis zum Item sperrt Arbiter weiter ‚über eine Base‘ und springt zurück, ohne Test
(Tests fort nach [9272](9272-testsOhneKriteriumNach8840.md)); das kann die DoD der nächsten
Technikphase treffen. Schon jetzt rot: `formregeln.glossar` meldet `Grund.überEineBase` in
`technik/arbiter/domaene/sperre.py`, weil der *Grund* in keiner Anforderung mehr steht. Schätzung aus 8840: etwa ein Item, mit AUF-29 zwei.

**Gegenvorschlag.** Etappe 2 anpassen und ein Item BEW-17, BEW-8, QUE-1.4 in den nächsten Plan,
AUF-29 und AUF-28.2 möglichst mit; AUF-31 und BEW-18 einer Etappe zuordnen. Wann was kommt,
entscheidest du; Etappenzeilen ändere ich auf deinen Wunsch.

**Stellungnahme.**
Angenommen nach F1 B und F2 A:
- [Etappe 2](../../domaene/etappen/02-bewegen.md) und
  [3](../../domaene/etappen/03-angriffUndFallBack.md) angepasst (8880).
- Items in Folge: [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md),
  [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md),
  [fliegen](../../domaene/items/fliegen.md); AUF-31 in
  [randfaelleDesAufstellens](../../domaene/items/randfaelleDesAufstellens.md).
- Wunsch an dich: AUF-29 `Etappe: 2`, AUF-28.2 „(Etappe 2)“, AUF-31 `Etappe: 7`; BEW-18:
  [9340](9340-fliegenDerSpinne.md).

**F1 · Anhalten übergehen (BEW-8.3 bis 8.5): wann?** 8880 F1 A sagte Etappe 3; seitdem fällt
‚über eine Base‘ übergehen fort (8840).
A: Etappe 3 (Anliegen 8880): Bis dahin kein „gemeinsam übergehen“ in der *Bewegungsphase*, der
Knopf aus Zyklus 9 geht und kommt wieder.
B: Etappe 2 (Anliegen 8840, Ihr Kommentar): Knopf und *Protokoll* bleiben, ein Item mehr.
Empfehlung: B, denn sonst korrigiert ihr in Etappe 2 nichts, und der Knopf entsteht zweimal.
Antwort: .

**F2 · Fliegt die Canoptek-Spinne in Etappe 2?** Sie hat FLY (Arbiter-old).
A: Ja (Regeltext, `core_rules.txt:871`): über fremde *Bases* und durch *Nahkampfreichweite*,
nicht darauf enden; ein kleines Item.
B: Erst Etappe 4 (Etappe 4): bis dahin hält Arbiter sie vor fremden *Bases* an, ohne Übergehen.
Empfehlung: A, denn sonst sperrt Arbiter, was die Regel erlaubt.
Antwort: .

Folgen: Mit B und A drei Items mehr in Plan 10, Technik und Token etwa doppelt; Etappe 2 endet
wohl mit Zyklus 11. Bis anhaltenAufDemWeg bleibt `formregeln.glossar` rot.

**Klärung.** Gesetzt, BEW-18 `Etappe: 2`. Neu für anhaltenAufDemWeg: BEW-19 (9420).

**Stellungnahme (Planer).** Umgesetzt mit F1 B, F2 A: BEW-19 im Item anhaltenAufDemWeg; die
drei Items kommen nach 9440 zuerst in Plan 10.
