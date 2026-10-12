"""Read the number pairs of Iskra document no. 449 with Martov's hymn as the key.

    python code/decode.py            the run of pairs at the end and the seven footnoted names, under both counts
    python code/decode.py --check    all checks; exit status 0 only if every one passes

A pair a.b is line a, letter b. Only letters are counted, and the hard sign counts as a letter.
There are two ways of counting the lines, both starting from the second printed line:

    print        every line as the journal prints it
    lepeshinsky  the same, but "Тише впередъ, / Рабочій народъ!" taken as one line; the end of the
                 third refrain, "Шествуй впередъ, / Рабочій народъ!", is joined in the same way

The checks also read README.md in this folder, the README.md of the repository and runs/README.md, and
test that the figures, tables and readings that the checks name are the ones computed here.  Standard
library only.
"""

import io
import os
import re
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PAGE = os.path.join(ROOT, "README.md")
FRONT = os.path.join(ROOT, "..", "README.md")
UNITS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
]  # fmt: skip
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return [s.rstrip("\n") for s in f if s.strip() and not s.startswith("#")]


def hymn_text():
    """The printed lines of the key as they stand in data/hymn.txt."""
    return [s.strip() for s in rows("hymn.txt")]


def letters(text):
    return "".join(ch for ch in text.lower() if ch.isalpha())


def hymn():
    """The printed lines of the key, letters only, lower case."""
    return [letters(s) for s in hymn_text()]


FIRST = 2  # the printed line that is line 1 of the key


def key_lines(count, first=FIRST, ring=False):
    """The lines of the key as numbered under one way of counting; first = printed line taken as line 1.
    With ring, the lines before it follow the last, so that a count past the end goes on from the top."""
    printed = hymn()
    if count == "lepeshinsky":
        joined = []
        for s in printed:
            if s == "рабочійнародъ" and joined and joined[-1].endswith("впередъ"):
                joined[-1] += s
            else:
                joined.append(s)
        printed = joined
    return printed[first - 1 :] + (printed[: first - 1] if ring else [])


def fold(text):
    """Old and new spelling of the same letter count as equal."""
    return text.lower().replace("ѣ", "е").replace("і", "и")


def decode(tokens, lines):
    """One character for each token: the letter, the clear token itself, or ? if there is no such letter."""
    out = []
    for t in tokens:
        if "." not in t:
            out.append(t)
            continue
        a, b = (int(x) for x in t.split("."))
        if 1 <= a <= len(lines) and 1 <= b <= len(lines[a - 1]):
            out.append(lines[a - 1][b - 1])
        else:
            out.append("?")
    return out


def units(expected, tokens):
    """Split the expected string into one unit for each token (clear tokens stand for themselves)."""
    out, i = [], 0
    for t in tokens:
        n = 1 if "." in t else len(t)
        out.append(expected[i : i + n])
        i += n
    if i != len(expected):
        raise ValueError("expected letters and tokens do not match: %s" % expected)
    return out


def load():
    items = []
    for s in rows("pairs.tsv")[1:]:
        ident, _page, word, expected, tokens = s.split("\t")
        tokens = tokens.split()
        items.append((ident, word, units(expected, tokens), tokens))
    return items


def score(items, lines, run):
    """(pairs that give the expected letter, pairs compared) over the run at the end (run=True) or the names."""
    good = total = 0
    for ident, _word, exp, tokens in items:
        if (ident == "RUN") != run:
            continue
        got = decode(tokens, lines)
        for e, g, t in zip(exp, got, tokens, strict=True):
            if "." in t and e != "*":
                total += 1
                good += fold(g) == fold(e)
    return good, total


def shifts():
    """For each line of Lepeshinsky's count, how many lines further on the same line is in the print count."""
    printed, out, k = hymn()[1:], [], 0
    for s in key_lines("lepeshinsky"):
        out.append(k - len(out))
        k += 1 if s in printed else 2
    return out


def prose(path):
    with open(path, encoding="utf-8") as f:
        return " ".join(f.read().split())


