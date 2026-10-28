import coverage


def umstellen(kontext: str) -> None:
    messung = coverage.Coverage.current()
    if messung is not None:
        messung.switch_context(kontext)


def pytest_runtest_setup(item):
    umstellen(item.nodeid)


def pytest_runtest_logfinish():
    umstellen("")
