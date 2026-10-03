# Kritik Der Zweck der Anforderung Aufstellung.md ist zu knapp.

97 · Kritik · von Stakeholder → Anforderungsautor (Domäne) · Runde 1/3 · erledigt

## Runde 1
"Zweck: Reihenfolge von Only War. Alle Kriterien: `core_rules.txt:2322`." 

Kritik: Die Aussage ist zu verkürzt dargestellt. Es ist nicht klar, was hier erreicht werden soll. Geht es um die Reihenfolge der Aufstellung von Einheiten einer Armee? Geht es um die Aufstellung von Einheiten im Schritt Reserven einsetzen der Bewegungsphase? Außerdem wäre ein Link zu der Datei in den Core_rules nett und hier soll dann auch zu den Methoden oder Klassen der Aufstellung verwiesen werden, welche von den Agenten aus der Technik geschrieben werden.

**Stellungnahme:**
Angenommen bis auf den Verweis auf Code; umgesetzt in
[aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md):
- Es geht um Schritt 4 „Deploy Forces“ von Only War, nicht um Reserven. Das sagt jetzt ein
  Absatz über allen Anforderungen der Datei; die „Reinforcements“ der Bewegungsphase
  (`core_rules.txt:800`) schließt er ausdrücklich aus. Der Zweck von AUF-1 nennt Zonenwahl und
  Reihenfolge; mehr Text trägt AUF-1 nicht, sie hält mit 1.199 Zeichen das Höchstmaß von 1.200
  (`domaene/CLAUDE.md`), und ihre Kriterien sind getestet.
- Jede Fundstelle in der Datei ist ein Link auf ihre Zeile in `core_rules.txt`, die Daten auf
  ihre YAML-Dateien.
- Nicht übernommen: Links auf Klassen und Methoden. Anforderungen beschreiben keine Technik
  (`domaene/CLAUDE.md`) und ändern sich nicht, wenn der Code umzieht; ein Link dorthin veraltet
  still. Der Weg zum Code führt über die Kriterien-ID: Sie springt zum Akzeptanztest
  ([83](83-sprungErproben.md)), der Test ruft die Klassen auf. Willst du trotzdem einen direkten
  Verweis, setz das Anliegen wieder auf offen.

**Stellungnahme:** Du hast die Anforderung effektiv in drei Teile geschnitten. Damit bin ich einverstanden. An sich könntest du daraus auch drei Dateien machen, um das Zeichenlimit wieder zu reduzieren. Ausgangslage von Only War AUF-2 lässt sich auch verallgemeinern und wäre damit eine eigene Anforderung. Dasselbe trifft auf AUF-3 das Setzen zu. Beim Bewegen dürfen Bases sich ebenfalls nicht überlappen.

**Stellungnahme:**
Angenommen und umgesetzt nach deinen Antworten in Anliegen 105 (F1 A, F2 A, F3 A, git):
- Drei Dateien nach den Bereichen aus `domaene/CLAUDE.md` (das Höchstmaß gilt je
  Anforderung, AUF-1 bleibt, wie sie ist):
  [spielobjekte.md](../../domaene/anforderungen/spielobjekte.md) mit OBJ-1 (*Armeen*,
  *Bases*, *Spielfeld*, gleich welche *Mission*),
  [querschnitt.md](../../domaene/anforderungen/querschnitt.md) mit QUE-1 (*Setzen* und
  ‚Base überdeckt‘) und [aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md) mit
  dem, was nur die *Aufstellung* von Only War betrifft.
- AUF-2.1 bis AUF-2.3, AUF-3.1 und AUF-3.3 sind ersetzt. Die Werte aus den YAML-Dateien
  stehen jetzt in AUF-2.6 und AUF-2.7.
- Bewegen: Arbiter prüft den gezogenen Weg (`core_rules.txt:729`). Das Kriterium QUE-2 kommt
  mit den Anforderungen zu Etappe 2.

Die neuen Kennungen stehen in Item 1, Item 2 und Plan 2 (Anliegen 106, erledigt, git).