def block_after(path, marker):
    """The lines of the first fenced block after the line that contains marker."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    i = next(k for k, s in enumerate(lines) if marker in s)
    start = next(k for k in range(i, len(lines)) if lines[k].startswith("```"))
    end = next(k for k in range(start + 1, len(lines)) if lines[k].startswith("```"))
    return [s for s in lines[start + 1 : end] if s.strip()]


def table_rows(path, first_cell_pattern):
    with open(path, encoding="utf-8") as f:
        found = [s.strip() for s in f if s.startswith("|")]
    return [[c.strip() for c in s.strip("|").split("|")] for s in found if re.match(first_cell_pattern, s[1:].strip())]


ORDINALS = [
    "",
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "ninth",
    "tenth",
    "eleventh",
    "twelfth",
    "thirteenth",
    "fourteenth",
    "fifteenth",
    "sixteenth",
]


def word(n):
    """A number from 0 to 99 in words."""
    return UNITS[n] if n < 20 else TENS[n // 10] + ("-" + UNITS[n % 10] if n % 10 else "")


def check():
    items = load()
    pr, le = key_lines("print"), key_lines("lepeshinsky")
    tokens = next(t for ident, _w, _e, t in items if ident == "RUN")
    pairs = [t for t in tokens if "." in t]
    clear = [t for t in tokens if "." not in t]
    words = [i for i in items if i[0] != "RUN"]
    word_pairs = sum(1 for i in words for t in i[3] if "." in t)
    spare = sum(1 for i in words for e, t in zip(i[2], i[3], strict=True) if "." in t and e == "*")
    results = []
    page, front = prose(PAGE), prose(FRONT)

    def ok(name, cond):
        results.append((name, bool(cond)))

    def says(path, text, phrase):
        ok("%s says: %s" % ("README.md" if path == FRONT else "doc449/README.md", phrase), phrase in text)

    ok(
        "the key has 36 printed lines, and the refrain is printed three times as four lines",
        len(hymn()) == 36 and len(le) == len(pr) - 3,
    )
    ok("the key has no letter ф", not any("ф" in s for s in hymn()))
    ok(
        "the run at the end has 40 pairs and three tokens in clear (Ф, the dash, 30)",
        (len(tokens), len(pairs), clear) == (43, 40, ["Ф", "—", "30"]),
    )
    got = [fold(x) for x in decode(tokens, pr)]
    address = "".join(got[2:])
    ok("the run, print count: no pair points outside the key", "?" not in got)
    g, n = score(items, pr, run=True)
    ok("the run, print count: all %d pairs after the first two give the address" % n, g == n == 38)
    first = [[fold(x) for x in decode(tokens[:2], lines)] for lines in (pr, le)]
    ok(
        "the first two pairs of the run, 10.2 and 2.2, give и and а under both counts",
        tokens[:2] == ["10.2", "2.2"] and first == [["и", "а"]] * 2,
    )
    g, n = score(items, le, run=False)
    ok("footnoted names, Lepeshinsky's count: all %d pairs give the printed names" % n, g == n == 38)
    left = [g for i in words for e, g, t in zip(i[2], decode(i[3], le), i[3], strict=True) if e == "*"]
    ok(
        "the spare pairs in the footnoted names give ъ or point past the end of a line",
        left and all(x in ("ъ", "?") for x in left),
    )
    run_le, run_n = score(items, le, run=True)
    words_pr, words_n = score(items, pr, run=False)
    ok("the run, Lepeshinsky's count: 19 of 38; got %d of %d" % (run_le, run_n), (run_le, run_n) == (19, 38))
    ok("footnoted names, print count: 24 of 38; got %d of %d" % (words_pr, words_n), (words_pr, words_n) == (24, 38))
    other = {
        s: score(items, key_lines("print", s, ring=True), run=True)[0] for s in range(1, len(hymn()) + 1) if s != 2
    }
    best = max(other.values())
    best_at = [s for s, v in other.items() if v == best]
    ok(
        "control: the run counted from each of the 35 other printed lines gives at most 8 of 38, from line 18; "
        "got %d from %s" % (best, best_at),
        len(other) == 35 and best == 8 and best_at == [18],
    )
    deepest = max(int(t.split(".")[0]) for i in items for t in i[3] if "." in t)
    ok(
        "no pair reaches the end of the third refrain, so joining it changes nothing (deepest line %d of %d)"
        % (deepest, len(le)),
        deepest < len(le),
    )
    sh = shifts()
    ok(
        "the two counts part company from line 11, by one line and after the second refrain by two",
        sh.index(1) + 1 == 11 and max(sh) == 2 and sorted(set(sh)) == [0, 1, 2],
    )

    # the pages
    quote = "Якоб Рихтер, Холфорд-сквер 30, Пентонвил, Лондон В. С."
    ok(
        "the address as quoted is what the closing run gives",
        re.sub(r"[^а-я0-9]", "", quote.lower()) == re.sub(r"[^а-я0-9]", "", address),
    )
    for path, text in ((PAGE, page), (FRONT, front)):
        says(path, text, "> " + quote)
    rows4 = table_rows(PAGE, r"\d+\.\d+ \|")
    ok("the table of the name has four rows", len(rows4) == 4)
    for pair, line, letter in rows4:
        a, b = (int(x) for x in pair.split("."))
        mark = line.index("[")
        ok(
            "table row %s: the line is line %d counted from the second, letter %d is the one in brackets, %s"
            % (pair, a, b, letter),
            line.replace("[", "").replace("]", "") == hymn_text()[a]
            and len(letters(line[:mark])) == b - 1
            and line[mark + 1 : mark + 3] == letter + "]"
            and fold(decode([pair], pr)[0]) == letter,
        )
    ok(
        "the table takes the pairs of the run that follow the first two and reads the first word of the address",
        [r[0] for r in rows4] == tokens[2 : 2 + len(rows4)]
        and "".join(r[2] for r in rows4) == quote.split(maxsplit=1)[0].lower(),
    )
    says(PAGE, page, "The table reads the first word pair by pair")
    block = [s.split() for s in block_after(PAGE, "40 pairs follows in order")]
    shown_pairs = [t for s in block[0::2] for t in s if t != "|"]
    shown_letters = [t for s in block[1::2] for t in s if t != "|"]
    ok("the block of all the pairs prints the run as in the data", shown_pairs == tokens)
    ok("the block of all the pairs prints the letters that the run gives", [fold(x) for x in shown_letters] == got)
    says(PAGE, page, "The whole run of %d pairs follows in order" % len(pairs))
    says(PAGE, page, "The %d pairs after the first two give the address letter for letter." % (len(pairs) - 2))
    says(
        PAGE,
        page,
        "Sinelnikov's count of %d for this passage evidently includes those %s." % (len(tokens), word(len(clear))),
    )
    says(
        PAGE,
        page,
        "the %s names in this letter that Krupskaya deciphered at the time all read correctly: %d of their %d "
        "pairs give the letters, and the other %s are spare"
        % (word(len(words)), word_pairs - spare, word_pairs, word(spare)),
    )
    says(
        PAGE,
        page,
        "From line %d onwards the two counts differ by %s line, and after the second refrain by %s"
        % (sh.index(1) + 1, word(1), word(max(sh))),
    )
    says(
        PAGE,
        page,
        "| | the %s names (%d pairs) | the address (%d pairs) |" % (word(len(words)), word_pairs - spare, run_n),
    )
    says(PAGE, page, "| lines as Lepeshinsky counted them | %d right | %d right |" % (word_pairs - spare, run_le))
    says(PAGE, page, "| lines as printed in *Zarya* | %d right | %d right |" % (words_pr, run_n))
    says(
        PAGE,
        page,
        "The run of pairs has %d, and its first two belong to no word of the address and are not counted." % len(pairs),
    )
    says(
        PAGE,
        page,
        "As a control it also counts from each of the other %d printed lines of the hymn as line 1, going on "
        "from the first line where the count runs past the last, and the run then gives at most %d of its %d "
        "letters (from line %d)." % (len(other), best, run_n, best_at[0]),
    )
    says(PAGE, page, "It is a coincidence that both columns have %d pairs." % run_n)
    says(
        PAGE,
        page,
        "The first two pairs, %s and %s, give %s and %s under either count."
        % (tokens[0], tokens[1], first[0][0], first[0][1]),
    )
    says(PAGE, page, "%s in all, which give the hard sign or point past the end of a line" % word(spare))
    says(PAGE, page, "The %s, the dash and the %s are written in clear" % (clear[0], clear[2]))
    # the refrain: the short lines that end with «Рабочій народъ!», and the lines that Lepeshinsky joined
    ht = hymn_text()
    ends = [i for i, s in enumerate(ht) if s.startswith("Рабочій народъ")]
    short = [next(k for k in range(e + 1) if len(ht[e - k].split()) > 2) for e in ends]
    joined = (len(pr) - len(le)) // len(ends) + 1
    ok(
        "the refrain is printed %s times as %s short lines, and Lepeshinsky joined the last %s"
        % (word(len(ends)), word(short[0]), word(joined)),
        len(set(short)) == 1 and len(pr) - len(le) == len(ends),
    )
    says(
        PAGE,
        page,
        "The refrain is printed as %s short lines, and Lepeshinsky took the last %s, «%s / %s», as %s."
        % (word(short[0]), word(joined), ht[ends[0] - 1], ht[ends[0]], word(1)),
    )
    says(PAGE, page, "the refrain is counted as the %s lines that *Zarya* prints" % word(short[0]))
    example = re.search(
        r"a pair such as (\d+)\.(\d+) means the (\w+) letter of the (\w+) line, counting from the (\w+) printed "
        r"line of the poem",
        page,
    )
    ok(
        "the pair that the page explains is a pair of the run, and the page counts it from line %d" % FIRST,
        example
        and "%s.%s" % example.group(1, 2) in tokens
        and example.group(3, 4, 5)
        == (ORDINALS[int(example.group(2))], ORDINALS[int(example.group(1))], ORDINALS[FIRST]),
    )
    says(PAGE, page, "| pair | line of the poem (counted from the %s) | letter |" % ORDINALS[FIRST])
    street = re.search(r"Пентонви(л+),", quote)
    town = re.sub(r"[^А-Я]", "", quote.rsplit("Лондон", 1)[-1])
    says(
        PAGE,
        page,
        "«Пентонвил» has %s л, and W.C. is written as the %s Russian letters %s."
        % (word(len(street.group(1)) if street else 0), word(len(town)), " and ".join(town.upper())),
    )
    runs_page = prose(os.path.join(ROOT, "..", "runs", "README.md"))
    counted = re.findall(r"\b(%s) (?:footnoted )?names\b" % "|".join(UNITS[1:]), " ".join((page, front, runs_page)))
    ok(
        "every count of the footnoted names on the three pages is %s (%d places)" % (word(len(words)), len(counted)),
        len(counted) == 9 and set(counted) == {word(len(words))},
    )
    leman = re.search(
        r"as the key of (\w+) letters between .*? \(vol\. 1, nos ([\d, ]+) and (\d+)\)\. In (\w+) of them, nos "
        r"([\d, ]+) and (\d+), the",
        page,
    )
    named = re.findall(r"\d+", leman.group(2)) + [leman.group(3)] if leman else []
    unnamed = re.findall(r"\d+", leman.group(5)) + [leman.group(6)] if leman else []
    ok(
        "the letters between the board and Leman that the page lists are as many as it says, and so are the three "
        "read without naming the key",
        leman
        and leman.group(1) == word(len(named))
        and leman.group(4) == word(len(unnamed))
        and set(unnamed) < set(named),
    )
    return results


def checked():
    """The results of check(); a check that stops with an error counts as failed."""
    try:
        return check()
    except Exception as error:
        traceback.print_exc()
        return [("the checks stopped with an error (%s: %s)" % (type(error).__name__, error), False)]


def report(results):
    for name, good in results:
        print(("ok    " if good else "FAIL  ") + name)
    n = sum(1 for r in results if r[1])
    print("%d of %d checks passed" % (n, len(results)))
    return 0 if n == len(results) else 1


def main():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return report(checked())
    items = load()
    for count, title in (
        ("print", "Lines counted as printed in the journal"),
        ("lepeshinsky", "Lines counted as Lepeshinsky counted them"),
    ):
        print(title)
        lines = key_lines(count)
        for ident, w, _exp, tokens in items:
            print("%-4s %-26s %s" % (ident, w, " ".join(fold(x) for x in decode(tokens, lines))))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
