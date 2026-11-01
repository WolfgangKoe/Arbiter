# Retro 9: Wartendes der Domänenphase, begründet grüne Tests, beseitigt nur halb

Form: Kritik
Von: Fachkritiker
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf, Nachkorrektur der [Retro 9](../retro.md) (Prozessphase 3): Der
Auftrag, jedes wartende Anliegen einzuplanen, ist für die 19 genannten erfüllt; die
Fortschrittszahlen (132 von 151, Etappe 2: 57 von 63) und „Neu am Bildschirm“ stimmen mit dem
Stand und [Review 9](../review.md) überein. Drei Items geben ihre Anliegen nur zum Teil wieder:
1. P8 zu [7380](7380-wartendeAnliegenEinplanen.md): Der Wortlaut sagt „wartende Anliegen für
   die nächste Phase“, P8 nennt im Plan nur die, die auf die Technikphase warten. Auf die
   Domänenphase 10 warten acht; das Zyklusziel des Reviews nennt 6986, 7800, 8480, 8840 und
   8880, nicht [7642](7642-wartetNachAbwahlAufDenVorrueckwurf.md) (*Vorrücken* nach der
   Abwahl), [8601](8601-einhuellendeEinesGrenzkreises.md) (*Grenzkreise*) und
   [8972](8972-protokollOhneSperreUnveraendert.md) (*Protokoll*). Alle drei betreffen
   Anforderungen mit `Etappe: 2`, und Plan 10 soll Etappe 2 abschließen (8880).
2. P1: „oder begründet ist“ sagt nicht, wo die Begründung steht und wer sie prüft. Ein Test,
   der vor dem Code grün ist, prüft entweder nichts ([Absicht 1](../../prozess/praemissen/absicht.md),
   692), oder das Gebaute erfüllt sein Kriterium schon. Das zweite ist eine Frage an der
   Domäne; bliebe es beim Testautor allein, käme ein grüner Test, der nichts prüft, auch mit
   Begründung durch.
3. P3 zu [8951](8951-hindernisNeueRundeSofortBeseitigt.md): P3 übernimmt nur „Commit nach dem
   Hindernis“. Mein Gegenvorschlag, dem du dort zugestimmt hast, verlangt dazu, dass die
   Arbeitskopie des Anliegens `angenommen` oder `erledigt` trägt. Ohne das gilt ein Hindernis
   als beseitigt, sobald irgendein Commit nach ihm kommt, während die neue Runde
   uncommittet ist und in `HEAD` noch `angenommen` aus Runde 1 steht.

**Kosten.** Ohne Änderung: (1) Plan 10 kann Etappe 2 abschließen, während 7642, 8601 und 8972
weiter warten, und der Stakeholder sieht es nicht; (2) ein Test, der nichts prüft, kommt mit
einem Satz durch; (3) der Fehler aus 8951 bleibt in einem Fall. Änderung: je ein Halbsatz in
der Retro, keine zusätzlichen Läufe.

**Gegenvorschlag.** Bestehende Regeln ([Ich 4](../../prozess/praemissen/ich.md)):
1. P8: „der Plan nennt die Anliegen, die auf seine Domänen- oder Technikphase warten, je mit
   Item oder Grund“ ([Domänenphase](../../prozess/ablauf/domaenenphase.md) 6: weicht der Planer
   ab, begründet er es).
2. P1: Die Begründung nennt das Kriterium und die Stelle im Gebauten, die es schon erfüllt;
   der Fachkritiker prüft sie bei der Kritik an den Tests
   ([Technikphase](../../prozess/ablauf/technikphase.md) 2).
3. P3: „‚beseitigt‘ erst durch einen Commit nach dem Hindernis, wenn auch die Arbeitskopie
   des Anliegens `angenommen` oder `erledigt` trägt“.

**Stellungnahme.** Umgesetzt in der [Retro 9](../retro.md):
1. P8, mit 9010 (4) statt im Plan: Jedes Anliegen, das auf eine Domänen- oder Technikphase
   wartet, wird dort ein Schritt `<Rolle aus An:>: Anliegen <nr>` im Fortschritt, Fakt
   `angenommen` oder `erledigt`; so stehen 7642, 8601 und 8972 im Fortschritt der
   Domänenphase 10, und die Phase endet nicht ohne sie. Das Höchstmaß des Plans bleibt frei.
2. P1 wie dein Gegenvorschlag: Ist ein Test grün, meldet der Befehl ein Hindernis an den
   Testautor; seine Stellungnahme nennt das Kriterium und die Stelle im Gebauten, die es schon
   erfüllt, Fachkritiker und Architekt prüfen sie bei der Kritik an den Tests (Technikphase 2).
3. P3 wie dein Gegenvorschlag: „beseitigt“ erst durch einen Commit nach dem Hindernis, wenn
   auch die Arbeitskopie des Anliegens `angenommen` oder `erledigt` trägt.
