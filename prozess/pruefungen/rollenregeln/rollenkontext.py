"""Hook (SubagentStart): Die Rolle bekommt Stand und die Ordner-CLAUDE.md ihrer Perspektive."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import perspektiven, projektordner
from lesen.agenten import schreibpfade
from standregeln.abhaken import offeneZeilen
from standregeln.stand import stand


def perspektive(rolle: str, wurzel: Path) -> str | None:
    muster = schreibpfade(rolle, wurzel)
    oberster = muster[0].split("/")[0] if muster else None
    return oberster if oberster in perspektiven else None


def kontext(rolle: str, wurzel: Path) -> str:
    teile = [stand(wurzel)]
    befehl = f"python3 prozess/pruefungen/gemeinsam/lauf.py standregeln.abhaken {rolle}"
    hindernis = befehl.replace("abhaken", "hindernis")
    hinweis = (
        f"Am Ende abhaken: {befehl} <Schritt>\n"
        f"Hält etwas auf: {hindernis} <Schritt> <Rolle, die es beseitigen kann> <Text>"
        " <Nummernbereich des Auftrags, z. B. 3940-3959, oder Nummer des Anliegens, das schon"
        " als Kritik besteht>"
    )
    offen = offeneZeilen(wurzel, rolle)
    schritte = "".join(f"\n- {schritt}" for schritt in offen) or " keine"
    teile.append(f"Offene Schritte im Fortschritt:{schritte}\n{hinweis}")
    ordner = perspektive(rolle, wurzel)
    datei = wurzel / ordner / "CLAUDE.md" if ordner else None
    if datei and datei.is_file():
        teile.append(f"{ordner}/CLAUDE.md:\n" + datei.read_text(encoding="utf-8"))
    return "\n\n".join(teile)


if __name__ == "__main__":
    eingabe = HookEingabe.aus(eingabeLesen())
    if eingabe.rolle:
        antwortAusgeben(zusatzkontext("SubagentStart", kontext(eingabe.rolle, projektordner())))
