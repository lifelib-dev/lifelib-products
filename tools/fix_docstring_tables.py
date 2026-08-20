"""Widen the RST simple tables in model docstrings whose cells outgrew their columns.

Every model's ``Projection`` docstring carries the mapping from the technical notes'
actuarial symbols to the cells names, laid out as an RST simple table.  A handful of cells
names are longer than the column rule they sit under -- ``plt_mort_factor_init_formula`` is
28 characters in a 26-character column -- and docutils rejects the whole table with
"Malformed table", losing the mapping that is the single most useful thing on the page.

Only *interior* boundaries matter: the last column may legally run past its rule, so a long
description is fine and a long cells name is not.

The fix re-lays the table: measure every cell, widen each column to fit, re-emit.  Cells are
recovered by splitting on runs of two or more spaces, which is what separates columns here
and never occurs inside a cell.

**Columns are measured in display width, not characters.**  docutils lays a simple table out
by display column, where an East Asian wide or fullwidth character occupies two.  jplib's
docstrings carry Japanese in the symbol column, so a character-counting version of this tool
reads a correctly laid out table as broken and re-lays it into one that really is -- the
failure runs in the direction that turns a clean build into "Malformed table".  Every
measurement below therefore goes through :func:`width`.

Usage::

    python tools/fix_docstring_tables.py lifelib/libraries/uslib --dry-run
    python tools/fix_docstring_tables.py lifelib/libraries/uslib
"""
import re
import sys
import pathlib
import collections
import unicodedata


RULE = re.compile(r'^(\s*)=+(\s+=+)+\s*$')


def char_width(ch):
    """Display columns one character occupies: two if East Asian wide or fullwidth."""
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def width(text):
    """Display width of ``text``, which is what docutils measures a table by."""
    return sum(char_width(c) for c in text)


def at_column(row, col):
    """The character occupying display column ``col``, or "" if the row ends first.

    A wide character straddling the boundary is returned, which is the answer that
    matters: it is occupying the column either way.
    """
    pos = 0
    for ch in row:
        w = char_width(ch)
        if pos <= col < pos + w:
            return ch
        pos += w
    return ""


def between_columns(row, start, stop):
    """The substring of ``row`` occupying display columns ``[start, stop)``."""
    out, pos = [], 0
    for ch in row:
        if pos >= stop:
            break
        if pos >= start:
            out.append(ch)
        pos += char_width(ch)
    return "".join(out)


def columns(rule):
    """(start, end) of each column marker in a rule line.

    Rule lines are pure ASCII, so their character and display indices coincide.
    """
    return [(m.start(), m.end()) for m in re.finditer(r'=+', rule)]


def overflows(row, bounds):
    """True if a cell intrudes on an interior separator, measured by display width.

    The whole separator span is checked, not just its first column.  A cell that is one
    column too *short* pushes the next cell one column left, into the far end of the
    separator -- which docutils rejects exactly as it rejects a cell that is too long, and
    which a single-column check walks straight past.  Renaming a cells to a shorter name
    without re-padding produces precisely that row.
    """
    for i, (_, end) in enumerate(bounds[:-1]):
        stop = bounds[i + 1][0]
        for col in range(end, stop):
            if at_column(row, col) not in ("", " "):
                return True
    return False


def cells_of(row, bounds):
    """The row's cells, however it is laid out."""
    if not overflows(row, bounds):
        out = []
        for i, (start, _) in enumerate(bounds):
            stop = bounds[i + 1][0] if i + 1 < len(bounds) else width(row)
            out.append(between_columns(row, start, stop).strip())
        return out
    parts = re.split(r'\s{2,}', row.strip())
    if row.startswith("  ") and len(parts) < len(bounds):
        parts = [""] + parts
    return (parts + [""] * len(bounds))[:len(bounds)]


def fix_block(lines, first, last):
    """Re-lay one table.  ``first``/``last`` index its opening and closing rule."""
    bounds = columns(lines[first])
    indent = len(lines[first]) - len(lines[first].lstrip())
    rows = [cells_of(lines[i], bounds) for i in range(first + 1, last)
            if not RULE.match(lines[i])]
    if not any(overflows(lines[i], bounds) for i in range(first + 1, last)):
        return None

    widths = [max((width(r[c]) for r in rows), default=0) for c in range(len(bounds))]
    rule = " " * indent + "  ".join("=" * max(w, 1) for w in widths)

    out, r = [rule], 0
    for i in range(first + 1, last):
        if RULE.match(lines[i]):
            out.append(rule)
            continue
        cells = rows[r]
        r += 1
        line = " " * indent + "  ".join(
            cell + " " * (widths[c] - width(cell)) for c, cell in enumerate(cells))
        out.append(line.rstrip())
    out.append(rule)
    return out


def process(text):
    lines = text.splitlines()
    marks = [i for i, l in enumerate(lines) if RULE.match(l)]
    fixed = 0

    # A simple table runs from its first rule to its last.  Consecutive rules belong to the
    # same table as long as no blank line separates them -- a blank line ends the table.
    blocks, i = [], 0
    while i < len(marks) - 1:
        j = i
        while (j + 1 < len(marks)
               and not any(not lines[k].strip()
                           for k in range(marks[j] + 1, marks[j + 1]))):
            j += 1
        if j > i:
            blocks.append((marks[i], marks[j]))
        i = j + 1

    for start, end in reversed(blocks):
        replacement = fix_block(lines, start, end)
        if replacement:
            lines[start:end + 1] = replacement
            fixed += 1
    return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), fixed


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/uslib")

    total = collections.Counter()
    for path in sorted((library / "products").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new, n = process(text)
        if n:
            total[str(path)] = n
            if not dry:
                path.write_text(new, encoding="utf-8")
    for path, n in total.items():
        print(f"  {n}  {path}")
    print(f"\n{sum(total.values())} tables re-laid{' (dry run)' if dry else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
