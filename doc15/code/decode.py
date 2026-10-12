"""Document 15: read the printed pairs with the poem and run the checks.

A pair a/b is letter b of line a.  Letters are counted without spaces and punctuation, in the old spelling,
so the hard sign at the end of a word counts.  Yat is printed as е and і as и in the output.

The checks also read README.md in this folder, the README.md of the repository, runs/README.md and the
records runs/make_corpus.txt and runs/corpus_control.txt.  They test that the figures, the table and the
reading that the checks name are the ones computed here or, where they come from the search, the ones in
those records.

usage: python code/decode.py            the key lines, the table and the reading
       python code/decode.py --check    the checks; exit status 0 only if every one holds
"""

import io
import os
import re
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
PAGE = os.path.join(HERE, "..", "README.md")
FRONT = os.path.join(HERE, "..", "..", "README.md")
FOLD = str.maketrans({"ё": "е", "ѣ": "е", "і": "и", "ѳ": "ф", "ѵ": "и"})
UNITS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
]  # fmt: skip
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def utf8_stdout():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")


def key_lines(hard_sign=True):
    out = []
    with open(os.path.join(DATA, "key_negri_tan.txt"), encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip():
                continue
            words = re.findall(r"[а-яёѣіѳѵ]+", ln.lower())
            if not hard_sign:
                words = [w[:-1] if len(w) > 1 and w.endswith("ъ") else w for w in words]
            out.append("".join(words).translate(FOLD))
    return out


def pairs():
    rows = []
    with open(os.path.join(DATA, "pairs.tsv"), encoding="utf-8") as f:
        for ln in f:
            if ln.startswith(("#", "n\t")) or not ln.strip():
                continue
            n, pair, ed = ([*ln.rstrip("\n").split("\t"), ""])[:3]
            a, b = pair.split("/")
            rows.append((int(n), int(a), None if b == "..." else int(b), ed))
    return rows


def letter(lines, a, b, start=0, swap=False, ring=False):
    """Letter b of line a, counted from line start + 1; with ring, a count that runs past the last line
    goes on from the first."""
    if b is None:
        return None
    if swap:
        a, b = b, a
    j = start + a - 1
    if ring:
        j %= len(lines)
    if 0 <= j < len(lines) and 1 <= b <= len(lines[j]):
        return lines[j][b - 1]
    return "?"


def agreement(lines, rows, **kw):
    """(pairs giving the compilers' letter, pairs that can be tested)."""
    ok = n = 0
    for _, a, b, ed in rows:
        if ed and b is not None:
            n += 1
            ok += letter(lines, a, b, **kw) == ed
    return ok, n


def cells(lines, rows):
    return "".join(letter(lines, a, b) or "." for _, a, b, _ in rows)


def other_starts(lines, rows):
    """Agreement with each other line of the poem taken as line 1, and with the pair read letter/line
    from each line of the poem: two dictionaries, line taken as line 1 -> agreement.  A count that runs
    past the last line goes on from the first, so that every pair is tested from every start."""
    direct = {s + 1: agreement(lines, rows, start=s, ring=True)[0] for s in range(1, len(lines))}
    swapped = {s + 1: agreement(lines, rows, start=s, swap=True, ring=True)[0] for s in range(len(lines))}
    return direct, swapped


def stands_at(lines, a, ch):
    return ["%d/%d" % (a, k + 1) for k in range(len(lines[a - 1])) if lines[a - 1][k] == ch]


def prose(path):
    with open(path, encoding="utf-8") as f:
        return " ".join(f.read().split())


def page_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def word(n, capital=False):
    """A number from 0 to 99 in words."""
    w = UNITS[n] if n < 20 else TENS[n // 10] + ("-" + UNITS[n % 10] if n % 10 else "")
    return w.capitalize() if capital else w


def bracketed(reading):
    """(the letters outside square brackets, the letters inside them), lower case, letters only."""
    out, inside = [], []
    for part in re.split(r"(\[[^\]]*\])", reading):
        target = inside if part.startswith("[") else out
        target.append("".join(c for c in part.lower() if c.isalpha()))
    return "".join(out), "".join(inside)


def check():
    lines, rows = key_lines(True), pairs()
    res = []
    page, front = prose(PAGE), prose(FRONT)

    def ok(name, cond):
        res.append((name, bool(cond)))

    def says(text, phrase, front_page=False):
        ok("%s says: %s" % ("README.md" if front_page else "doc15/README.md", phrase), phrase in text)

    whole = [b for _, _, b, _ in rows if b is not None]
    ok("34 pairs, three of them printed without a second number", (len(rows), len(whole)) == (34, 31))
    ok(
        "every pair points within the first ten letters of one of the first thirteen lines",
        max(a for _, a, _, _ in rows) == 13 and max(whole) == 10,
    )
    got = cells(lines, rows)
    shown = [s.split() for s in page_lines(PAGE) if s.startswith("    моссв")]
    ok(
        "the letters printed on the page are the ones the pairs give; got %s" % got,
        len(shown) == 1 and "".join(shown[0]) == got,
    )
    g, n = agreement(lines, rows)
    ok("16 of the 18 letters of the compilers' reading that can be tested; got %d of %d" % (g, n), (g, n) == (16, 18))
    wrong = [(k, letter(lines, a, b), ed) for k, a, b, ed in rows if ed and b is not None and letter(lines, a, b) != ed]
    ok("the two that differ are pair 4 (с for к) and pair 7 (ы for б)", wrong == [(4, "с", "к"), (7, "ы", "б")])
    differ = {k for k, _, _ in wrong}
    ok(
        "for pairs %s the letter wanted is the next one in the line" % sorted(differ),
        [letter(lines, a, b + 1) for k, a, b, _ in rows if k in differ] == [e for _, _, e in wrong],
    )
    says(page, "In both the letter wanted is the next one in the line")

    # the address as the page prints it: the letters outside the brackets are those of the pairs that give
    # a letter of the address; inside, those that the compilers' reading supplies, and «рный в»
    reading = [s.strip() for s in page_lines(PAGE) if s.startswith("    Мос[")]
    stretch = rows[19:23]
    kept = "".join(
        letter(lines, a, b)
        for k, a, b, ed in rows
        if b is not None and (k, letter(lines, a, b), ed) not in wrong and (k, a, b, ed) not in stretch
    )
    supplied = "".join(r[3] for r in rows if r[2] is None and r[3] and r not in stretch) + "".join(
        e for _, _, e in wrong
    )
    ok(
        "the address printed on the page: the letters outside the brackets are those the pairs give, those "
        "inside are the compilers' letters for pairs 4, 6 and 7, then «рный в» for pairs 20 to 23",
        len(reading) == 1
        and bracketed(reading[0])[0] == kept
        and sorted(bracketed(reading[0])[1]) == sorted(supplied + "рныйв"),
    )
    ok(
        "к stands at 5/9 and 5/3, б at 13/3, а at 2/5, в at 2/2, р at 9/3, н at 9/1, ы at 6/16",
        [letter(lines, a, b) for a, b in ((5, 9), (5, 3), (13, 3), (2, 5), (2, 2), (9, 3), (9, 1), (6, 16))]
        == list("ккбаврны"),
    )
    ok("the last eleven pairs give рачъиоделло", got[23:] == "рачъиоделло")
    direct, swapped = other_starts(lines, rows)
    best = max(direct.values())
    best_at = [s for s, v in direct.items() if v == best]
    ok(
        "the 25 other lines of the poem taken as line 1: at most 3 of 18, from lines 16 and 20; got %d from %s"
        % (best, best_at),
        len(direct) == 25 and best == 3 and best_at == [16, 20],
    )
    ok(
        "the pair read letter/line, from each of the 26 lines: at most 2 of 18; got %d" % max(swapped.values()),
        len(swapped) == 26 and max(swapped.values()) == 2,
    )
    bare = key_lines(False)
    g2, _ = agreement(bare, rows)
    ok(
        "without hard signs: 14 of 18, and the last eleven pairs give рачтиоублло; got %d and %s"
        % (g2, cells(bare, rows)[23:]),
        g2 == 14 and cells(bare, rows)[23:] == "рачтиоублло",
    )
    fixed = {(a, b): (k, ed) for k, a, b, ed in rows if ed and b is not None}
    later = [(k, a, b) for k, a, b, _ in rows[20:] if (a, b) in fixed]
    ok(
        "three cells that the compilers' reading fixes occur again later: 10/2 as pair 22 (first pair 9, й), 4/3 "
        "as pair 24 (pair 16, р) and 4/1 as pair 28 (pair 11, и); got %s" % later,
        later == [(22, 10, 2), (24, 4, 3), (28, 4, 1)]
        and [fixed[p[1:]] for p in later] == [(9, "й"), (16, "р"), (11, "и")]
        and all(letter(lines, a, b) == fixed[(a, b)][1] for _, a, b in later),
    )
    earlier = {(a, b) for _, a, b, _ in rows[:27] if b is not None}
    name = [(a, b) for _, a, b, _ in rows[27:]]
    ok(
        "of the seven pairs of the name, only the first uses a cell that occurs earlier in the passage",
        [p in earlier for p in name] == [True] + [False] * 6,
    )

    # the table on the page, row by row
    table = [
        [c.strip() for c in s.strip().strip("|").split("|")] for s in page_lines(PAGE) if re.match(r"^\| \d+ \|", s)
    ]
    ok("the table has a row for each of the 34 pairs, in order", [int(t[0]) for t in table] == [r[0] for r in rows])
    for (k, a, bb, ed), t in zip(rows, table, strict=False):
        want = [str(k), "%d/%s" % (a, "..." if bb is None else bb), letter(lines, a, bb) or "", ed]
        note = t[4]
        good = t[:4] == want
        for ch, at in re.findall(r"(\S) (?:stands )?at ((?:\d+/\d+(?: and )?)+)", note):
            places = re.findall(r"\d+/\d+", at)
            good = good and all(letter(lines, *map(int, p.split("/"))) == ch for p in places)
            good = good and (bb is not None or all(p.split("/")[0] == str(a) for p in places))
        if bb is None:
            good = good and note.startswith("second number not printed")
        ok("table row %d: %s" % (k, " | ".join(t).rstrip(" |")), good)
    complete = [r for r in rows if r[0] <= 11 and r[2] is not None]
    incomplete = len(rows) - len(whole)
    says(page, "the %d printed pairs give, letter by letter" % len(rows))
    says(
        page,
        "Of the %s letters of the compilers' reading that complete pairs fix, %s agree with the key, and where "
        "the compilers print dots the key gives %s letters" % (word(n), word(g), word(len(got) - 27)),
    )
    says(
        page,
        "%s of those %s pairs are printed in full and can be tested"
        % (word(n, True), word(sum(1 for r in rows if r[3]))),
    )
    ok("pair 9 is the й of «Бойни» (pairs 7 to 11)", "".join(r[3] for r in rows[6:11]) == "бойни")
    says(
        page,
        "%s of the cells that it fixes occur again later in the passage. Pair %d repeats %d/%d, the %s of "
        "«Бойни», and pair %d repeats %d/%d, which is %s where «врачъ» would have it if the word begins at pair "
        "%d. Pair %d, the first of the name, repeats %d/%d, and no other pair of the name uses a cell that "
        "occurs earlier in the passage"
        % (
            word(len(later), True),
            *later[0],
            fixed[later[0][1:]][1],
            *later[1],
            fixed[later[1][1:]][1],
            later[1][0] - 1,
            *later[2],
        ),
    )
    ok("pair 28 is the first pair of the name", later[2][0] == len(rows) - len(name) + 1)
    says(
        page,
        "%s of the %d pairs are printed without a second number, and %s more give a letter that the address "
        "cannot have." % (word(incomplete, True), len(rows), word(len(wrong) + 1)),
    )
    p4 = rows[3]
    also = [p for p in stands_at(lines, p4[1], p4[3]) if p != "%d/%d" % (p4[1], p4[2] + 1)]
    says(
        page,
        "for pair %d it also stands at %s, so a %s misread as %d would explain it as well"
        % (p4[0], also[0], also[0].split("/")[1], p4[2]),
    )
    soft = [x.replace("ь", "") for x in lines]
    moved = [
        (k, letter(lines, a, b), letter(soft, a, b)) for k, a, b, _ in rows if letter(lines, a, b) != letter(soft, a, b)
    ]
    g3, _ = agreement(soft, rows)
    ok(
        "without the soft sign in the count only pair 4 changes, from с to к, and 17 of 18 agree; got %s and %d"
        % (moved, g3),
        moved == [(4, "с", "к")] and g3 == 17,
    )
    says(page, "line 5 begins «Я скорбь!», and without its ь, 5/8 is %s" % letter(soft, 5, 8))
    says(
        page,
        "Leaving the soft sign out of the count changes no other pair of the %d, so pair %d is the only test of "
        "it, and the agreement would be %d of %d." % (len(rows), moved[0][0], g3, n),
    )
    says(page, "The third of the three is pair 21, which gives %s." % got[20])
    says(
        page,
        "Pairs %d to %d stand where the compilers print «р[ный] в», and %s of them are printed incomplete"
        % (stretch[0][0], stretch[-1][0], word(sum(1 for r in stretch if r[2] is None))),
    )
    says(page, "The %s of pair 22 fits the ending of «ветеринарный»." % got[21])
    p20, p23 = rows[19], rows[22]
    ok(
        "pair 20 is printed 9/... and line 9 has р and н; pair 23 is printed 2/... and line 2 has в",
        p20[1:3] == (9, None)
        and stands_at(lines, 9, "р")
        and stands_at(lines, 9, "н")
        and p23[1:3] == (2, None)
        and stands_at(lines, 2, "в"),
    )
    says(page, "Pair 20 can be р or н, since line %d has both, and pair 23 can be в" % p20[1])
    says(page, "If pair 21 was 6/16, which is %s, the four pairs read н %s й в" % ((letter(lines, 6, 16),) * 2))
    says(
        page,
        "without the soft sign in the count, that %s would be %s"
        % (letter(lines, 6, 16), stands_at(soft, 6, letter(lines, 6, 16))[0]),
    )
    says(
        page,
        "Pairs 24 to 34 played no part in finding the key. They give «%s», which completes «врачъ» with its "
        "hard sign, and then «%s»." % (got[23:27], got[27:]),
    )
    says(page, "«%s» is what the last %s pairs give" % (got[27:].capitalize(), word(len(got) - 27)))
    # pair 24 repeats the cell of pair 16; the cells of pairs 25 to 27 are used by no earlier pair
    used = {(a, b) for _, a, b, _ in rows[:23] if b is not None}
    fresh = ["%d/%d" % (a, b) for _, a, b, _ in rows[24:27] if (a, b) not in used]
    ok(
        "pair 24 is 4/3, the cell of pair 16, and pairs 25 to 27 use cells that no earlier pair uses",
        rows[23][1:3] == rows[15][1:3] == (4, 3) and fresh == ["7/5", "1/6", "3/2"],
    )
    says(
        page,
        "Pair 24 is %d/%d, the cell of pair 16, which the search had already fixed as %s, but the other three "
        "letters of «%s» come from cells that no earlier pair uses (%s, %s and %s)."
        % (*rows[23][1:3], got[23], got[23:27], *fresh),
    )
    says(
        page,
        "The pairs use only the first %s letters of the first %s lines of the poem"
        % (word(max(whole)), word(max(a for _, a, _, _ in rows))),
    )
    # the complete pairs before the name, tested against the address: the compilers' letters for pairs 1 to
    # 19, any letter of «рный в» for pairs 20 to 23, and «рачъ» for pairs 24 to 27
    before = [(k, letter(lines, a, b)) for k, a, b, _ in rows[:27] if b is not None]
    want = {k: ed for k, _, _, ed in rows[:19]} | dict(zip(range(24, 28), "рачъ", strict=True))
    misfit = [k for k, ch in before if (ch != want[k] if k in want else ch not in "рныйв")]
    rate = ((len(before) - len(misfit)) / len(before)) ** len(name)
    ok(
        "3 of the 24 complete pairs before the name give a letter that the address cannot have, pairs 4, 7 and "
        "21; got %d of %d, pairs %s" % (len(misfit), len(before), misfit),
        (len(misfit), len(before), misfit) == (3, 24, [4, 7, 21]),
    )
    says(
        page,
        "%s of the %d complete pairs before the name give a letter that the address cannot have (pairs %d, %d "
        "and %d). At that rate the chance is about %.2f that the %s pairs of the name hold no slip"
        % (word(len(misfit), True), len(before), *misfit, rate, word(len(name))),
    )
    says(page, "since the key was chosen to fit %d of those %d pairs" % (n, len(before)))
    soft_misfit = [k for k in misfit if k != moved[0][0]]
    says(
        page,
        "(about %.2f if the soft sign explains pair %d)"
        % (((len(before) - len(soft_misfit)) / len(before)) ** len(name), moved[0][0]),
    )
    says(
        page,
        "«%s», the end of «врачъ», %s of its letters from cells that no earlier pair uses"
        % (got[23:27], word(len(fresh))),
    )
    # the search over other texts: the number of trials follows from the blocks and start lines on the page
    tested = [(a, b) for _, a, b, ed in rows if ed and b is not None]
    down, across = max(a for a, _ in tested), max(b for _, b in tested)
    m = re.search(
        r"Each of the ([\d,]+) blocks of (\w+) lines or more .*? That gives ([\d,]+) start lines with the pair "
        r"read line/letter, and more with the pair read letter/line, which reaches only (\w+) lines down\. "
        r".*? ([\d,]+) trials in all",
        page,
    )
    blocks, starts, trials = (int(m.group(k).replace(",", "")) for k in (1, 3, 5)) if m else (0, 0, 0)
    ok(
        "the search: blocks of %s lines or more, the pair read letter/line reaching %s lines down, and trials = "
        "2 × (start lines + start lines + %d × blocks)" % (word(down), word(across), down - across),
        m is not None
        and (m.group(2), m.group(4)) == (word(down), word(across))
        and trials == 2 * (starts + starts + (down - across) * blocks),
    )
    says(
        page,
        "in some %.1f million trials, many of them repeats, no other text gave more than nine of the eighteen"
        % (trials / 1e6),
    )
    says(
        front,
        "In a strict search over %s blocks of verse from Russian Wikisource it gives" % (m.group(1) if m else "?"),
        True,
    )
    ok("the complete pairs of the first two words: ten, two of them wrong", (len(complete), len(wrong)) == (10, 2))
    says(page, "Tan's translation gave %d of %d" % (g, n))
    says(
        page,
        "Taken from any of the other %d lines, the pairs give at most %d of the %d letters (from lines %d and %d), "
        "and read letter/line at most %d. Without hard signs in the count, %d agree and the last eleven "
        "pairs give «%s»."
        % (len(direct), best, n, best_at[0], best_at[1], max(swapped.values()), g2, cells(bare, rows)[23:]),
    )
    says(front, "it gives %d of the %d letters of that reading that complete pairs fix" % (g, n), True)
    says(
        front,
        "The pairs that the search did not use complete «в%s» and then give «%s»" % (got[23:27], got[27:].capitalize()),
        True,
    )
    says(page, "The size of the search does not account for the %s, which support" % word(g))
    says(
        page,
        "The %s after the bracketed stretch give «%s»"
        % (word(len(rows) - len(name) - stretch[-1][0]), got[stretch[-1][0] : len(rows) - len(name)]),
    )
    says(page, "The %s after them give a word that may be a name" % word(len(name)))
    says(
        page,
        "but %s pairs cannot hold the %s letters «рный в»" % (word(len(stretch)), word(len("рныйв"))),
    )
    says(page, "whether pairs %d, %d and %d are slips of the writer or misprints" % tuple(misfit))
    says(
        page,
        "Beside pairs 1 to %d it gives the letter that the compilers' reading requires" % sum(1 for r in rows if r[3]),
    )
    says(
        page,
        "Pair %d gives %s for the %s of «Москва», and pair %d gives %s for the %s of «Бойни»." % (*wrong[0], *wrong[1]),
    )
    hard = [c for c in fresh if letter(lines, *map(int, c.split("/"))) == "ъ"]
    says(page, "a small one: %s new cells, %s of them a hard sign" % (word(len(fresh)), word(len(hard))))
    vets = re.search(r"The index of the edition names (\w+) veterinarians .*? None of the (\w+) is", page)
    listed = re.findall(r"\b[A-Z]\. [A-Z]\. [A-Z][a-z]+", vets.group(0)) if vets else []
    ok(
        "the veterinarians of the index are as many as the page says (%s)" % ", ".join(listed),
        vets and vets.group(1) == vets.group(2) == word(len(listed)),
    )
    says(page, "None of the %s is the name that the %s pairs give" % (word(len(listed)), word(len(name))))
    says(page, "преждевременно. %d шифрдроби»" % len(rows))
    says(page, "what the %s incomplete pairs and the" % word(incomplete))
    says(page, "of the %s testable pairs gave the compilers' letter" % word(n))
    # the figures of the search, against its records in runs/
    record = os.path.join(HERE, "..", "..", "runs", "%s.txt")
    with open(record % "make_corpus", encoding="utf-8") as f:
        written = int(re.search(r"blocks of verse written: (\d+)", f.read()).group(1))
    with open(record % "corpus_control", encoding="utf-8") as f:
        control = f.read()
    tried, started = (int(x) for x in re.search(r"texts tried: (\d+); start lines .*?: (\d+)", control).groups())
    other, of = (
        int(x) for x in re.search(r"best text other than the pages of this poem: (\d+) of (\d+)", control).groups()
    )
    tan = "Полночною порой вчера к моей постели (Негри; Богораз)"
    tops = re.findall(r"(?m)^ *(\d+) of (\d+) .*?  (%s\S*)$" % re.escape(tan), control)
    best_of = {t: max(int(s) for s, _n, u in tops if u == t) for _s, _n, t in tops}
    old, modern = best_of.get(tan + "/ДО"), best_of.get(tan)
    ok(
        "the record of the search gives %s of %d to Tan's translation in the old spelling, %s to the modern one, "
        "and %d to the best other text" % (old, of, modern, other),
        len(best_of) == 2 and old == g and of == n,
    )
    says(page, f"which `code/corpus_control.py` makes over {written:,} blocks")
    says(page, f"Each of the {tried:,} blocks of")
    says(page, f"That gives {started:,} start lines with the pair read line/letter")
    says(page, "Tan's translation gave %d of %d, and the best of the other texts gave %d." % (g, n, other))
    says(page, "modern spelling, without hard signs, gives %s of the %d." % (modern, n))
    says(page, "so its 17 of %d cannot be repeated from these files" % n)
    says(page, "with that freedom Tan's translation gave 17 of the %d." % n)
    says(page, "no other text gave more than %s of the %s" % (word(other), word(n)))
    says(front, f"over {tried:,} blocks of verse from Russian Wikisource", True)
    says(front, "and no other text gives more than %d." % other, True)
    with open(os.path.join(HERE, "..", "..", "runs", "README.md"), encoding="utf-8") as f:
        runs_page = " ".join(f.read().split())
    for phrase in (
        f"the collection of verse cut from the Wikisource dump ({written:,} blocks)",
        f"({tried:,} blocks of thirteen lines or more, {started:,} start lines in the reading's own convention, "
        f"{other} of {of} at best for any other text)",
        f"cuts from it: {written:,} blocks of verse",
    ):
        ok("runs/README.md says: " + phrase, phrase in runs_page)
    return res


def checked():
    """The results of check(); a check that stops with an error counts as failed."""
    try:
        return check()
    except Exception as error:
        traceback.print_exc()
        return [("the checks stopped with an error (%s: %s)" % (type(error).__name__, error), False)]


def show():
    lines, rows = key_lines(True), pairs()
    print("key lines 1-13 (letters only):")
    for i, s in enumerate(lines[:13], 1):
        print("  %2d  %s" % (i, s))
    print("\n  n  pair   letter  compilers note")
    for n, a, b, ed in rows:
        ch = letter(lines, a, b)
        note = ""
        if b is None:
            at = stands_at(lines, a, ed) if ed else []
            note = "second number not printed" + ("; %s stands at %s" % (ed, ", ".join(at)) if at else "")
            ch = "."
        elif ed and ch != ed:
            note = "differs; %s stands at %s" % (ed, ", ".join(stands_at(lines, a, ed)))
        print((" %2d  %-6s %-7s %-8s  %s" % (n, "%d/%s" % (a, b if b else "..."), ch, ed, note)).rstrip())
    text = cells(lines, rows)
    print(
        "\ncells as decoded: %s | %s | %s | %s | %s | %s"
        % (text[:6], text[6:11], text[11:19], text[19:23], text[23:27], text[27:])
    )
    return 0


if __name__ == "__main__":
    utf8_stdout()
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        results = checked()
        for name, good in results:
            print(("ok    " if good else "FAIL  ") + name)
        passed = sum(1 for r in results if r[1])
        print("%d of %d checks passed" % (passed, len(results)))
        sys.exit(0 if passed == len(results) else 1)
    sys.exit(show())
