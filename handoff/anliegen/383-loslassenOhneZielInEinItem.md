# Loslassen ohne Ziel in ein Item

383 · Kritik · von Anforderungsautor (Domäne) → Planer (Domäne) · Runde 1/3 · angenommen

## Runde 1
**Befund.** Nach den Antworten des Stakeholders in 380 (F1 A, F2 B) gibt es eine neue
Anforderung, [AUF-16 · Loslassen ohne Ziel](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md):
- AUF-16.1: Eine *Einheit*, deren *Modelle* alle *gesetzt* sind, auf der *Karte* losgelassen,
  kommt ohne Meldung an ihren alten Ort zurück.
- AUF-16.2: Dasselbe gilt für alles, was neben *Karte* und *Ablagen* losgelassen wird.
- AUF-16.3: Ein *Modell* der *Einheit in Aufstellung* auf der *Ablage* des anderen *Spielers*
  ist *Sperre* ‚nicht wählbar‘.

Dazu nennt [AUF-12.2](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) jetzt
auch 16.3. Das *Modell* kommt dann wie bei AUF-8.4 an seinen alten Ort zurück, und Arbiter nennt
den *Grund* bis zur nächsten Handlung. Bisher steht AUF-16 in keinem Item.

**Kosten.** Ohne Item entscheidet beim Bau der Implementierer, was in diesen Fällen geschieht,
und kein Test hält es fest.

**Gegenvorschlag.** Ein Item in Plan 5 nimmt AUF-16 auf:
- 16.1 und 16.2 zu [Ziehen](../../domaene/items/ziehen.md);
- 16.3 zu [Gesperrt stehen und zurück](../../domaene/items/gesperrtStehenUndZurueck.md), dort
  stehen schon AUF-8.4 und AUF-12.1 bis 12.3.

Neue Mockups sind nicht nötig: 16.1 und 16.2 zeigen nichts Neues, und für 16.3 genügt die
Meldung aus [auf-12](../../domaene/mockups/auf-12.html) mit dem *Grund* ‚nicht wählbar‘.

**Stellungnahme.** Angenommen wie vorgeschlagen.
[Ziehen](../../domaene/items/ziehen.md) nennt AUF-16.1 und 16.2,
[Gesperrt stehen und zurück](../../domaene/items/gesperrtStehenUndZurueck.md) AUF-16.3 (jetzt
zehn Kriterien). [Plan 5](../plan.md) nennt beides bei den Items, und „Nach Zyklus 5 am
Bildschirm machbar“ sagt: Was ohne Ziel losgelassen wird, springt still zurück; wer in die
*Ablage* des anderen *Spielers* zieht, sieht den *Grund*.
