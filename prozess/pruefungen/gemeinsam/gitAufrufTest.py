import subprocess

from gemeinsam.gitAufruf import freigaben

kennungLänge = 40


def commit(ordner, betreff):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", betreff]
        + ["--allow-empty"],
        cwd=ordner,
        check=True,
    )


def testFreigabeNenntKennungUndBetreff(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    commit(tmp_path, "Anderes")
    commit(tmp_path, "Freigabe Plan 2")
    gefunden = freigaben(tmp_path)
    assert [freigabe.betreff for freigabe in gefunden] == ["Freigabe Plan 2"]
    assert len(gefunden[0].kennung) == kennungLänge
