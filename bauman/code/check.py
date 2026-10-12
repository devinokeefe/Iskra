"""Bauman's key: the poem in data/poem.txt against the number pairs printed in «Переписка…», vol. 1.

Rule.  The first ten lines of the poem are the rows of a square, old spelling, word-final ъ counted.  A pair
a/b is the letter in row a, place b.  Both numbers are taken modulo 10 (11 = 1, 23 = 3, 35 = 5, 20 = 10).
The one exception is b = 12 in rows 3 and 8, which is the real twelfth letter of the line (ж and ш, which the
square lacks), as Sinelnikov describes.  Letters are compared in modern spelling: ѣ counts as е, і and й
as и.

data/pairs.tsv gives each printed group of pairs with the letters the 1969 edition prints for it, aligned
pair by pair:  _ = a hard sign that modern print drops,  * = a pair for which the printed word has no
letter.  "compilers" in the column read_by are the compilers of the edition.  A pair printed without its
second number ("6/...") is written 6/? and not compared.  Letters that the writer left in clear inside a group (й, ь)
are not in the file.  data/sinelnikov_square.txt is the square as Sinelnikov prints it.

The checks also read README.md in this folder and the README.md of the repository, and test that the
figures, the square, the poem, the tables and the readings that the checks name are the ones computed here.

usage: python code/check.py            every group, the totals, the cells, the controls
       python code/check.py --check    the checks; exit status 0 only if every one holds
"""

import collections
import io
import os
import re
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
PAGE = os.path.join(HERE, "..", "README.md")
FRONT = os.path.join(HERE, "..", "..", "README.md")
LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюяѣіѳѵ"
FOLD = str.maketrans({"ѣ": "е", "і": "и", "й": "и", "ё": "е", "ѳ": "ф", "ѵ": "и"})
UNITS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
]  # fmt: skip
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
TWELFTH_ROWS = (2, 7)  # rows 3 and 8, counted from 0
SINELNIKOV_TWELFTH_ROWS = (1, 2, 7)  # Sinelnikov's square has a twelfth letter in row 2 as well
SEARCH_ROWS = 2  # the search that found the poem used only the first two rows of Sinelnikov's square

# Every pair that does not give the printed letter: document, pair, the key's letter, the printed letter.
DISAGREEMENTS = """
14 3/9 я а      | 14 2/8 к р      | 14 4/2 л п      | 14 3/21 к н     | 14 8/2 ѣ о
14 3/6 е о      | 14 7/2 ѣ а      | 14 9/4 ъ р      | 14 5/7 л ь      | 24 35/5 и ю
24 5/16 п в     | 24 3/2 а о      | 73 19/2 о а     | 73 8/4 ъ н      | 73 10/9 г ю
73 7/3 л н      | 73 10/9 г и     | 80 6/6 м о      | 80 8/6 а р      | 80 8/7 в а
80 8/7 в а      | 200 3/5 б т     | 200 1/4 з е     | 200 4/3 е р     | 200 2/6 р б
200 2/5 м у     | 200 22/4 у р    | 200 2/59 ѣ с    | 200 2/12 ъ ж    | 200 11/25 д р
200 8/15 р е    | 200 5/10 у к    | 200 10/9 г м    | 200 8/2 ѣ в     | 200 35/4 к т
200 17/21 д н   | 200 8/15 р е    | 200 5/1 т н     | 200 16/3 о м
"""

# Agreement with the square begun at line 2, 3, ... 16 of the poem, the sixteen lines taken as a ring.
SHIFTED = [15, 21, 31, 9, 17, 30, 24, 41, 41, 34, 3, 20, 29, 11, 4]


