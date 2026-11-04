# Einheit zurücksetzen fehlt im Glossar

Form: Kritik
Von: Testautor
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [BEW-24](../../domaene/anforderungen/phasen/bewegung/einheitZuruecksetzen.md)
nennt die Handlung „Einheit zurücksetzen“. Der
[Vertrag](../../technik/architektur/vertrag/bewegung/grenzkreise.md) und die
[Tests](../../technik/tests/akzeptanz/phasen/bewegung/einheitZuruecksetzenTest.py) nennen
sie `einheitZurücksetzen` (Handlung, Anfrage, Schlüssel im Spielstand) und
`einheitZurücksetzenAngeboten`. Im [Glossar](../../domaene/glossar.md) steht kein Begriff
dazu; nach [Wir 2](../../prozess/praemissen/wir.md) muss ein Begriff aus der Anforderung
dort stehen.

**Kosten.** Der Implementierer übernimmt einen Bezeichner ohne Glossarzeile; der Reviewer
kann Glossar → Code nicht prüfen. Den Happy Path hält es nicht auf, die Tests stehen.

**Gegenvorschlag.** Eine Zeile wie bei *gemeinsam übergehen*:
`Einheit zurücksetzen | – | einheitZurücksetzen | Handlung, mit der bis zum Ende der
*Bewegungsphase* jedes *Modell* einer gezogenen *Einheit* wieder steht, wo es zu Beginn
der *Bewegungsphase* stand (BEW-24.1, 24.2).` Wortlaut nach deinem Urteil.

**Stellungnahme.** Angenommen. Das [Glossar](../../domaene/glossar.md) hat die Zeile
*Einheit zurücksetzen* mit `einheitZurücksetzen`, nach *Einheit in Aufstellung*. Statt
„gezogen“ und „bis zum Ende“ trägt sie die Bedingungen aus BEW-24.1 (*ausgewählte*
*Einheit*, weder *vorgerückt* noch wartend auf den *Vorrückwurf*) und das Ergebnis aus 24.2.
`einheitZurücksetzenAngeboten` ist „angeboten“ aus derselben Zeile, ohne eigenen Begriff.
