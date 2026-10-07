"""Hook (SubagentStart, SubagentStop): meldet Änderungen außerhalb der Schreibpfade."""

from pathlib import Path

from gemeinsam.gitAufruf import geänderteDateien, kopfCommit
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import istNurLesbar, nurLesbar, projektordner
from lesen.agenten import darfSchreiben, schreibpfade

kopfPräfix = "HEAD "


def standDatei(wurzel: Path, agentId: str) -> Path:
    return wurzel / ".git" / "arbiter-schreibgrenze" / f"{agentId}.txt"


def beimStart(eingabe: HookEingabe, wurzel: Path) -> dict:
    datei = standDatei(wurzel, eingabe.agentId)
    datei.parent.mkdir(parents=True, exist_ok=True)
    zeilen = [f"{kopfPräfix}{kopfCommit(wurzel)}", *sorted(geänderteDateien(wurzel))]
    datei.write_text("\n".join(zeilen), encoding="utf-8")
    muster = schreibpfade(eingabe.rolle, wurzel)
    return zusatzkontext(
        "SubagentStart",
        "Deine Schreibpfade: "
        + (", ".join(muster) if muster else "keine, du schreibst nichts")
        + f". Für alle nur lesbar: {', '.join(nurLesbar)}.",
    )


def beimEnde(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    datei = standDatei(wurzel, eingabe.agentId)
    zeilen = datei.read_text(encoding="utf-8").splitlines() if datei.exists() else []
    datei.unlink(missing_ok=True)
    kopfVorher = next(
        (zeile.removeprefix(kopfPräfix) for zeile in zeilen if zeile.startswith(kopfPräfix)), None
    )
    vorher = {zeile for zeile in zeilen if not zeile.startswith(kopfPräfix)}
    rolle = eingabe.rolle
    muster = schreibpfade(rolle, wurzel)
    meldungen = []
    verstöße = sorted(
        pfad
        for pfad in geänderteDateien(wurzel) - vorher
        if istNurLesbar(pfad) or not darfSchreiben(pfad, muster)
    )
    if verstöße:
        meldungen.append(
            f"Schreibgrenze verletzt: {rolle} hat außerhalb seiner Schreibpfade oder in nur "
            f"lesbaren Pfaden geändert: {', '.join(verstöße)}."
        )
    if kopfVorher is not None and kopfCommit(wurzel) != kopfVorher:
        meldungen.append(
            f"Während {rolle} lief, kam ein Commit hinzu. Hast du ihn nicht selbst gemacht, "
            f"hat {rolle} committet; das ist dem Koordinator vorbehalten."
        )
    if not meldungen:
        return None
    return zusatzkontext(
        "SubagentStop", " ".join(meldungen) + " Nicht committen, dem Stakeholder melden."
    )


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    if eingabe.ereignis == "SubagentStart" and eingabe.agentId and eingabe.rolle:
        return beimStart(eingabe, wurzel)
    if eingabe.ereignis == "SubagentStop" and eingabe.agentId and eingabe.rolle:
        return beimEnde(eingabe, wurzel)
    return None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