def data_lines(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return [s.rstrip("\n") for s in f if s.strip() and not s.startswith("#")]


def poem_rows():
    return ["".join(c for c in ln.lower() if c in LETTERS) for ln in data_lines("poem.txt")]


def sinelnikov():
    return data_lines("sinelnikov_square.txt")


def place(a, b, twelfth=TWELFTH_ROWS):
    """(row, column) from 0; twelfth = the rows whose twelfth letter a pair a/12 gives."""
    r = (a - 1) % 10
    c = 11 if (b == 12 and r in twelfth) else (b - 1) % 10
    return r, c


def cell(rows, a, b, twelfth=TWELFTH_ROWS):
    r, c = place(a, b, twelfth)
    return rows[r][c] if c < len(rows[r]) else "."


def items():
    out = []
    for ln in data_lines("pairs.tsv")[1:]:
        doc, page, who, printed, ps, exp = ln.split("\t")
        pp = []
        for p in ps.split():
            a, b = p.split("/")
            pp.append((int(a), None if b == "?" else int(b)))
        if len(pp) != len(exp):
            raise ValueError("%s %s: %d pairs, %d letters" % (doc, printed, len(pp), len(exp)))
        out.append((doc, page, who, printed, pp, exp))
    return out


def score(rows, its, verbose=False, cells=None, twelfth=TWELFTH_ROWS):
    """Returns (pairs with an expected letter, agreeing, hard signs agreeing, list of disagreements)."""
    tot = hit = hard = 0
    bad = []
    for doc, page, who, printed, pp, exp in its:
        dec = ""
        for i, ((a, b), e) in enumerate(zip(pp, exp, strict=True)):
            x = "?" if b is None else cell(rows, a, b, twelfth)
            dec += x
            if b is None or e == "*":
                continue
            tot += 1
            ok = (x == "ъ") if e == "_" else (x.translate(FOLD) == e.translate(FOLD))
            if ok:
                hit += 1
                hard += e == "_"
            else:
                bad.append((doc, page, printed, "%d/%d" % (a, b), x, e, i, who))
            if cells is not None:
                cells[place(a, b, twelfth)][ok] += 1
        if verbose:
            print("doc. %s, p. %s (%s): %s" % (doc, page, who, printed))
            print("    key gives  " + dec)
            print("    printed    " + exp)
    return tot, hit, hard, bad


def word_at(printed, i):
    """The word of a printed reading that holds its letter i (from 0)."""
    for w in re.findall(r"\w+", printed):
        if i < len(w):
            return w
        i -= len(w)
    return None


def kind(doc, printed, pair, i):
    """The heading under which the README lists a disagreement."""
    if doc == "200" and "first copy" in printed and i < 9:
        return "stretch"
    if printed.startswith("Марье"):
        return "Марье"
    if (
        (printed.startswith("Чапышниной") and pair in ("4/2", "3/21", "8/2"))
        or printed.startswith("Доноди")
        or (printed.startswith("Устинью") and pair == "10/9")
        or (printed.endswith("Ветровой") and pair == "5/16")
    ):
        return "compilers"
    if (printed.startswith("Майский") and pair == "35/5") or (printed == "Лепешинского" and pair == "3/2"):
        return "spelling"
    return "single"


def differing_cells(rows, table, cells):
    """(row, place, poem, table, uses agreeing, uses) where the poem differs from Sinelnikov's square or fills it."""
    out = []
    for r in range(10):
        for c in range(12):
            if c == 10 or (c == 11 and r not in TWELFTH_ROWS):
                continue
            s = table[r][c]
            p = rows[r][c] if c < len(rows[r]) else "."
            if s.translate(FOLD) != p.translate(FOLD):
                u = cells.get((r, c), [0, 0])
                out.append((r + 1, c + 1, p, s, u[1], u[0] + u[1]))
    return out


def figures(rows, its):
    """Everything the README quotes, in one dictionary."""
    table = sinelnikov()
    cells = collections.defaultdict(lambda: [0, 0])
    tot, hit, hard, bad = score(rows, its, cells=cells)
    f = {
        "documents": sorted({int(i[0]) for i in its}),
        "groups": len(its),
        "pairs": sum(len(i[4]) for i in its),
        "no second number": sum(1 for i in its for a, b in i[4] if b is None),
        "no letter": collections.Counter(
            i[0] for i in its for (a, b), e in zip(i[4], i[5], strict=True) if e == "*" and b is not None
        ),
        "compared": tot,
        "agree": hit,
        "hard signs": hard,
        "bad": bad,
        "cells": cells,
    }
    filled = [(r, c) for r in range(10) for c in range(10) if table[r][c] != "."]
    used = {(r, c) for r, c in cells if c < 10}
    f["cells used"] = len(used)
    f["table unattested"] = ["%d/%d" % (r + 1, c + 1) for r, c in filled if (r, c) not in used]
    f["table unattested right"] = sum(
        1 for r, c in filled if (r, c) not in used and table[r][c].translate(FOLD) == rows[r][c].translate(FOLD)
    )
    f["used but empty in table"] = ["%d/%d" % (r + 1, c + 1) for r, c in sorted(used) if (r, c) not in filled]
    f["table filled"] = len(filled)
    f["table same"] = sum(1 for r, c in filled if table[r][c].translate(FOLD) == rows[r][c].translate(FOLD))
    # the rows used to find the poem are no test of it
    later = [(r, c) for r, c in filled if r >= SEARCH_ROWS]
    f["later rows filled"] = len(later)
    f["later rows same"] = sum(1 for r, c in later if table[r][c].translate(FOLD) == rows[r][c].translate(FOLD))
    extra = [(r, c) for r in range(10) for c in (10, 11) if table[r][c] != "."]
    f["columns 11-12 filled"] = len(extra)
    f["columns 11-12 same"] = sum(1 for r, c in extra if table[r][c].translate(FOLD) == rows[r][c].translate(FOLD))
    f["table agree"] = score(table, its, twelfth=SINELNIKOV_TWELFTH_ROWS)[1]
    f["twelfth pairs"] = sum(1 for i in its for a, b in i[4] if b == 12 and (a - 1) % 10 in TWELFTH_ROWS)
    f["without twelfth"] = score(rows, its, twelfth=())[1]
    f["above thirty"] = [
        (i[0], a, b, e, cell(rows, a, b))
        for i in its
        for (a, b), e in zip(i[4], i[5], strict=True)
        if b is not None and (a > 30 or b > 30)
    ]
    f["shifted"] = [score(rows[k:] + rows[:k], its)[1] for k in range(1, len(rows))]
    f["no hard signs"] = score([r.replace("ъ", "") for r in rows], its)[1]
    f["kinds"] = collections.Counter(kind(d, pr, pair, i) for d, _, pr, pair, _, _, i, _ in bad)
    f["differing"] = differing_cells(rows, table, cells)
    return f


def group(its, start):
    return next(i for i in its if i[3].startswith(start))


def reading(rows, its, start, pairs=None):
    """The key's letters for the group whose printed reading begins with start (or for the pairs given)."""
    doc, page, who, printed, pp, exp = group(its, start)
    got = "".join("?" if b is None else cell(rows, a, b) for a, b in pp)
    if pairs is None:
        return got
    want = [tuple(int(x) for x in p.split("/")) for p in pairs.split()]
    for j in range(len(pp) - len(want) + 1):
        if pp[j : j + len(want)] == want:
            return got[j : j + len(want)]
    return None


def prose(path):
    with open(path, encoding="utf-8") as f:
        return " ".join(f.read().split())


def page_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def section(path, heading):
    """The lines of one section of a page, from its heading to the next heading."""
    lines = page_lines(path)
    i = lines.index(heading)
    end = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("#")), len(lines))
    return lines[i + 1 : end]


