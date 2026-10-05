"""Stil und Legende der Dashboard-Seite."""

legende = (
    ("var(--c-orchestrator)", "Gold: Koordinator", False),
    ("var(--c-subagent)", "Grau: Rolle", False),
    ("var(--c-warnung)", "Rot: ab Warnschwelle", False),
    ("var(--c-winddown)", "Gestrichelt: Warnschwelle", True),
    ("var(--c-korridor)", "Gestrichelt: Sperrschwelle", True),
    ("var(--c-peak)", "Gestrichelt: Median", True),
)

stil = """
:root{--bg:#0f0e0c;--panel:#1c1a14;--panel-2:#23201a;--text:#e6dcc4;--text-muted:#a89a72;
--border:#3a3526;--accent-text:#c9a869;--c-subagent:#7c8ba1;--c-orchestrator:#c9a869;--c-warnung:#f43f5e;
--c-peak:#fbbf24;--c-winddown:#d946ef;--c-korridor:#f97316}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--text);
font-family:"Segoe UI",system-ui,Roboto,Arial,sans-serif;
margin:0;padding:20px 28px 56px;line-height:1.5}
h1{color:var(--accent-text);font-size:1.5rem;margin:0 0 4px}
h3{color:var(--text);font-size:.98rem;margin:0 0 8px}
.muted{color:var(--text-muted);font-size:.86rem}
.bericht-zeile{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap}
.karten-spalte{flex:3 1 620px;min-width:320px}
.seiten-spalte{flex:1 1 280px;min-width:260px}
.kasten,.sitzungs-karte{background:var(--panel);border:1px solid var(--border);
border-radius:10px;padding:12px 14px;margin-bottom:14px;font-size:.84rem}
.sitzungs-karte>h3{color:var(--accent-text);margin:0 0 2px;font-size:1rem}
.karten-kopf{color:var(--text-muted);font-size:.8rem;margin:0 0 8px}
.karten-diagramm{overflow-x:auto}
svg{display:block;max-width:100%;height:auto;background:var(--panel-2);border-radius:6px}
.gitter{stroke:var(--border);stroke-width:1}
.achse-text{fill:var(--text-muted);font-size:10px}
.schwelle-winddown{stroke:var(--c-winddown);stroke-width:1.5;stroke-dasharray:5 4}
.schwelle-korridor{stroke:var(--c-korridor);stroke-width:1.5;stroke-dasharray:5 4}
.schwelle-text{font-size:9px}
.schwelle-text.winddown{fill:var(--c-winddown)}.schwelle-text.korridor{fill:var(--c-korridor)}
.saeule{fill:var(--c-subagent)}.saeule.warnung{fill:var(--c-warnung)}.saeule.orchestrator{fill:var(--c-orchestrator)}
.vert-median{stroke:var(--c-peak);stroke-width:1.5;stroke-dasharray:4 3}
.wert-text{fill:var(--text);font-size:9px;font-weight:600}
.rollen-text{fill:var(--text-muted);font-size:8.5px}
table.auftraege{border-collapse:collapse;width:100%;font-size:.82rem;margin-top:10px}
table.auftraege th,table.auftraege td{border:1px solid var(--border);
padding:4px 8px;text-align:left}
table.auftraege th{background:var(--panel-2);color:var(--accent-text);font-weight:600}
table.auftraege td.rolle{color:var(--c-subagent)}
table.auftraege td.stand{text-align:right;font-variant-numeric:tabular-nums}
.legende ul{list-style:none;margin:0;padding:0}
.legende li{display:flex;gap:8px;margin-bottom:9px}
.legende .marke{flex:0 0 18px;height:12px;margin-top:3px;border-radius:2px}
.legende .marke.linie{height:0;border-top:2px dashed;margin-top:8px}
"""
