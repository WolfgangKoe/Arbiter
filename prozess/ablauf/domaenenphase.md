# Domänenphase

1. Planer: Etappen aus dem Ziel; nur die aktuelle ausformuliert. Auslöser: keine Etappe.
2. Architekt: Kritik an der aktuellen Etappe und der Reihenfolge, als Anliegen.
3. Freigabe: „.“ → Koordinator committet `Freigabe Etappe <n>`.
4. Anforderungsautor, in jedem Zyklus: die Happy Paths des Spielers zum nächsten Schnitt,
   in Zyklus 1 zur Etappe, danach zum Zyklusziel des freigegebenen Reviews samt Kommentaren
   (ohne dieses zum Abschnitt „Danach“ des vorigen Plans), abgeleitet aus ArbiterMap und
   Arbiter-old ([Domäne](../../domaene/CLAUDE.md)); Begriffe ins Glossar. Eine genügt.
   Auslöser: kein Kriterium ohne Akzeptanztest. Bei einer Oberfläche danach
   [UX](../../.claude/agents/ux.md): ein Mockup je Anforderung ([DoR 5](dor.md)); das Item
   verlinkt es. Mechanismus: nur Text.
5. Fachkritiker: prüft Anforderungen und Mockups gegen Ziel und Regeltext
   ([Kritik](kritik.md)). Mechanismus: nur Text.
6. Planer: `handoff/plan.md` (`# Plan · Zyklus <n>`) mit den Items, die bereit sind
   ([DoR](dor.md)): eins genügt, höchstens drei; weicht er vom Zyklusziel des Reviews ab,
   begründet er es. Am Ende der Abschnitt `## Freigabe` ([Freigabe und Kommentare](freigabe.md)).
   Weitere Anforderungen kommen in späteren Zyklen. Jedes Item steht als Link
   `[…](../domaene/items/<id>.md)`; daran erkennt die Rückverfolgung die Items des Plans
   ([DoD 2](dod.md)). Mechanismus: `lesen/plan.py` (`offeneItems`). Jedes Item nennt
   Kriterien ohne Test (`AUF-7.3`) oder ihre Anforderung; bis dahin ist der Plan nicht zur
   Freigabe bereit. Mechanismus: nur Text; der Stand nennt die Kriterien ohne Test.
7. Kritik am Plan samt Items, Anforderungen und Mockups ([Kritik](kritik.md)).
8. Freigabe ([Freigabe und Kommentare](freigabe.md)) → Koordinator committet
   `Freigabe Plan <n>`. Danach [Technikphase](technikphase.md).

Kritik blockiert nicht: Offene Anliegen stehen in der Freigabevorlage, sortiert vom
Moderator (`handoff/moderation.md`). Mechanismus: nur Text. Wer gleichzeitig läuft:
[Gleichzeitige Läufe](gleichzeitigeLaeufe.md).