def word(n, capital=False):
    """A number from 0 to 99 in words."""
    w = UNITS[n] if n < 20 else TENS[n // 10] + ("-" + UNITS[n % 10] if n % 10 else "")
    return w.capitalize() if capital else w


def uses(rows, its, r, c):
    """Every use of cell r/c (from 1): (document, printed reading, whose, place in the group, letter wanted,
    letter of the poem, length of the group)."""
    out = []
    for doc, _page, who, printed, pp, exp in its:
        for i, ((a, b), e) in enumerate(zip(pp, exp, strict=True)):
            if b is not None and place(a, b) == (r - 1, c - 1):
                out.append((doc, printed, who, i, e, cell(rows, a, b), len(exp)))
    return out


def listing(names):
    return ", ".join(names[:-1]) + " and " + names[-1]


def check():
    rows = poem_rows()
    its = items()
    table = sinelnikov()
    f = figures(rows, its)
    res = []
    page, front = prose(PAGE), prose(FRONT)

    def ok(name, cond):
        res.append((name, bool(cond)))

    def says(text, phrase, front_page=False):
        ok("%s says: %s" % ("README.md" if front_page else "bauman/README.md", phrase), phrase in text)

    ok(
        "the poem has 16 lines and each of the first ten has at least ten letters",
        len(rows) == 16 and all(len(r) >= 10 for r in rows[:10]),
    )
    ok("Sinelnikov's square as transcribed has ten rows of twelve columns", [len(r) for r in table] == [12] * 10)
    ok(
        "the square has no ж, ш or ю; lines 3 and 8 have ж and ш as twelfth letters",
        not set("жшю") & set("".join(r[:10] for r in rows[:10])) and rows[2][11] == "ж" and rows[7][11] == "ш",
    )
    ok("Sinelnikov's twelfth letters for rows 3 and 8 are those of the poem", table[2][11] + table[7][11] == "жш")
    ok("9 documents, 33 groups, 562 pairs", (len(f["documents"]), f["groups"], f["pairs"]) == (9, 33, 562))
    ok(
        "3 pairs printed without a second number, 4 with no letter, 555 compared",
        (f["no second number"], sum(f["no letter"].values()), f["compared"]) == (3, 4, 555),
    )
    ok("the poem gives the printed letter in 516 of 555 (93.0%%); got %d" % f["agree"], f["agree"] == 516)
    ok(
        "Sinelnikov's square: 89 cells filled, 84 the letter of the poem",
        (f["table filled"], f["table same"]) == (89, 84),
    )
    ok(
        "the printed pairs use 81 cells of the square; ten of Sinelnikov's 89 are used by none, nine of them right",
        f["cells used"] == 81 and len(f["table unattested"]) == 10 and f["table unattested right"] == 9,
    )
    ok(
        "rows 3 to 10 of Sinelnikov's square: 69 cells filled, 64 the letter of the poem; rows 1 and 2 are "
        "filled and agree",
        (f["later rows filled"], f["later rows same"]) == (69, 64)
        and f["table filled"] - f["later rows filled"] == f["table same"] - f["later rows same"] == 20,
    )
    ok(
        "columns 11 and 12 of Sinelnikov's square: six letters, four of them the poem's",
        (f["columns 11-12 filled"], f["columns 11-12 same"]) == (6, 4),
    )
    ok(
        "two cells that the pairs use are empty in Sinelnikov's square: 5/10 and 6/7",
        f["used but empty in table"] == ["5/10", "6/7"],
    )
    ok(
        "Sinelnikov's square, read with all its twelfth letters, gives 514 of 555; got %d" % f["table agree"],
        f["table agree"] == 514,
    )
    ok(
        "the square begun at each other line gives at most 41 of 555; got %s" % f["shifted"],
        f["shifted"] == SHIFTED and max(f["shifted"]) == 41,
    )
    ok("without hard signs: 346; got %d" % f["no hard signs"], f["no hard signs"] == 346)
    ok(
        "six pairs use the twelfth letter; without the exception 510",
        (f["twelfth pairs"], f["without twelfth"]) == (6, 510),
    )
    big = f["above thirty"]
    thirties = [x for x in big if max(x[1], x[2]) < 40]
    fifties = [x for x in big if 50 < max(x[1], x[2]) < 60]
    big_right = [x for x in big if x[3].translate(FOLD) == x[4].translate(FOLD)]
    ok(
        "seven pairs have a number above thirty, six in the thirties and one in the fifties; four give the "
        "printed letter, three in no. 14 and one in no. 24",
        (len(big), len(thirties), len(fifties)) == (7, 6, 1) and [x[0] for x in big_right] == ["14", "14", "14", "24"],
    )
    ok(
        "11 = 1, 23 = 3 and 35 = 5, and a pair a/12 gives the twelfth letter only in rows 3 and 8",
        place(11, 23) == place(1, 3)
        and place(35, 35) == place(5, 5)
        and [place(a, 12)[1] for a in range(1, 11)] == [1, 1, 11, 1, 1, 1, 1, 11, 1, 1],
    )
    ok(
        "39 disagreements: 7 in the stretch, 20 single, 2 spelling, 3 in «Марье», 7 in the compilers' readings",
        len(f["bad"]) == 39
        and dict(f["kinds"]) == {"stretch": 7, "single": 20, "spelling": 2, "Марье": 3, "compilers": 7},
    )
    listed = [" ".join(x.split()) for x in DISAGREEMENTS.replace("\n", "|").split("|") if x.strip()]
    ok(
        "the 39 disagreements are the ones listed in this script, pair for pair",
        ["%s %s %s %s" % (b[0], b[3], b[4], b[5]) for b in f["bad"]] == listed,
    )
    compilers = [b for b in f["bad"] if kind(b[0], b[2], b[3], b[6]) == "compilers"]
    ok(
        "every disagreement counted as the compilers' is in a reading that data/pairs.tsv gives to the compilers",
        all(b[7] == "compilers" for b in compilers),
    )
    readings = []
    for b in compilers:
        if b[2] not in readings:
            readings.append(b[2])
    not_only_10_9 = [p for p in readings if any(b[2] == p and b[3] != "10/9" for b in compilers)]
    ok(
        "the compilers' readings with a disagreement: four, and in one of them («Устинью») it is only cell 10/9",
        len(readings) == 4 and [p for p in readings if p not in not_only_10_9] == ["Устинью Яковлевну Топову"],
    )
    by_compilers = [b for b in f["bad"] if b[7] == "compilers"]
    also = [(b[0], b[3], word_at(b[2], b[6])) for b in by_compilers if kind(b[0], b[2], b[3], b[6]) == "single"]
    ok(
        "nine of the 39 disagreements are in readings that data/pairs.tsv gives to the compilers, two of them "
        "single pairs, 2/8 in «Покров» (no. 14) and 8/4 in «магазин» (no. 73); got %d" % len(by_compilers),
        len(by_compilers) == 9 and also == [("14", "2/8", "Покров"), ("73", "8/4", "магазин")],
    )
    says(
        page,
        "%s of the %s single pairs are also in readings made by the compilers, %s in «%s» (no. %s) and %s in «%s» "
        "(no. %s), so %s of the %d fall in such readings."
        % (
            word(len(also), True),
            word(f["kinds"]["single"]),
            also[0][1],
            also[0][2],
            also[0][0],
            also[1][1],
            also[1][2],
            also[1][0],
            word(len(by_compilers)),
            len(f["bad"]),
        ),
    )
    in200 = [b for b in f["bad"] if b[0] == "200"]
    ok(
        "18 of the 39 disagreements are in no. 200: the 7 of the stretch, 6 more in the first copy and 5 in the second",
        len(in200) == 18
        and sum(1 for b in in200 if "first copy" in b[2]) == 13
        and sum(1 for b in in200 if "second copy" in b[2]) == 5,
    )
    says(page, "No. 200 holds %d of the %d disagreements." % (len(in200), len(f["bad"])))
    d = {(r, c): (p, s, a, n) for r, c, p, s, a, n in f["differing"]}
    ok(
        "the poem fills 11 empty cells of the square and differs in 5",
        sum(1 for v in d.values() if v[1] == ".") == 11 and sum(1 for v in d.values() if v[1] != ".") == 5,
    )
    ok(
        "cells 7/2, 7/3, 5/7, 4/5, 10/9, 6/7, 5/10: uses agreeing 3 of 4, 1 of 2, 0 of 1, 0 of 0, 0 of 3, 2 of 2, "
        "0 of 1",
        [d.get(k, (None,) * 4)[2:] for k in ((7, 2), (7, 3), (5, 7), (4, 5), (10, 9), (6, 7), (5, 10))]
        == [(3, 4), (1, 2), (0, 1), (0, 0), (0, 3), (2, 2), (0, 1)],
    )
    c = f["cells"]
    ok(
        "cell 4/2 gives л in 11 other places, 3/1 gives к in 18, 5/6 gives п in 17",
        (c[(3, 1)][1], c[(2, 0)][1], c[(4, 5)][1]) == (11, 18, 17),
    )
    ok(
        "no. 14: the pairs printed for «Чапышниной» give чалышкинѣи, 8/2 is the ninth of them, and 8/9 is о",
        reading(rows, its, "Чапышниной")[:10] == "чалышкинѣи"
        and group(its, "Чапышниной")[4][8] == (8, 2)
        and cell(rows, 8, 9) == "о",
    )
    ok(
        "no. 24: the pairs printed for «Ветровой» give петрово, and 5/19 is в",
        reading(rows, its, "Псков, Завеличье", "5/16 14/3 6/4 8/5 7/6 11/2 6/3") == "петрово"
        and cell(rows, 5, 19) == "в",
    )
    first_two = group(its, "Чапышниной")[4][:10] + group(its, "Псков, Завеличье")[4][-7:]
    ok(
        "every cell of those two readings is the same in Sinelnikov's square as in the poem, in modern spelling",
        all(cell(table, a, b).translate(FOLD) == cell(rows, a, b).translate(FOLD) for a, b in first_two),
    )
    ok("no. 73: the pairs printed for «Доноди» give долод and cell 10/9", reading(rows, its, "Доноди") == "долодг")
    ok("no. 73: Sinelnikov's square gives доноди for the same pairs", reading(table, its, "Доноди") == "доноди")
    ok(
        "no. 222: the letters the compilers bracket in «З[и]наида Павло[в]на» are in the pairs",
        reading(rows, its, "З[и]наида").translate(FOLD) == "зинаидапавловна",
    )
    ok("no. 235: the pairs for «Ляп[унова]» give ляпунов", reading(rows, its, "Ляп[унова]") == "ляпунов")
    who = {g[3].split(",")[0].split(" ")[0]: g[2] for g in its}
    ok(
        "data/pairs.tsv gives «Чапышниной», «Ветровой», «Устинью», «Доноди» and «З[и]наида» to the compilers, "
        "«Ляп[унова]» to Krupskaya and both copies in no. 200 to Blumenfeld",
        [
            who["Чапышниной"],
            group(its, "Псков, Завеличье")[2],
            who["Устинью"],
            who["Доноди"],
            who["З[и]наида"],
            who["Ляп[унова]"],
        ]
        == ["compilers"] * 5 + ["Krupskaya"]
        and [g[2] for g in its if g[0] == "200" and "copy" in g[3]] == ["Blumenfeld"] * 2,
    )
    support = [
        (g[0], a, b, e)
        for g in its
        for (a, b), e in zip(g[4], g[5], strict=True)
        if (a - 1) % 10 == 1 and b in (11, 12) and e in "еж"
    ]
    bis = group(its, "the same address")
    ok(
        "Sinelnikov's е and ж in row 2, where the poem has о and ч: the only pair that would use them is one "
        "2/12 in no. 200, where the second copy has 3/12",
        table[1][10:] == "еж" and rows[1][10:12] == "оч" and support == [("200", 2, 12, "ж")] and (3, 12) in bis[4],
    )

    # the slips named on the page: the pair printed, and a pair that gives the letter wanted
    def slip(word_in, wrong_pair, right_pair, doc=None):
        a, b = (int(x) for x in right_pair.split("/"))
        hits = [x for x in f["bad"] if x[3] == wrong_pair and word_in in x[2] and (doc is None or x[0] == doc)]
        return len(hits) == 1 and cell(rows, a, b).translate(FOLD) == hits[0][5].translate(FOLD)

    ok("19/2 stands where 13/2 gives the letter wanted, in «Полтава» (no. 73)", slip("Полтава", "19/2", "13/2", "73"))
    ok("8/4 stands where 8/1 gives the letter wanted, in «магазин»", slip("магазин", "8/4", "8/1"))
    ok(
        "for the м of «Марковичу», 10/3, the first copy has 10/9 and the second 16/3",
        cell(rows, 10, 3) == "м"
        and slip("first copy", "10/9", "10/3", "200")
        and slip("second copy", "16/3", "10/3", "200"),
    )
    no80 = [x for x in f["bad"] if x[0] == "80"]
    ok(
        "no. 80: four pairs one too high in the second number (6/6, 8/6, 8/7 twice), each one lower giving the "
        "letter wanted",
        [x[3] for x in no80] == ["6/6", "8/6", "8/7", "8/7"]
        and all(slip(x[2], x[3], "%s/%d" % (x[3].split("/")[0], int(x[3].split("/")[1]) - 1), "80") for x in no80[:2])
        and cell(rows, 8, 6).translate(FOLD) == no80[2][5] == no80[3][5],
    )
    spelling = [x for x in f["bad"] if kind(x[0], x[2], x[3], x[6]) == "spelling"]
    respelt = {}
    for x in spelling:
        g = group(its, x[2])
        respelt[x[2].split(" ")[0]] = g[5][: x[6]] + x[4] + g[5][x[6] + 1 :]
    ok(
        "the two of spelling: the key gives лепешинскаго, and the last pair of «Майский листок» gives и for ю",
        respelt.get("Лепешинского") == "лепешинскаго" and respelt.get("Майский", "").endswith("получении"),
    )

    # the pages: the poem, the square, the tables and the figures
    block = [s.strip() for s in section(PAGE, "## The poem") if s.startswith("    ")]
    ok(
        "the poem printed on the page is data/poem.txt, with the signature",
        block[:-1] == [s.strip() for s in data_lines("poem.txt")] and block[-1] == "Л. Медвѣдевъ.",
    )
    square = [s.split() for s in section(PAGE, "## The key") if re.match(r"^ +\d+ +[^\d\s]", s)]
    head = [s.split() for s in section(PAGE, "## The key") if re.match(r"^ +1 +2 +3 ", s)]
    ok(
        "the square printed on the page is the first ten letters of the first ten lines, with ж and ш at 3/12 and 8/12",
        head == [[str(k) for k in range(1, 11)] + ["12"]]
        and [int(s[0]) for s in square] == list(range(1, 11))
        and ["".join(s[1:11]).lower() for s in square] == [r[:10] for r in rows[:10]]
        and [s[11:] for s in square] == [[], [], ["ж"], [], [], [], [], ["ш"], [], []],
    )

    # the table of the cells that the poem adds, row by row
    def use_row(r, col):
        p, s = d[(r, col)][:2]
        return "| %d/%d | %s | %s |" % (r, col, p, "empty" if s == "." else s)

    u72 = uses(rows, its, 7, 2)
    e72 = [u for u in u72 if u[4].translate(FOLD) == "е"]
    a72 = [u for u in u72 if u[4] == "а"]
    ok(
        "cell 7/2: е at the last letter of «на севере» (no. 80) and of «отделение» in both copies (no. 200); а "
        "once, in «Марье» (no. 14)",
        [u[0] for u in e72] == ["80", "200", "200"]
        and e72[0][3] == e72[0][6] - 1
        and e72[0][1] == "на севере"
        and all(group(its, u[1])[5].find("отделение") + 8 == u[3] for u in e72[1:])
        and [(u[0], u[1][:5]) for u in a72] == [("14", "Марье")]
        and len(u72) == 4,
    )
    says(
        page,
        "%s е or ѣ %s times, the last letter of «на сѣверѣ» (no. %s) and of «отдѣленіе» in both copies (no. %s); "
        "а once, in «Марье» (no. %s) |" % (use_row(7, 2), word(len(e72)), e72[0][0], e72[1][0], a72[0][0]),
    )
    u73 = uses(rows, its, 7, 3)
    ok(
        "cell 7/3: л in «листок» (no. 24), н in the compilers' «Доноди» (no. 73)",
        [(u[0], u[4], u[2]) for u in u73]
        == [("24", "л", "cipher written above the clear word"), ("73", "н", "compilers")]
        and "листок" in u73[0][1]
        and u73[1][1] == "Доноди",
    )
    says(
        page,
        "%s л in «листок» (no. %s); н only in the compilers' «Доноди» (no. %s) |"
        % (use_row(7, 3), u73[0][0], u73[1][0]),
    )
    u57 = uses(rows, its, 5, 7)
    ok("cell 5/7: one use, ь in «Марье»", [(u[1][:5], u[4]) for u in u57] == [("Марье", "ь")])
    says(page, "%s once, in «Марье», where the clear word has ь |" % use_row(5, 7))
    u109 = uses(rows, its, 10, 9)
    ok("cell 10/9: no use gives the letter wanted", all(u[4] != u[5] for u in u109))
    says(page, "%s %s times, and г fits none of them (see Limits) |" % (use_row(10, 9), word(len(u109))))
    u67 = uses(rows, its, 6, 7)
    ok(
        "cell 6/7: the hard sign at the end of «Меерсон» in both copies (no. 200)",
        [(u[0], u[4], u[3] == u[6] - 1) for u in u67] == [("200", "_", True)] * 2,
    )
    says(page, "%s the hard sign of «Меерсонъ» in both copies (no. %s) |" % (use_row(6, 7), u67[0][0]))
    u510 = uses(rows, its, 5, 10)
    ok("cell 5/10: one use, in no. 200, where к is wanted", [(u[0], u[4]) for u in u510] == [("200", "к")])
    says(page, "%s once, in no. %s, where к is wanted |" % (use_row(5, 10), u510[0][0]))
    says(
        page,
        "%s of these %s cells are used in the letters, and the table gives their uses."
        % (word(sum(1 for v in d.values() if v[3]), True), word(len(d))),
    )

    says(page, "The square printed in the study has %d of its hundred cells filled" % f["table filled"])
    says(page, "%s of the printed pairs use a twelfth letter." % word(f["twelfth pairs"], capital=True))
    twelves = [(doc, a) for doc, _, _, _, pp, _ in its for a, b in pp if b == 12]
    others = [(doc, a) for doc, a in twelves if (a - 1) % 10 not in TWELFTH_ROWS]
    ok(
        "eight printed pairs have 12 as the second number, and the two outside rows 3 and 8 are 4/12 in no. 73 "
        "and 2/12 in no. 200",
        len(twelves) == 8 and others == [("73", 4), ("200", 2)],
    )
    says(
        page,
        "Two more pairs have 12 as their second number, %s, and are read by the rule of tens as %s."
        % (" and ".join("%d/12 in no. %s" % (a, d) for d, a in others), " and ".join("%d/2" % a for _, a in others)),
    )
    says(
        page,
        "Numbers above thirty occur %s times in the letters, %s in the thirties and %s in the fifties, and %s of "
        "them give the printed letter when read in the same way (%s in no. %s, %s in no. %s)."
        % (
            word(len(big)),
            word(len(thirties)),
            word(len(fifties)),
            word(len(big_right)),
            listing(["%d/%d" % x[1:3] for x in big_right[:3]]),
            big_right[0][0],
            "%d/%d" % big_right[3][1:3],
            big_right[3][0],
        ),
    )
    says(
        page,
        "The poem agrees with %d of the %d cells of Sinelnikov's square, and with %s of the %s letters in its "
        "columns 11 and 12"
        % (
            f["table same"],
            f["table filled"],
            word(f["columns 11-12 same"]),
            word(f["columns 11-12 filled"]),
        ),
    )
    says(
        page,
        "Rows 1 and %d of the square were used to find the poem, so the test lies in rows %d to %d, where the "
        "poem agrees with %d of the %d filled cells."
        % (SEARCH_ROWS, SEARCH_ROWS + 1, len(table), f["later rows same"], f["later rows filled"]),
    )
    says(
        page,
        "prints pairs in this key in %s letters: nos %s."
        % (word(len(f["documents"])), listing([str(x) for x in f["documents"]])),
    )
    says(page, "holds all %d groups, %d pairs" % (f["groups"], f["pairs"]))
    n = f["compared"]
    says(page, "| the poem | %d of %d (%.1f%%) |" % (f["agree"], n, 100.0 * f["agree"] / n))
    says(page, "| Sinelnikov's square | %d of %d |" % (f["table agree"], n))
    says(
        page, "| the square begun at each other line of the poem in turn | at most %d of %d |" % (max(f["shifted"]), n)
    )
    says(page, "| the poem without hard signs | %d of %d |" % (f["no hard signs"], n))
    says(page, "| the poem without the twelfth letters | %d of %d |" % (f["without twelfth"], n))
    nl = f["no letter"]
    says(
        page,
        "%s of the %d pairs are not counted: %s are printed without their second number (such as «6/...»), and %s "
        "have no letter in the printed word (%s in no. 80, %s in «Разоренова» in no. 14)."
        % (
            word(f["no second number"] + sum(nl.values()), capital=True),
            f["pairs"],
            word(f["no second number"]),
            word(sum(nl.values())),
            word(nl["80"]),
            word(nl["14"]),
        ),
    )
    says(page, "including the %s at 2/12" % table[1][11])
    says(page, "the %s lines are taken as a ring" % word(len(rows)))
    says(
        page,
        "The script lists the %d pairs that do not give the printed letter, and they are of five kinds."
        % len(f["bad"]),
    )
    k = f["kinds"]
    stretch = [b[6] + 1 for b in f["bad"] if kind(b[0], b[2], b[3], b[6]) == "stretch"]
    ok("the stretch is pairs 3 to 9 of the first copy, one after another", stretch == list(range(3, 10)))
    says(
        page,
        "%s in a row near the start of the first copy of the address in no. 200 (pairs %d to %d)"
        % (word(k["stretch"]), stretch[0], stretch[-1]),
    )
    says(page, "%s single pairs, several of them one figure away" % word(k["single"]))
    says(page, "19/2 for 13/2 in «Полтава», 8/4 for 8/1 in «магазин»")
    says(page, "the м of «Марковичу», which is 10/3, the first copy in no. 200 has 10/9 and the second 16/3")
    says(
        page,
        "In no. 80 the second number is one too high %s times (6/6, 8/6 and 8/7 twice, where 6/5, 8/5 and 8/6 "
        "give the letters wanted)" % word(len(no80)),
    )
    says(
        page,
        "%s of spelling: the cipher has «%s» and «%s» where the edition prints «Лепешинского» and «получению»"
        % (word(k["spelling"]), respelt["Лепешинского"].capitalize(), respelt["Майский"][-9:]),
    )
    marye = [b for b in f["bad"] if b[2].startswith("Марье")]
    says(
        page,
        "%s of the %s in «Марье» in no. 14 (%s)"
        % (word(k["Марье"]), word(len("Марье")), ", ".join(b[3] for b in marye)),
    )
    ok("the three in «Марье» are among its first five pairs", all(b[6] < 5 for b in marye))
    says(
        page,
        "%s in %s readings made by the compilers, in nos %s. %s of these readings are discussed "
        "[below](#readings-that-the-printed-pairs-do-not-give). In the fourth, «Устинью», the one pair that "
        "disagrees is cell 10/9"
        % (
            word(k["compilers"]),
            word(len(readings)),
            listing(sorted({b[0] for b in compilers}, key=int)),
            word(len(not_only_10_9), True),
        ),
    )
    says(
        page,
        "The printed pairs use %d cells of the square. %s of Sinelnikov's %d are used by no pair (%s)"
        % (
            f["cells used"],
            word(len(f["table unattested"]), capital=True),
            f["table filled"],
            listing(f["table unattested"]),
        ),
    )
    wrong = [x for x in f["table unattested"] if x in ["%d/%d" % (r, c) for r, c, _, s, _, _ in f["differing"]]]
    says(
        page,
        "%s of the %s are right, and the tenth is %s"
        % (word(f["table unattested right"], capital=True), word(len(f["table unattested"])), wrong[0]),
    )
    says(
        page,
        "The poem fills the %s cells left empty in Sinelnikov's square and differs from it in %s."
        % (word(sum(1 for v in d.values() if v[1] == ".")), word(sum(1 for v in d.values() if v[1] != "."))),
    )
    says(
        page,
        "Sinelnikov's square also has %s and %s in columns 11 and 12 of row 2, where the poem has %s and %s "
        "(«ночи»). The only support for them is %s 2/12 in the first copy of no. 200, where the second copy has "
        "3/12." % (table[1][10], table[1][11], rows[1][10], rows[1][11], word(len(support))),
    )
    says(
        page,
        "In %s of them the pairs as printed say something else, leaving aside cell 10/9." % word(len(not_only_10_9)),
    )
    says(page, "Cell 4/2 is л in %s other places and 3/1 is к in %s." % (word(c[(3, 1)][1]), word(c[(2, 0)][1])))
    says(page, "Cell 5/6 is п in %s other places." % word(c[(4, 5)][1]))
    ch = group(its, "Чапышниной")
    says(
        page,
        "The pairs %s give %s"
        % (" ".join("%d/%d" % p for p in ch[4][:10]), " ".join(reading(rows, its, "Чапышниной")[:10])),
    )
    says(page, "«Чалышкиной» if 8/2 is a slip for 8/9, which is %s." % cell(rows, 8, 9))
    vet = group(its, "Псков, Завеличье")
    says(
        page,
        "The pairs %s give %s"
        % (" ".join("%d/%d" % p for p in vet[4][-7:]), " ".join(reading(rows, its, "Псков, Завеличье")[-7:])),
    )
    says(page, "A 5/19 in the manuscript would give %s" % cell(rows, 5, 19))
    for start, what in (
        ("Чапышниной", "Babushkin's address in Pokrov"),
        ("Псков, Завеличье", "the address for callers in Pskov"),
        ("Доноди", "Bauman's address for callers in Moscow"),
    ):
        says(page, "- No. %s, %s" % (group(its, start)[0], what))
    don = group(its, "Доноди")
    says(
        page,
        "The last word is %s, which with the poem is %s, the %s from cell 10/9. Sinelnikov has %s at 7/3 and %s at "
        "10/9, which are the letters «Доноди» needs"
        % (
            " ".join("%d/%d" % p for p in don[4]),
            " ".join(reading(rows, its, "Доноди")),
            cell(rows, 10, 9),
            cell(table, 7, 3),
            cell(table, 10, 9),
        ),
    )
    says(page, "the %s pairs printed with it give ляпунов" % word(len(group(its, "Ляп[унова]")[4])))
    differ = sorted({p for p in don[4] if cell(table, *p) != cell(rows, *p)})
    ok("no. 73: the poem and Sinelnikov's square differ at 7/3 and 10/9 in «Доноди»", differ == [(7, 3), (10, 9)])
    says(page, "so those %s cells of the square probably come from this reading" % word(len(differ)))
    listed = " ".join(" ".join(section(PAGE, "## Readings that the printed pairs do not give")).split())
    listed = [re.search(r"(?:\d+/\d+ )+\d+/\d+", b).group(0).split() for b in listed.split(" - No. ")[1:]]
    same = [
        all(
            cell(table, a, b).translate(FOLD) == cell(rows, a, b).translate(FOLD)
            for a, b in (map(int, x.split("/")) for x in p)
        )
        for p in listed
    ]
    leading = same.index(False) if False in same else len(same)
    ok(
        "the readings listed under those the pairs do not give: the cells of the first %d are the same in both "
        "squares, and the rest differ" % leading,
        len(listed) == len(not_only_10_9) and not any(same[leading:]),
    )
    says(
        page,
        "The first %s need nothing from the poem, because the cells concerned are the same in Sinelnikov's square."
        % word(leading),
    )
    (only,) = sorted(set(SINELNIKOV_TWELFTH_ROWS) - set(TWELFTH_ROWS))
    says(
        page,
        "The other %s, %s %s in row %d, are discussed below."
        % (word(f["columns 11-12 filled"] - f["columns 11-12 same"]), table[only][10], table[only][11], only + 1),
    )
    says(page, "%s letters from that correspondence have passages in his cipher" % word(len(f["documents"]), True))
    copies = re.search(
        r"of the \w+ letters are printed from copies.*?Nos (\d+) and (\d+) are police copies.*?Nos (\d+) "
        r"and (\d+) are copies",
        page,
    )
    ok(
        "the letters printed from copies are as many as the page says, and are among the nine",
        copies and set(copies.groups()) <= {str(x) for x in f["documents"]} and len(set(copies.groups())) == 4,
    )
    says(
        page,
        "%s of the %s letters are printed from copies"
        % (word(len(set(copies.groups())) if copies else 0, True), word(len(f["documents"]))),
    )
    says(page, "at the %s numbers given above" % word(len(f["documents"])))
    says(page, "and the %s letters are those listed there" % word(len(f["documents"])))
    ring = re.search(r"a square begun at line (\d+) goes on from line (\d+) to line (\d+)\.", page)
    ok(
        "the example of the ring: a square begun at that line runs past the last line of the poem and goes on "
        "from line 1",
        ring
        and int(ring.group(1)) + len(table) - 1 > len(rows)
        and (int(ring.group(2)), int(ring.group(3))) == (len(rows), 1),
    )
    says(front, "The search used only rows 1 and %d of the square." % SEARCH_ROWS, True)
    says(page, "for the openings of rows 1 and %d of Sinelnikov's square" % SEARCH_ROWS)
    tenth = [(g[0], g[3], j, len(g[4])) for g in its for j, p in enumerate(g[4]) if p == (10, 9)]
    ok(
        "10/9 is printed three times: once in no. 200, then as the last of six pairs in «Устинью» and the last "
        "pair of «Доноди» in no. 73",
        [(u[0], u[1].split(" ")[0], u[2] + 1, u[3]) for u in tenth]
        == [("73", "Устинью", 6, 21), ("73", "Доноди", 6, 6), ("200", "Петербургский", 66, 81)],
    )
    says(page, "Cell 10/9, %s in the poem, fits none of its %s uses" % (cell(rows, 10, 9), word(len(tenth))))
    says(page, "the last of the %s pairs that the compilers read «Устинью»" % word(tenth[0][2] + 1))
    says(
        page,
        "%s stand over %s, and the poem gives %s"
        % (listing([b[3] for b in marye]), listing([b[5] for b in marye]), listing([b[4] for b in marye])),
    )
    says(front, "Sinelnikov's square has %d of its cells filled" % f["table filled"], True)
    says(
        front,
        "Of the %d filled cells of the other %s rows, %d hold the poem's letter, and the poem supplies the "
        "other %s. Read with the poem, %d of the %d pairs in this key that can be compared give the edition's "
        "reading (%d are printed)"
        % (
            f["later rows filled"],
            word(len(table) - SEARCH_ROWS),
            f["later rows same"],
            word(10 * (len(table) - SEARCH_ROWS) - f["later rows filled"]),
            f["agree"],
            n,
            f["pairs"],
        ),
        True,
    )
    says(
        front,
        "and in %s places the pairs as printed do not give the name that the compilers read."
        % word(len(not_only_10_9)),
        True,
    )
    says(front, "the pairs from %s letters" % word(len(f["documents"])), True)
    side = len(table)
    says(page, "a square, %s lines by %s letters" % (word(side), word(side)))
    says(front, "a square of %s lines by %s letters" % (word(side), word(side)), True)
    says(page, "The first %s lines are the rows of the square" % word(side))
    says(page, "It has %s lines and is signed" % word(len(rows)))
    says(page, "For the third row of the table the %s lines" % word(len(rows)))
    says(front, "%s lines signed Л. Медвѣдевъ" % word(len(rows)), True)
    m = re.search(r"multiple of ten \(([^)]*)\)", page)
    tens = [(int(x), int(y)) for x, y in re.findall(r"(\d+) = (\d+)", m.group(1))] if m else []
    ok(
        "each example of the rule of tens on the page is a number and its remainder: %s" % tens,
        tens and all(x != y and (x - 1) % 10 + 1 == y for x, y in tens),
    )
    r3, r8 = (r + 1 for r in TWELFTH_ROWS)
    says(page, "so %d/12 and %d/12 stand for the real twelfth letters of lines %d and %d" % (r3, r8, r3, r8))
    says(
        page,
        "%s %s in row %d and %s %s in row %d"
        % (table[r3 - 1][10], table[r3 - 1][11], r3, table[r8 - 1][10], table[r8 - 1][11], r8),
    )
    times = {1: "once", 2: "twice"}
    u = uses(rows, its, 10, 9)
    by_doc = collections.Counter(x[0] for x in u)
    ok("cell 10/9 gives the wanted letter at none of its uses", u and all(x[4] != x[5] for x in u))
    says(
        page,
        "Cell 10/9, %s in the poem, fits none of its %s uses: %s in no. 200, where"
        % (cell(rows, 10, 9), word(len(u)), times[by_doc["200"]]),
    )
    says(page, "and %s in no. 73, as the last" % times[by_doc["73"]])
    high = [
        (a, b)
        for doc, _, _, _, pp, exp in its
        for (a, b), e in zip(pp, exp, strict=True)
        if doc == "80"
        and b is not None
        and e not in "*_"
        and cell(rows, a, b).translate(FOLD) != e.translate(FOLD)
        and cell(rows, a, b - 1).translate(FOLD) == e.translate(FOLD)
    ]
    ok("in no. 80 four pairs are one too high in the second number, 8/7 twice", len(high) == 4 and high[2] == high[3])
    says(
        page,
        "In no. 80 the second number is one too high %s times (%s, %s and %s twice, where %s, %s and %s give the "
        "letters wanted)"
        % (
            word(len(high)),
            *("%d/%d" % p for p in high[:3]),
            *("%d/%d" % (a, b - 1) for a, b in high[:3]),
        ),
    )
    says(page, "In no. 80 the second number of %s pairs is one too high." % word(len(high)))
    says(page, "and the count of %d rests on that alignment" % f["agree"])
    cyr = re.compile(r"[а-яёѣіѳѵ]")
    supplied = [
        (doc, printed)
        for doc, _, _, printed, _, exp in its
        if "[" in printed
        and len([c for c in exp if c not in "*_"]) > len(cyr.findall(re.sub(r"\[[^\]]*\]", "", printed.lower())))
    ]
    says(
        page,
        "%s the edition brackets letters that the pairs supply. No. %s is printed «%s»"
        % (times[len(supplied)].capitalize(), *supplied[0]),
    )
    says(page, "In no. %s the name is printed «%s»" % supplied[1])
    return res


def checked():
    """The results of check(); a check that stops with an error counts as failed."""
    try:
        return check()
    except Exception as error:
        traceback.print_exc()
        return [("the checks stopped with an error (%s: %s)" % (type(error).__name__, error), False)]


def main():
    rows = poem_rows()
    its = items()
    score(rows, its, verbose=True)
    f = figures(rows, its)
    print()
    print(
        "documents: %d; groups of pairs: %d; pairs printed: %d (%d printed without a second number, %d with no "
        "letter to compare)"
        % (len(f["documents"]), f["groups"], f["pairs"], f["no second number"], sum(f["no letter"].values()))
    )
    print(
        "pairs compared: %d; the poem gives the printed letter in %d (%.1f%%), %d of them hard signs"
        % (f["compared"], f["agree"], 100.0 * f["agree"] / f["compared"], f["hard signs"])
    )
    print("disagreements (%d):" % len(f["bad"]))
    for doc, page, printed, pair, x, e, i, _who in f["bad"]:
        print(
            "    doc. %s p. %s  %-6s key %s, printed %s   %-8s [%s]"
            % (doc, page, pair, x, e, kind(doc, printed, pair, i), printed[:40])
        )
    used = sorted(f["cells"])
    print(
        "cells of the square in use: %d of 100, plus %s"
        % (f["cells used"], ", ".join("%d/12" % (r + 1) for r, c in used if c == 11))
    )
    print("cells where the poem differs from Sinelnikov's square or fills a gap in it (uses agreeing / uses):")
    for r, c, p, s, a, n in f["differing"]:
        print("    %2d/%-2d poem %s, square %s   %d / %d" % (r, c, p, "empty" if s == "." else s, a, n))
    print(
        "Sinelnikov's square: %d cells filled, %d of them the letter of the poem" % (f["table filled"], f["table same"])
    )
    print("cells of Sinelnikov's square that no printed pair uses: " + ", ".join(f["table unattested"]))
    print("Sinelnikov's square on the same pairs: %d of %d" % (f["table agree"], f["compared"]))
    print(
        "pairs 3/12 and 8/12: %d; without the twelfth-letter exception the poem gives %d of %d"
        % (f["twelfth pairs"], f["without twelfth"], f["compared"])
    )
    print(
        "control, the square begun at line 2 to %d: %s of %d"
        % (len(f["shifted"]) + 1, ", ".join(str(h) for h in f["shifted"]), f["compared"])
    )
    print("control, hard signs not counted: %d of %d" % (f["no hard signs"], f["compared"]))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        results = checked()
        for name, good in results:
            print(("ok    " if good else "FAIL  ") + name)
        passed = sum(1 for r in results if r[1])
        print("%d of %d checks passed" % (passed, len(results)))
        sys.exit(0 if passed == len(results) else 1)
    sys.exit(main())
