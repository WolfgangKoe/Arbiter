from mutationsregeln.geaenderteZeilen import geänderteZeilen, zeilenAusDiff

diff = (
    "diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n"
    "@@ -3,0 +4,2 @@ def x():\n+eins\n+zwei\n"
    "@@ -9 +11 @@\n-alt\n+neu\n"
    "@@ -20,2 +22,0 @@\n-weg\n-weg\n"
    "diff --git a/b.py b/b.py\n--- a/b.py\n+++ /dev/null\n@@ -1 +0,0 @@\n-x\n"
)


def testDerDiffNenntDieNeuenZeilenJeDatei():
    assert zeilenAusDiff(diff) == {"a.py": {4, 5, 11}}


def testNurGeänderteZeilenSeitDerPlanfreigabeZählen(gitRepo):
    ordner = gitRepo.ordner / "technik" / "arbiter" / "domaene"
    ordner.mkdir(parents=True)
    (ordner / "alt.py").write_text("a = 1\nb = 2\nc = 3\n", encoding="utf-8")
    gitRepo.festhalten("Freigabe Plan 1")
    (ordner / "alt.py").write_text("a = 1\nb = 5\nc = 3\nd = 4\n", encoding="utf-8")
    (ordner / "neu.py").write_text("x = 1\ny = 2\n", encoding="utf-8")
    (ordner / "notiz.md").write_text("x\n", encoding="utf-8")
    assert geänderteZeilen(gitRepo.ordner, "technik/arbiter/domaene") == {
        "technik/arbiter/domaene/alt.py": {2, 4},
        "technik/arbiter/domaene/neu.py": {1, 2},
    }
