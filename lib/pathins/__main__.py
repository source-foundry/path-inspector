#!/usr/bin/env python3

import argparse
import os
import sys

from . import __version__
from .coordinates import coordinates_run
from .direction import direction_run
from .path import path_run

# from .overlap import overlap_run


def main() -> None:  # pragma: no cover
    run(sys.argv[1:])


def run(argv) -> None:
    # ===========================================================
    # argparse command line argument definitions
    # ===========================================================
    parser = argparse.ArgumentParser(description="TTF font curve path inspector")
    parser.add_argument(
        "-v", "--version", action="version", version=f"pathins v{__version__}"
    )
    subparsers = parser.add_subparsers(dest="subparser_name")

    # -------------------------------
    # coordinates sub-command parser
    # -------------------------------
    parser_coordinates = subparsers.add_parser(
        "coordinates",
        help="Path coordinates inspection",
        description="Path coordinates inspection",
    )
    parser_coordinates.add_argument(
        "-v", "--version", action="version", version=f"pathins v{__version__}"
    )
    parser_coordinates.add_argument(
        "--nocolor", action="store_true", help="no ANSI color"
    )
    parser_coordinates.add_argument("fontpath", type=str, help="font file path")
    parser_coordinates.add_argument(
        "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
    )
    parser_coordinates.set_defaults(func=coordinates_run)

    # -----------------------------
    # direction sub-command parser
    # -----------------------------
    parser_direction = subparsers.add_parser(
        "direction",
        help="Path direction inspection",
        description="Path direction inspection",
    )
    parser_direction.add_argument(
        "-v", "--version", action="version", version=f"pathins v{__version__}"
    )
    parser_direction.add_argument("--nocolor", action="store_true", help="no ANSI color")
    parser_direction.add_argument("fontpath", type=str, help="font file path")
    parser_direction.add_argument(
        "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
    )
    parser_direction.set_defaults(func=direction_run)

    # -----------------------------
    # overlap sub-command parser
    # -----------------------------
    # parser_overlap = subparsers.add_parser(
    #     "overlap", help="Path overlap inspection", description="Path overlap inspection"
    # )
    # parser_overlap.add_argument(
    #     "-v", "--version", action="version", version=f"pathins v{__version__}"
    # )
    # parser_overlap.add_argument(
    #     "--check",
    #     action="store_true",
    #     help="quick check for any overlaps with status code",
    # )
    # parser_overlap.add_argument("--nocolor", action="store_true", help="no ANSI color")
    # parser_overlap.add_argument("fontpath", type=str, help="font file path")
    # parser_overlap.add_argument(
    #     "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
    # )
    # parser_overlap.set_defaults(func=overlap_run)

    # -----------------------------
    # path sub-command parser
    # -----------------------------
    parser_path = subparsers.add_parser("path", help="Path dump", description="Path dump")
    parser_path.add_argument(
        "-v", "--version", action="version", version=f"pathins v{__version__}"
    )
    parser_path.add_argument("--nocolor", action="store_true", help="no ANSI color")
    parser_path.add_argument("fontpath", type=str, help="font file path")
    parser_path.add_argument(
        "glyphname", type=str, help="glyph name (optional, default=all)", nargs="?"
    )
    parser_path.set_defaults(func=path_run)

    # -----------------------------
    # Parse args
    # -----------------------------

    args: argparse.Namespace = parser.parse_args(argv)
    # execute the default function assigned to the subcommand
    if args.subparser_name is None:
        parser.print_usage()
        sys.stderr.write(f"pathins: error: please enter a valid sub-command{os.linesep}")
        sys.exit(1)
    else:
        args.func(args)
