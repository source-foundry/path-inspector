import pytest

import pathins.stringbuilder


def test_bold_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.bold_text("TEST")
    assert res == "\033[1mTEST\033[0m"


def test_bold_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.bold_text("TEST", nocolor=True)
    assert res == "TEST"


def test_cyan_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_text("TEST")
    assert res == "\033[36mTEST\033[0m"


def test_cyan_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_text("TEST", nocolor=True)
    assert res == "TEST"


def test_cyan_bright_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_bright_text("TEST")
    assert res == "\033[1;96mTEST\033[0m"


def test_cyan_bright_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.cyan_bright_text("TEST", nocolor=True)
    assert res == "TEST"


def test_green_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.green_text("TEST")
    assert res == "\033[32mTEST\033[0m"


def test_green_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.green_text("TEST", nocolor=True)
    assert res == "TEST"


def test_red_text(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.red_text("TEST")
    assert res == "\033[31mTEST\033[0m"


def test_red_text_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.red_text("TEST", nocolor=True)
    assert res == "TEST"


def test_report_header(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.report_header("TEST")
    assert res == "-----\n\033[1;96mTEST\033[0m\n-----"


def test_report_header_nocolor(monkeypatch):
    # mock tty
    def mock_isatty():
        return True

    # apply the monkeypatch for sys.stdout.isatty()
    monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

    res = pathins.stringbuilder.report_header("TEST", nocolor=True)
    assert res == "-----\nTEST\n-----"


# def test_overlap_result_pass_default(monkeypatch):
#     # mock tty
#     def mock_isatty():
#         return True

#     # apply the monkeypatch for sys.stdout.isatty()
#     monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

#     res = pathins.stringbuilder.overlap_result("TEST", test_pass=True)
#     assert res == "[ \x1b[31mTEST\x1b[0m ]: Yes"


# def test_overlap_result_pass_nocolor(monkeypatch):
#     # mock tty
#     def mock_isatty():
#         return True

#     # apply the monkeypatch for sys.stdout.isatty()
#     monkeypatch.setattr(pathins.stringbuilder, "IS_A_TTY", mock_isatty)

#     res = pathins.stringbuilder.overlap_result("TEST", test_pass=True, nocolor=True)
#     assert res == "[ TEST ]: Yes"
