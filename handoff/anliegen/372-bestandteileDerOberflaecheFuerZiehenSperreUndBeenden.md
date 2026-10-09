# Neue Bestandteile der Oberfläche für Sperre und Beenden

372 · Fragen · von UX (Domäne) → Architekt (Technik) · Runde 1/3 · offen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde)

## Runde 1
**Befund.** Die Mockups zu AUF-8, AUF-9, AUF-10 und AUF-12
([8](../../domaene/mockups/auf-8.html), [9](../../domaene/mockups/auf-9.html),
[10](../../domaene/mockups/auf-10.html), [12](../../domaene/mockups/auf-12.html)) brauchen
drei Bestandteile, die die [Komponentenseite](../../technik/frontend/komponenten.html) nicht
hat (O3). Mein Vorschlag steht schon in
[vorschlag.css](../../domaene/mockups/vorschlag.css), damit der Stakeholder die Mockups
sieht; er gilt erst mit deiner Entscheidung:
1. `knopf`: Schaltfläche („zurück“, „Aufstellen der Einheit beenden“), `<button>` unter der
   *Karte*.
2. `sperrmeldung` mit `sperrmeldungGrund`: Liste, ein Eintrag je *Grund* (AUF-9.1, AUF-10.4,
   AUF-12.3), unter der *Karte*, `role="alert"`.
3. `modell gesperrt`: Kennzeichen an der *Karte* (AUF-9.1), halbtransparent mit gestricheltem
   Rand in `--akzentHell`; `ausgewählt` bleibt der volle weiße Rand (AUF-5.7).
Dazu eine Änderung an `spalteMitte`: `flex-wrap` und `gap`, damit Meldung und Knöpfe unter
die *Karte* rücken.

**Kosten.** Ohne Entscheidung ist DoR 5 für AUF-9, AUF-10 und AUF-12 nicht erfüllt.

**Gegenvorschlag.** Du wählst andere Namen oder Orte; ich passe Mockups und
`vorschlag.css` an. „gemeinsam übergehen“ fehlt noch (Plan 6).

**Stellungnahme.**
