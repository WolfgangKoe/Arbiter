"""Stellt coverage je Test auf dessen Kennung um, damit jede Zeile ihre Tests nennt."""

import coverage


def umstellen(kontext: str) -> None:
    messung = coverage.Coverage.current()
    if messung is not None:
        messung.switch_context(kontext)


def pytest_runtest_setup(item):
    umstellen(item.nodeid)


def pytest_runtest_logfinish():
    umstellen("")
