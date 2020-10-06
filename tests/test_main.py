#!/usr/bin/env python3

import pytest
from pathins.__main__ import run


def test_run_missing_subcommand(capsys):
    with pytest.raises(SystemExit) as e:
        run([])

    captured = capsys.readouterr()
    assert e.value.code == 1
    assert "error: please enter a valid sub-command" in captured.err


def test_run_invalid_subcommand(capsys):
    with pytest.raises(SystemExit) as e:
        run(["boguscmd"])

    captured = capsys.readouterr()
    assert e.value.code == 2
    assert "argument subparser_name: invalid choice" in captured.err


def test_run_help(capsys):
    with pytest.raises(SystemExit) as e:
        run(["--help"])

    captured = capsys.readouterr()
    assert e.value.code == 0
    assert "usage:" in captured.out
    assert "positional arguments:" in captured.out
    assert "optional arguments:" in captured.out


def test_run_version(capsys):
    with pytest.raises(SystemExit) as e:
        run(["--version"])

    captured = capsys.readouterr()
    assert e.value.code == 0
    assert "pathins v" in captured.out


#
#
# Sub-command parsers
#
#


def test_run_coordinates_subcmd_invalid_file(capsys):
    with pytest.raises(SystemExit) as e:
        run(["coordinates", "boguspath"])

    captured = capsys.readouterr()
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_run_coordinates_subcmd_version(capsys):
    with pytest.raises(SystemExit) as e:
        run(["coordinates", "--version"])

    captured = capsys.readouterr()
    assert e.value.code == 0
    assert "pathins v" in captured.out


def test_run_direction_subcmd_invalid_file(capsys):
    with pytest.raises(SystemExit) as e:
        run(["direction", "boguspath"])

    captured = capsys.readouterr()
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_run_direction_subcmd_version(capsys):
    with pytest.raises(SystemExit) as e:
        run(["direction", "--version"])

    captured = capsys.readouterr()
    assert e.value.code == 0
    assert "pathins v" in captured.out


def test_run_path_subcmd_invalid_file(capsys):
    with pytest.raises(SystemExit) as e:
        run(["path", "boguspath"])

    captured = capsys.readouterr()
    assert e.value.code == 1
    assert "does not appear to be a file" in captured.err


def test_run_path_subcmd_version(capsys):
    with pytest.raises(SystemExit) as e:
        run(["path", "--version"])

    captured = capsys.readouterr()
    assert e.value.code == 0
    assert "pathins v" in captured.out
