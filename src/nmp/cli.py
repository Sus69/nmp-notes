"""Command-line interface for nmp-notes."""

import argparse
import sys
from typing import List, Optional

from nmp import __version__
from nmp.mk import (
    NMPError,
    TargetFileExistsError,
    TemplateNotFoundError,
    available_templates,
    file,
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="nmp",
        description="NMP Notes - Quickly scaffold practical lab files from templates.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        metavar="<command>",
    )

    # Subcommand: make
    make_parser = subparsers.add_parser(
        "make",
        help="Generate a practical file from a template.",
        description="Generate a practical file from a template in dot notation (e.g., ai.p1).",
    )
    make_parser.add_argument(
        "template_name",
        type=str,
        help="Template name in dot notation (e.g., 'ai.p1', 'dbms.p1').",
    )
    make_parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save the created file into (default: current directory).",
    )
    make_parser.add_argument(
        "-f",
        "--filename",
        type=str,
        default=None,
        help="Custom destination filename (default: <name_with_underscores>.py).",
    )
    make_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite destination file if it already exists.",
    )

    # Subcommand: list
    subparsers.add_parser(
        "list",
        help="List all available practical templates.",
        description="Display all practical lab templates found in the installed library.",
    )

    return parser


def handle_make(args: argparse.Namespace) -> int:
    """Handle execution of the 'make' subcommand."""
    try:
        created_path = file(
            name=args.template_name,
            output_dir=args.output_dir,
            filename=args.filename,
            force=args.force,
        )
        print(f"[OK] Created practical file: {created_path}")
        return 0
    except TargetFileExistsError as err:
        print(f"[Error] {err}", file=sys.stderr)
        return 1
    except TemplateNotFoundError as err:
        print(f"[Error] {err}", file=sys.stderr)
        return 1
    except (ValueError, NMPError) as err:
        print(f"[Error] {err}", file=sys.stderr)
        return 1
    except Exception as err:
        print(f"[Unexpected Error] {err}", file=sys.stderr)
        return 1


def handle_list() -> int:
    """Handle execution of the 'list' subcommand."""
    templates = available_templates()
    if not templates:
        print("No templates found.")
        return 0

    print(f"Available practical templates ({len(templates)}):")
    for name in templates:
        print(f"  - {name}")
    print("\nTip: Run 'nmp make <template_name>' to generate a practical file.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """CLI main entry point.

    Parameters:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "make":
        return handle_make(args)
    elif args.command == "list":
        return handle_list()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
