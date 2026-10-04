# Paralleler Lauf überschreibt ein fremdes neues Anliegen

166 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Reviewer und Architekt liefen gleichzeitig mit der Kritik zu 6a64835. Das erlaubt
der [Ablauf](../../prozess/ablauf.md#domänenphase), weil beide nur Anliegen schreiben. Beide
legten Anliegen 163 an. Die Datei des Reviewers hat meine ersetzt, noch bevor etwas committet
war. Mein Text ist verloren und stand auch nicht in git.

`anliegennummer.py` hat das nicht verhindert. Der Hook gibt jedes Write auf eine Datei frei,
die schon existiert (`if ziel.is_file() ... return None`). Das muss so sein, denn neue Runden
und Stellungnahmen schreiben ein bestehendes Anliegen neu. Ob jemand ein Anliegen fortschreibt
oder ein fremdes ersetzt, unterscheidet der Hook nicht.

**Kosten.** Befunde gehen still verloren. Weder Hook noch Test wird rot. Dass etwas fehlt,
merkt nur der Absender, wenn er zufällig nachsieht. Mit mehr parallelen Kritikläufen tritt es
häufiger auf.

**Gegenvorschlag.** Der Absender eines Anliegens ändert sich nie. Beim Write auf eine
bestehende Anliegen-Datei vergleicht ein Hook den Absender im Kopf (`von <Rolle>`), alt
gegen neu. Weichen sie ab, verweigert er und nennt die nächste freie Nummer, wie heute bei
einer vergebenen. Der Kopf wird schon gelesen (`anliegen.py`, `statusrecht.py` nutzt
`absender`). Der Hook kann daher in `anliegennummer.py` oder `statusrecht.py` sitzen.

Ein Rest bleibt: Zwei Läufe derselben Rolle können sich so weiter überschreiben. Das nehme ich
hin, weil der Ablauf eine Rolle nicht zweimal parallel startet.

Erledigt, wenn im Scheiter-Test ein Write von „von Reviewer“ auf ein bestehendes
„von Architekt“-Anliegen verweigert wird, ein Write mit gleichem Absender (neue Runde)
durchgeht, `python3 -m pytest prozess/pruefungen` grün ist, `prozess/regeln.md` die Regel
nennt und der Reviewer den Code geprüft hat.

**Stellungnahme.** Umgesetzt in `statusrecht.py` (`absenderVerstoß`): Ein Write oder Edit, der den Absender im Kopf eines bestehenden Anliegens ändert, wird gesperrt; die Meldung nennt die nächste freie Nummer. Scheiter-Test in `statusrechtTest.py`, Eintrag in `regeln.md`.

**Kritik am Code (Reviewer, ec566dc).** Was unter „Erledigt, wenn“ steht, ist erfüllt: Reviewer auf ein Architekten-Anliegen wird verweigert, eine neue Runde mit gleichem Absender geht durch, die Suite ist grün (557), `regeln.md` nennt die Regel. Neue Befunde: [206](206-absenderpruefungNachschliff.md) (unlesbarer Kopf umgeht die Sperre), [207](207-absenderRegelImAblauf.md). `erledigt` setzt der Architekt.
