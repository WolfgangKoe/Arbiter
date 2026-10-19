# „Aufstellen der Einheit beenden“ fehlt in auf-19 und auf-22

852 · Kritik · von Fachkritiker → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** Unter der *Karte* zeigt [auf-19](../../domaene/mockups/auf-19.html) nur „zurück“
und „gemeinsam übergehen“, [auf-22](../../domaene/mockups/auf-22.html) gar keinen Knopf.
[auf-18](../../domaene/mockups/auf-18.html) bis auf-21 und die gebaute Seite zeigen
„Aufstellen der Einheit beenden“ immer (`technik/frontend/seite.js:266`). Zwei *Sperren*
setzen voraus, dass der Knopf auch in diesen beiden Lagen zu klicken ist:
[AUF-12.1](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) (‚Modell
gesperrt‘, wenn ein *Modell* *gesperrt* steht, wie in auf-19) und
[AUF-7.4](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md) (‚nicht in
Aufstellung‘, wenn es keine *Einheit in Aufstellung* gibt, wie in auf-22).

Einordnung nach Ich 3: hält auf. Baut die Technik nach den Mockups, fehlen zwei *Sperren*,
die ein Kriterium verlangt.

**Kosten.** Ohne den Knopf erreicht der *Spieler* AUF-12.1 und AUF-7.4 am Bildschirm nicht
mehr. Verschwindet der Knopf und erscheint er wieder, springt die *Karte*, genau das soll
[QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) verhindern
([670](670-karteSpringtWennEinGrundErscheint.md)).

**Gegenvorschlag.** In auf-19 und auf-22 steht „Aufstellen der Einheit beenden“ wie in auf-18,
in auf-19 neben „zurück“ und „gemeinsam übergehen“. Soll der Knopf in manchen Lagen fehlen,
ist das eine Frage an den Anforderungsautor. Erledigt, wenn beide Mockups den Knopf zeigen
oder du begründest, warum nicht.

**Stellungnahme.** Stimmt, umgesetzt. [auf-19](../../domaene/mockups/auf-19.html) zeigt „Aufstellen der Einheit beenden“ neben „zurück“ und „gemeinsam übergehen“, [auf-22](../../domaene/mockups/auf-22.html) unter der *Karte* wie auf-18. Der Knopf steht damit in allen fünf Mockups, AUF-12.1 und AUF-7.4 sind am Bildschirm erreichbar und die *Karte* springt nicht (QUE-7.1).

Der Fachkritiker prüft nach.
