"""Command-line access to the bundled texts: ``sigurd list|show|export|serve``."""

import argparse
import contextlib
import functools
import html
import json
import os
import sys
import tempfile
from collections.abc import Sequence
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from sigurd import __version__
from sigurd.texts import TEXTS, get_text

__all__ = ["export", "main"]


def export(directory: Path, formats: Sequence[str] = ("txt", "json")) -> list[Path]:
    """Write every bundled text in ``directory``, with an ``index.html`` linking them.

    Args:
        directory: where to write the files, created if needed.
        formats: ``txt`` for plain text, ``json`` for structured data.

    Returns:
        The written files.
    """
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    rows = []
    for text in TEXTS.values():
        links = []
        if "txt" in formats:
            path = directory / f"{text.id}.txt"
            path.write_text(text.as_plain_text(), encoding="utf-8")
            written.append(path)
            links.append(f'<a href="{path.name}">txt</a>')
        if "json" in formats:
            path = directory / f"{text.id}.json"
            data = {
                "id": text.id,
                "title": text.title,
                "source": text.source,
                "text": text.as_data(),
            }
            path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            written.append(path)
            links.append(f'<a href="{path.name}">json</a>')
        rows.append(
            f"<tr><td><code>{text.id}</code></td><td>{html.escape(text.title)}</td>"
            f"<td>{' · '.join(links)}</td><td>{html.escape(text.source)}</td></tr>"
        )
    index = directory / "index.html"
    index.write_text(_INDEX.format(version=__version__, rows="\n".join(rows)), encoding="utf-8")
    written.append(index)
    return written


_INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>sigurd texts</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 60rem; margin: 2rem auto; padding: 0 1rem; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ text-align: left; vertical-align: top; padding: .4rem .6rem; }}
td {{ border-top: 1px solid #ddd; }}
</style>
</head>
<body>
<h1>Nibelungenlied and Völsunga saga — texts</h1>
<p>Texts bundled with <code>sigurd</code> {version}.</p>
<table>
<tr><th>Id</th><th>Title</th><th>Formats</th><th>Source</th></tr>
{rows}
</table>
</body>
</html>
"""


class _UTF8Handler(SimpleHTTPRequestHandler):
    extensions_map = {  # noqa: RUF012
        **SimpleHTTPRequestHandler.extensions_map,
        ".txt": "text/plain; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".html": "text/html; charset=utf-8",
    }


def _serve(host: str, port: int) -> None:
    with tempfile.TemporaryDirectory(prefix="sigurd-") as directory:
        export(Path(directory))
        handler = functools.partial(_UTF8Handler, directory=directory)
        with ThreadingHTTPServer((host, port), handler) as server:
            print(f"Serving the texts on http://{host}:{port}/ (Ctrl+C to stop)", flush=True)
            with contextlib.suppress(KeyboardInterrupt):
                server.serve_forever()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sigurd", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="list the bundled texts")

    show = commands.add_parser("show", help="print a text")
    show.add_argument(
        "text", choices=TEXTS, metavar="TEXT", help="identifier given by `sigurd list`"
    )
    show.add_argument("--json", action="store_true", help="print structured data as JSON")

    export_ = commands.add_parser("export", help="write every text to a directory")
    export_.add_argument("directory", type=Path)
    export_.add_argument(
        "--format", dest="formats", action="append", choices=["txt", "json"], help="default: both"
    )

    serve = commands.add_parser("serve", help="browse the texts over HTTP")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line."""
    args = _parser().parse_args(argv)
    try:
        _run(args)
    except BrokenPipeError:
        # The output was piped into a command that stopped reading it, like `head`.
        # https://docs.python.org/3/library/signal.html#note-on-sigpipe
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
    return 0


def _run(args: argparse.Namespace) -> None:
    if args.command == "list":
        width = max(map(len, TEXTS))
        for text in TEXTS.values():
            print(f"{text.id:<{width}}  {text.title}")
    elif args.command == "show":
        text = get_text(args.text)
        if args.json:
            json.dump(text.as_data(), sys.stdout, ensure_ascii=False, indent=1)
            print()
        else:
            sys.stdout.write(text.as_plain_text())
    elif args.command == "export":
        for path in export(args.directory, args.formats or ("txt", "json")):
            print(path)
    elif args.command == "serve":
        _serve(args.host, args.port)


if __name__ == "__main__":
    sys.exit(main())
