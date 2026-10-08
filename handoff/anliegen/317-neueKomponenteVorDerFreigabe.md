# Neue Komponente vor der Freigabe des Plans

317 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Die Kennzeichnung `ausgewählt` für AUF-5 ist in
[316](316-kennzeichenAusgewaehlt.md) entschieden, steht aber noch nicht in
`technik/frontend/komponenten.css`. Das schreibt nur der Implementierer, und der arbeitet in
der Technikphase. DoR 5 ([Ablauf](../../prozess/ablauf.md#dor-item-bereit)) verlangt ein
„Mockup aus vorhandenen Komponenten“. Den Weg über `vorschlag.css` nennt die Regel nur für
den Fall, dass es noch keine Komponentenseite gibt. Web, O3
([web.md](../../technik/architektur/web.md)) verbietet neue Klassen in Mockups. Für eine
neue Komponente, wenn die Komponentenseite schon besteht, regelt keins von beiden, wann sie
als vorhanden gilt.

**Kosten.** Bis zur Antwort ist offen, ob AUF-5 DoR 5 erfüllt und Plan 4 zur Freigabe bereit
ist. Die Frage kommt bei jeder neuen Komponente wieder.

**Gegenvorschlag.**

**F1 · Wann gilt eine neue Komponente für DoR 5 als vorhanden?**
- A (Empfehlung): Wenn der Architekt sie im Anliegen entschieden hat und UX die Regeln
  wörtlich in `vorschlag.css` übernommen hat. Der Implementierer trägt sie in der
  Technikphase in `komponenten.css` und `komponenten.html` ein, wie O3 es für den Anfang
  schon vorsieht („gebaut aus `vorschlag.css`“). Kosten: Bis zur Technikphase hat
  `vorschlag.css` zwei Regeln mehr als `komponenten.css`. Danach je eine Zeile in DoR 5
  (Anliegen an den Organisationsentwickler) und in O3 (ich, in der Technikphase), die diesen
  Weg nennen. Diese Regeln ergänzen die beiden bestehenden, statt neue zu schaffen.
- B: Erst wenn sie in `komponenten.css` steht. Der Koordinator startet dafür den
  Implementierer schon vor der Freigabe des Plans; der Ablauf erlaubt das, wenn sonst das
  Inkrement blockiert ist. Kosten: Bei jeder neuen Komponente ein Lauf und ein Commit
  außerhalb der Phase, und die Kritik des Reviewers kommt vor der Freigabe dazu.

Warum A: Die Mockups zeigen schon jetzt dieselben Regeln, die später in `komponenten.css`
stehen. Mit B bekommt der Stakeholder vor der Freigabe also kein anderes Bild zu sehen, nur
mehr Läufe.

Antwort: .

**Stellungnahme.**
