# Kriterien zum gesperrten Modell entfallen mit dem Anhalten an Bases

1351 · Kritik · von Fachkritiker → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung: hält die Abnahme des Items auf, nicht die Umsetzung. Nach DoD 3 muss
die Anforderung das gebaute Verhalten beschreiben
([Ablauf](../../prozess/ablauf.md#dod-item-fertig)).
Das [Item](../../domaene/items/anhaltenAnBases.md) streicht AUF-9.1, 9.3, 12.1 und QUE-3.5
samt Test. Ihre Tests löscht der Testautor
([1350](1350-testsEntfallenerKriterienWidersprechenAnhalten.md)). Nach AUF-26.1 und 26.2
entsteht kein *gesperrtes* *Modell* mehr. Trotzdem nennen es noch diese Stellen:
1. [gesperrtesModell.md](../../domaene/anforderungen/phasen/aufstellen/gesperrtesModell.md)
   mit AUF-9.1 und 9.3. Nach dem Löschen bleibt AUF-9 ohne Kriterium.
2. AUF-12.1 in [sperreOhneStelle.md](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md),
   dazu dessen Zweck („solange ein …“).
3. QUE-3.5 in [bedienung.md](../../domaene/anforderungen/querschnitt/bedienung.md).
4. Verweise: AUF-17.1 („Gegeben kein *gesperrtes* *Modell*“) und QUE-2.7 („jedes *gesperrte*
   *Modell*“). Dazu die Zeilen „Am Bildschirm“ in
   [ziehen.md](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) und
   [sperrenBeimSetzen.md](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md)
   („*Sperre*: AUF-9“) und der Zweck von
   [gesperrtesBeenden.md](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md).
5. Im [Glossar](../../domaene/glossar.md): *gesperrt*, *Gesperrtes* und *zurück*, das ein
   *gesperrtes* *Modell* an seine vorige *Stelle* bringt.

**Kosten.** Bleiben die Kriterien stehen, zeigt der Stand sie als „wartet auf den Testautor“
und schickt die falsche Rolle los (wie in 1121). Bei der Abnahme beschreiben AUF-9 und das
Glossar außerdem ein *Modell*, das es nicht mehr gibt.

**Gegenvorschlag.** Sobald 1350 erledigt ist: AUF-9.1, 9.3, 12.1 und QUE-3.5 löschen. Fällt
AUF-9 ganz weg, auch die Datei. Die Verweise aus 4 und die Glossarzeilen aus 5 nachziehen.
*zurück* bleibt für AUF-17.1, ‚keine Kohärenz‘ kommt mit AUF-13 (Plan 7).
Erledigt, wenn `grep -rn "gesperrt" domaene/anforderungen domaene/glossar.md` nur noch
*Sperren* von Handlungen findet, kein *gesperrtes* *Modell*.

**Stellungnahme.** Angenommen, in zwei Schritten, weil der Code das *gesperrte* *Modell*
noch hat, bis Item 3 gebaut ist (V10).
- Jetzt umgesetzt: AUF-9.1, 9.3 und QUE-3.5 gelöscht. Verweise nachgezogen: AUF-17.1
  („Gegeben keine *Sperre* nach AUF-10.3“), QUE-2.7 (nur *gesetzte* *Modelle*), „Am
  Bildschirm“ in [ziehen.md](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) und
  [sperrenBeimSetzen.md](../../domaene/anforderungen/phasen/aufstellen/sperrenBeimSetzen.md)
  (jetzt AUF-26), Zweck von
  [gesperrtesBeenden.md](../../domaene/anforderungen/phasen/aufstellen/gesperrtesBeenden.md)
  und [uebergehen.md](../../domaene/anforderungen/querschnitt/uebergehen.md). Im Glossar
  bringt *zurück* kein *Modell* mehr an seine vorige *Stelle*.
- Bleibt, bis der Implementierer mit V10 `gesperrtesModell.py`, die Klasse `Gesperrtes` und
  `Grund.modellGesperrt` entfernt hat: [gesperrtesModell.md](../../domaene/anforderungen/phasen/aufstellen/gesperrtesModell.md)
  nur mit Überschrift und Zweck, ohne Kriterium (sonst ist `spiegelTest` rot), AUF-12.1 mit
  ‚Modell gesperrt‘ und der Satz dazu im Zweck von AUF-12, die Glossarzeilen *gesperrt* und
  *Gesperrtes* (sonst ist `glossarTest` rot). Rot sperrten beide jeden Commit (Hook).
- Reihenfolge: nach „Implementierer: Tests zu Item anhaltenAnBases grün“, vor „Fachkritiker:
  Item anhaltenAnBases abgenommen“ lösche ich diese Reste; dann gilt dein Erledigt-Satz.
  Bis dahin nennt der Stand AUF-12.1 als „wartet auf den Testautor“.
- Nebenbei gefunden: Was am Bildschirm geschieht, wenn beim Loslassen noch QUE-1.3 sperrt,
  sagt nach AUF-9 kein Kriterium mehr: [1400](1400-nahkampfreichweiteBeimLoslassen.md).
