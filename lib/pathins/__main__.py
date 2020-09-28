#!/usr/bin/env python3

import argparse
import sys

from pathins import __version__


def main():  # pragma: no cover
    run(sys.argv[1:])


def run(argv):
    # ===========================================================
    # argparse command line argument definitions
    # ===========================================================
    parser = argparse.ArgumentParser(
        description="TTF font curve path inspector"
    )
    parser.add_argument(
        "--version", action="version", version="pathins v{}".format(__version__)
    )
    args = parser.parse_args(argv)
