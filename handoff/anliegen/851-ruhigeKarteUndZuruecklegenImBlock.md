# Ruhige Karte beim Umschalter, Zurücklegen in „Ganze Einheit“

851 · Kritik · von Fachkritiker → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.**
1. Nach ihrem Zweck verschiebt sich die *Karte* in
   [QUE-7](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) nicht, wenn etwas neben ihr
   erscheint oder verschwindet. QUE-7.1 zählt aber nur einige Fälle auf: einen *Grund*,
   „zurück“, „gemeinsam übergehen“ und *an der Reihe*. Es fehlen der Umschalter
   „Ganze Einheit / Einzelmodelle“, der nach AUF-20.1 mit der *Auswahl* erscheint und nach
   AUF-5.10 verschwindet, und „Aufstellen der Einheit beenden“, falls er je nach Lage fehlt
   (siehe [852](852-beendenFehltInAuf19UndAuf22.md)).
2. AUF-21.1 regelt in der *Ebene* „Ganze Einheit“ nur das Ziehen auf der *Karte* (AUF-8.2).
   Für das Ziehen eines *Modells* auf die *Ablage* (AUF-8.3) sagt kein Kriterium, ob es nur
   dieses *Modell* *zurücklegt* oder die ganze *Einheit*.

Einordnung nach Ich 3: beides sind Lücken abseits des Happy Path, sie warten.

**Kosten.** Zu 1: Steht die *Ablage* bei schmalem Fenster über der *Karte*, springt sie beim
Auswählen. Die Technik muss das nicht verhindern. Zu 2: Die Technik wählt selbst, der
Testautor hat nichts zu prüfen.

**Gegenvorschlag.** Zu 1: QUE-7.1 allgemein fassen, etwa „wenn neben der *Karte* etwas zu
sehen beginnt oder aufhört“. Zu 2: eine Frage an den Stakeholder mit Empfehlung, etwa: nur das
gezogene *Modell*, wie in der *Ebene* „Einzelmodelle“. Erledigt, wenn beides geregelt ist oder
du begründest, warum nicht.

**Stellungnahme.** Angenommen, beides umgesetzt.
1. [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) gilt jetzt für alles, was
   neben der *Karte* zu sehen beginnt oder aufhört; die Beispiele nennen „Ganze Einheit“ und
   „Einzelmodelle“ und „Aufstellen der Einheit beenden“. QUE-7.1 hat noch keinen Test, die
   Kennung bleibt.
2. Frage an den Stakeholder: [890](890-zuruecklegenInGanzeEinheit.md). Ich empfehle B, die
   ganze *Einheit*, nicht das gezogene *Modell*: So bewegt „Ganze Einheit“ den Block auf
   der *Karte* wie auf die *Ablage*, und eine *Formation* ist mit einem Zug wieder vom Tisch
   und neu zu klicken (AUF-18.5 ändert sonst nichts); einzelne *Modelle* legt
   „Einzelmodelle“ zurück. Mit dieser Annahme steht es in
   [AUF-23.1](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md), eigene
   Datei, weil AUF-21 an der Grenze von 1.200 Zeichen ist. Antwortet er A, entfällt AUF-23.
