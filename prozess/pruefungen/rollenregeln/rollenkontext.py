"""Hook (SubagentStart): Die Rolle bekommt Stand und die Ordner-CLAUDE.md ihrer Perspektive."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import perspektiven, projektordner
from lesen.agenten import schreibpfade
from standregeln.stand import stand


def perspektive(rolle: str, wurzel: Path) -> str | None:
    muster = schreibpfade(rolle, wurzel)
    oberster = muster[0].split("/")[0] if muster else None
    return oberster if oberster in perspektiven else None


def kontext(rolle: str, wurzel: Path) -> str:
    teile = [stand(wurzel)]
    ordner = perspektive(rolle, wurzel)
    datei = wurzel / ordner / "CLAUDE.md" if ordner else None
    if datei and datei.is_file():
        teile.append(f"{ordner}/CLAUDE.md:\n" + datei.read_text(encoding="utf-8"))
    return "\n\n".join(teile)


if __name__ == "__main__":
    eingabe = HookEingabe.aus(eingabeLesen())
    if eingabe.rolle:
        antwortAusgeben(zusatzkontext("SubagentStart", kontext(eingabe.rolle, projektordner())))
