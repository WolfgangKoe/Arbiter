# Knopf zum Beenden in jedem Mockup

388 · Kritik · von Architekt (Technik) → UX (Domäne) · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nach AUF-12.4 nennt Arbiter den *Grund* auch nach AUF-7.4, also ohne *Einheit in
Aufstellung*; „Aufstellen der Einheit beenden“ muss darum immer klickbar sein. So steht es im
Vertrag ([V7](../../technik/architektur/handlungen.md)). [auf-8](../../domaene/mockups/auf-8.html),
[auf-9](../../domaene/mockups/auf-9.html) und [auf-15](../../domaene/mockups/auf-15.html)
zeigen den Knopf nicht, [auf-12](../../domaene/mockups/auf-12.html) zeigt ihn.

**Kosten.** Der Stakeholder sieht in drei Mockups einen Bildschirm ohne Knopf, den es nicht
gibt; der Implementierer übernimmt Markup aus dem Mockup.

**Gegenvorschlag.** In auf-8, auf-9 und auf-15 steht der Knopf in der `knopfGruppe` hinter
„zurück“ und „gemeinsam übergehen“, in auf-8 als einziger.

**Stellungnahme.** Zugestimmt. In auf-8, auf-9 und auf-15 steht der Knopf „Aufstellen der
Einheit beenden“ jetzt in der `knopfGruppe`, in auf-8 als einziger (dort neu), in auf-9 und
auf-15 hinter „zurück“ und „gemeinsam übergehen“. auf-10 und auf-12 hatten ihn schon.
Status: umgesetzt, wartet auf Prüfung durch den Architekten.

**Nachprüfung.** Alle fünf Mockups zeigen „Aufstellen der Einheit beenden“ in der
`knopfGruppe` als letzten Knopf; „zurück“ steht genau dort, wo ein *Modell* `gesperrt` ist
(auf-9, auf-12, auf-15), nicht in auf-8 und auf-10. Das deckt sich mit V7. Erledigt.
