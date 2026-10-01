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


BOLD, DIM, REV, RESET = "\033[1m", "\033[2m", "\033[7m", "\033[0m"


def _arrow_menu(slugs: List[str]) -> Optional[str]:
    """Arrow-key menu (up/down + Enter, number shortcut, type-to-filter, q to quit)."""
    idx, query = 0, ""

    def filtered() -> List[str]:
        q = query.lower()
        return [s for s in slugs if q in s.lower() or q in PRACTICALS[s][0].lower()] or slugs

    def render(items: List[str]) -> None:
        # Full-screen redraw on alternate screen: no cursor math, no wrap bugs.
        # NOTE: raw mode disables ONLCR, so bare \n won't return the
        # carriage (staircase effect). Use \r\n for every line in here.
        NL = "\r\n"
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(f"{BOLD}College practicals{RESET}{DIM}  up/down navigate · type to filter · Enter to create · q to quit{RESET}{NL}{NL}")
        if query:
            sys.stdout.write(f"Filter: {BOLD}{query}{RESET}  {DIM}(esc clears){RESET}{NL}{NL}")
        for i, s in enumerate(items):
            line = f"  {i + 1}. {PRACTICALS[s][0]} {DIM}({s}){RESET}"
            if i == idx:
                sys.stdout.write(f"{REV}>{line}{RESET}{NL}")
            else:
                sys.stdout.write(f" {line}{NL}")
        sys.stdout.flush()

    if sys.platform == "win32":
        import msvcrt
        import os
        os.system("")  # Enable ANSI terminal mode in Windows console
        try:
            sys.stdout.write("\033[?1049h\033[?25l")  # alt screen, hide cursor
            sys.stdout.flush()
            render(filtered())
            while True:
                ch = msvcrt.getwch()
                items = filtered()
                if ch == "\x03":  # Ctrl+C
                    return None
                if ch.lower() == "q" and not query:
                    return None
                if ch in ("\r", "\n"):
                    return items[idx] if items else None
                if ch in ("\x00", "\xe0"):
                    code = msvcrt.getwch()
                    if code == "H":  # Up arrow
                        idx = (idx - 1) % len(items)
                    elif code == "P":  # Down arrow
                        idx = (idx + 1) % len(items)
                    render(filtered())
                elif ch == "\x1b":  # Esc
                    query, idx = "", 0
                    render(filtered())
                elif ch in ("\x7f", "\x08"):
                    query = query[:-1]
                    idx = 0
                    render(filtered())
                elif ch.isdigit() and not query:
                    n = int(ch)
                    if 1 <= n <= len(items):
                        return items[n - 1]
                elif ch.isprintable():
                    query += ch
                    idx = 0
                    render(filtered())
        finally:
            sys.stdout.write("\033[?25h\033[?1049l")  # restore cursor + main screen
            sys.stdout.flush()
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdout.write("\033[?1049h\033[?25l")  # alt screen, hide cursor
            sys.stdout.flush()
            render(filtered())
            while True:
                ch = sys.stdin.read(1)
                items = filtered()
                if ch == "\x03":
                    return None
                if ch.lower() == "q" and not query:
                    return None
                if ch in ("\r", "\n"):
                    return items[idx] if items else None
                if ch == "\x1b":  # arrows / esc
                    nxt = sys.stdin.read(2)
                    if nxt == "[A":
                        idx = (idx - 1) % len(items)
                    elif nxt == "[B":
                        idx = (idx + 1) % len(items)
                    else:  # lone Esc clears filter
                        query, idx = "", 0
                    render(filtered())
                elif ch in ("\x7f", "\x08"):
                    query = query[:-1]
                    idx = 0
                    render(filtered())
                elif ch.isdigit() and not query:
                    n = int(ch)
                    if 1 <= n <= len(items):
                        return items[n - 1]
                elif ch.isprintable():
                    query += ch
                    idx = 0
                    render(filtered())
        finally:
            sys.stdout.write("\033[?25h\033[?1049l")  # restore cursor + main screen
            sys.stdout.flush()
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def interactive() -> int:
    """Numbered/arrow-key menu; writes the chosen practical into the cwd."""
    slugs = list(PRACTICALS)
    if sys.stdin.isatty():
        try:
            slug = _arrow_menu(slugs)
        except Exception:  # ponytail: no TTY/raw mode -> plain prompt fallback
            slug = False
            print("Fancy menu unavailable, using plain prompt.")
        if slug:
            return handle_create(argparse.Namespace(template=slug, output=None))
        if slug is None:
            print("Cancelled.")
            return 1
    for i, s in enumerate(slugs, 1):  # non-TTY fallback
        print(f"{i}. {PRACTICALS[s][0]} ({s})")
    try:
        choice = input("Select number: ").strip()
    except EOFError:
        return 1
    if not choice.isdigit() or not 1 <= int(choice) <= len(slugs):
        print("Invalid choice.", file=sys.stderr)
        return 1
    return handle_create(argparse.Namespace(template=slugs[int(choice) - 1], output=None))


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
