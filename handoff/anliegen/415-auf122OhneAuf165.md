# AUF-12.2 zählt AUF-16.5 nicht auf, obwohl AUF-16.5 sich darauf beruft

415 · Kritik · von Fachkritiker (Domäne) → Anforderungsautor (Domäne) · Runde 1/3 · offen

## Runde 1
**Befund.** Bei der Abnahme von Plan 5 stimmt das Gebaute mit AUF-16.5 überein: Lässt jemand
eine *Einheit* auf der *Ablage* des anderen *Spielers* los, springt sie zurück, Arbiter nennt
‚nicht wählbar‘ und bietet *gemeinsam übergehen* nicht an. So hat es der Stakeholder in Anliegen
390 F1 B entschieden („Arbiter nennt den *Grund* bis zur nächsten Handlung (AUF-12.3)“).
AUF-16.5 in [Loslassen ohne Ziel](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md)
beruft sich dafür auf „(AUF-12.2, 12.3 …)“. AUF-12.2 in
[Sperre ohne Stelle](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) zählt
die Fälle aber abschließend auf: „**Wenn** AUF-7.2, 7.3, 8.4, 12.1 oder 16.3 beim Loslassen
sperrt“. AUF-16.5 fehlt. Der Zweck von AUF-12 nennt AUF-7, AUF-8.4 und AUF-9, aber AUF-16 gar
nicht. Wörtlich gelesen gelten also weder „steht danach, wo sie vor dem Ziehen war“ (12.2) noch
„nennt den *Grund* bis zur nächsten Handlung und bietet *gemeinsam übergehen* nicht an“ (12.3)
für eine *Einheit* auf der *Ablage* des Gegners. Das gilt nur über den Umweg „wie AUF-16.3“.

**Kosten.** Gering, nur Text: Code und Tests bleiben. Ohne Änderung widersprechen sich zwei
Kriterien scheinbar. Wer AUF-12.2 liest, hält AUF-16.5 für nicht erfasst. Wer AUF-12 später
ändert, verliert AUF-16.5 leicht aus dem Blick.

**Gegenvorschlag.** In AUF-12.2 „12.1 oder 16.3“ durch „12.1, 16.3 oder 16.5“ ersetzen. Im
Zweck von AUF-12 auch die *Ablage* des anderen *Spielers* ([AUF-16](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md))
nennen. AUF-16.5 bleibt, wie es ist.

**Stellungnahme.**
