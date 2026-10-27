"""Command-line interface for nmp-notes."""

import argparse
import sys
from typing import List, Optional

from nmp import __version__
from nmp.mk import (
    NMPError,
    PRACTICALS,
    TargetFileExistsError,
    TemplateNotFoundError,
    available_templates,
    file,
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="nmp",
        description="Pick a college practical, drop its code into the current folder.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # Subcommand: list
    subparsers.add_parser(
        "list",
        help="List all available practicals.",
    )

    # Subcommand: create
    create_parser = subparsers.add_parser(
        "create",
        help="Create a practical file.",
    )
    create_parser.add_argument(
        "template",
        type=str,
        choices=list(PRACTICALS),
        help="Practical slug (e.g., '1a-bfs').",
    )
    create_parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Custom destination filename (default: practical's own filename).",
    )

    return parser


def handle_list() -> int:
    """Handle execution of the 'list' subcommand."""
    for i, slug in enumerate(PRACTICALS, 1):
        print(f"{i}. {PRACTICALS[slug][0]} ({slug})")
    return 0


def handle_create(args: argparse.Namespace) -> int:
    """Handle execution of the 'create' subcommand."""
    try:
        created_path = file(name=args.template, filename=args.output)
    except TargetFileExistsError:
        try:
            ans = input(f"{args.output or PRACTICALS[args.template][1]} exists. Overwrite? [y/N] ").strip().lower()
        except EOFError:
            ans = "n"
        if ans != "y":
            print("Cancelled.")
            return 1
        created_path = file(name=args.template, filename=args.output, force=True)
    except (TemplateNotFoundError, ValueError, NMPError) as err:
        print(f"[Error] {err}", file=sys.stderr)
        return 1
    print(f"Created {created_path.name} <- {PRACTICALS[args.template][0]}")
    return 0


def _matches(slugs: List[str], choice: str) -> List[str]:
    """Resolve a number, slug, or partial name to matching slugs."""
    c = choice.strip().lower()
    if c.isdigit():
        n = int(c)
        return [slugs[n - 1]] if 1 <= n <= len(slugs) else []
    if c.endswith(".py"):
        c = c[:-3]
    if c in PRACTICALS:
        return [c]
    hits = [s for s in slugs if c and (c in s or c in PRACTICALS[s][0].lower())]
    if len(hits) > 1:  # prefer a whole slug word: 'bfs' -> 1a-bfs, not 2b-rbfs
        token_hits = [s for s in hits if c in s.split("-")]
        if token_hits:
            hits = token_hits
    return hits


def interactive() -> int:
    """Plain numbered menu; writes the chosen practical into the cwd.

    Cooked mode only (no raw mode / ANSI / alt screen) so it works on every
    terminal, including Windows, dumb terms, SSH and piped stdin.
    """
    slugs = list(PRACTICALS)
    width = len(str(len(slugs)))
    print("College practicals\n")
    for i, s in enumerate(slugs, 1):
        print(f"{i:>{width}}. {PRACTICALS[s][0]} ({s})")
    print()
    while True:
        try:
            choice = input(f"Number or name (1-{len(slugs)}, q to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if choice.lower() in ("q", "quit"):
            return 0
        hits = _matches(slugs, choice)
        if len(hits) == 1:
            return handle_create(argparse.Namespace(template=hits[0], output=None))
        if hits:
            print(f"Ambiguous: {', '.join(hits)} — be more specific.")
        else:
            print(f"No match for '{choice}'. Try a number 1-{len(slugs)} or a name like 'bfs'.")


def main(argv: Optional[List[str]] = None) -> int:
    """CLI main entry point.

    Parameters:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        return handle_list()
    elif args.command == "create":
        return handle_create(args)
    elif args.command is None:
        return interactive()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
