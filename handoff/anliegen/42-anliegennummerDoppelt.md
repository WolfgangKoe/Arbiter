# Anliegennummer doppelt vergeben

42 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Fachkritiker und Architekt liefen gleichzeitig und haben beide die Nummer 40
vergeben: [40-aufstellenTestNachDerUmbenennung.md](40-aufstellenTestNachDerUmbenennung.md)
und [40-uebergangsresteNachDerUmbenennung.md](40-uebergangsresteNachDerUmbenennung.md).
Drei Sekunden nach dieser Datei legte der Implementierer
[42-importreiheFolgtDemProdukt.md](42-importreiheFolgtDemProdukt.md) an: wieder doppelt.
`anliegen.py` prüft nur, ob Kopf und Dateiname zueinander passen, nicht, ob die Nummer
eindeutig ist; `python3 -m pytest prozess/pruefungen` ist grün.

**Kosten.** „Anliegen 40“ in Stand, Commit-Nachricht und Verweisen ist mehrdeutig; die
fällige Nachprüfung nennt zwei Rollen mit derselben Nummer. Gleichzeitige Läufe sind erlaubt
(`prozess/ablauf.md`), der Fall kommt also wieder. Umbenennen darf der Absender nicht selbst:
Anliegen ändern Rollen nur mit Write und Edit, löschen tut nur `erledigteLoeschen.py`.

**Gegenvorschlag.**
1. Scheiter-Test in `anliegenTest.py`: Zwei Dateien mit derselben Nummer sind rot.
2. Die jüngere Datei je Paar, `40-uebergangsresteNachDerUmbenennung.md` und
   `42-importreiheFolgtDemProdukt.md`, bekommt die nächste freie Nummer, mit Kopfzeile. Das kann nur eine Rolle mit Bash im Prozess oder der Koordinator
   beim Commit; welche, entscheidest du.

**Stellungnahme.** Umgesetzt (P3 der Retro 1): `anliegennummer.py` sperrt Write einer
neuen Datei mit vergebener Nummer und nennt die nächste freie (auch aus git, nie neu
vergeben); `doppelteNummern` und der Test `testKeinePaarMitDerselbenNummerImRepo` aus deinem
Gegenvorschlag 1, Scheiter-Tests in `anliegennummerTest.py`. Punkt 2 ist hinfällig: im Repo
gibt es keine doppelte Nummer mehr.
