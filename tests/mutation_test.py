"""Mutation test: deliberate errors in the data, the pages and the scripts, one at a time.

Each mutant changes one place in one file: a pair or a letter copied wrongly, a line of a key poem changed,
a reading given to the wrong person, a figure or a letter changed on a page, or a rule of a script changed
(a letter counted from the wrong place, the refrain counted the other way, a spelling no longer folded).
The script copies the repository once to a
temporary folder, where check.py must pass before any change.  For each mutant it makes the change there, runs
check.py, notes whether it fails and which part fails, and puts the file back.

Some mutants are marked with the reason why the checks are not expected to detect them: four change facts
that the pages quote from their sources (a date, an archival reference, the month of the journal and a
column of the directory), which no computation here can test, and one drops a letter of Tan's translation
that no pair, control or other check reads.  The script prints one line for each mutant and ends with
status 0 only if every unmarked mutant is detected and every marked one is not.

usage: python tests/mutation_test.py      (from any folder)
"""

import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTED = "a fact quoted from a source, which no computation here tests"

# (description, file, text, replacement[, reason why it is not expected to be detected]);
# the text must occur exactly once in the file
MUTANTS = [
    # the data
    (
        "doc449, the run: one pair of the name copied wrongly (1.6 as 1.7)",
        "doc449/data/pairs.tsv",
        "10.2 2.2 1.6 2.5",
        "10.2 2.2 1.7 2.5",
    ),
    ("doc449, the run: the clear Ф omitted", "doc449/data/pairs.tsv", "5.4 Ф 17.5", "5.4 17.5"),
    (
        "doc449, footnoted word «Варде»: last pair copied wrongly (8.2 as 8.3)",
        "doc449/data/pairs.tsv",
        "15.1 13.2 14.3 8.3 8.2",
        "15.1 13.2 14.3 8.3 8.3",
    ),
    (
        "doc449, the hymn: the hard sign dropped from «Темныя силы въ загривокъ насъ бьютъ»",
        "doc449/data/hymn.txt",
        "Темныя силы въ загривокъ",
        "Темныя силы в загривокъ",
    ),
    (
        "doc449, the hymn: the first refrain typed with its last two lines as one",
        "doc449/data/hymn.txt",
        "Тише впередъ,\nРабочій народъ!\nЖаждетъ",
        "Тише впередъ, Рабочій народъ!\nЖаждетъ",
    ),
    (
        "bauman, pairs: a pair of «Ляп[унова]» copied wrongly",
        "bauman/data/pairs.tsv",
        "10/6 5/6 5/2 8/1",
        "10/6 5/6 5/3 8/1",
    ),
    (
        "bauman, pairs: «Доноди» given to Krupskaya instead of the compilers",
        "bauman/data/pairs.tsv",
        "compilers\tДоноди",
        "Krupskaya\tДоноди",
    ),
    (
        "bauman, pairs: no. 73 numbered 74 in one group",
        "bauman/data/pairs.tsv",
        "73\t113\tcompilers\tДоноди",
        "74\t113\tcompilers\tДоноди",
    ),
    ("bauman, the poem: «Дѣла» typed «Дала» (row 7)", "bauman/data/poem.txt", "Дѣла до счастья", "Дала до счастья"),
    (
        "bauman, the poem: a line of the second half changed",
        "bauman/data/poem.txt",
        "Тихимъ аккордомъ",
        "Тихимъ акордомъ",
    ),
    (
        "bauman, Sinelnikov's square: one cell copied wrongly",
        "bauman/data/sinelnikov_square.txt",
        "тучкипи.....",
        "тучкиши.....",
    ),
    ("doc15, pairs: pair 30 copied wrongly (4/9 as 4/8)", "doc15/data/pairs.tsv", "30\t4/9", "30\t4/8"),
    ("doc15, pairs: the compilers' letter of pair 5 changed", "doc15/data/pairs.tsv", "5\t3/1\tв", "5\t3/1\tб"),
    (
        "doc15, the poem: one word of line 4 changed",
        "doc15/data/key_negri_tan.txt",
        "И прямо въ душу",
        "И прямо въ сердце",
    ),
    (
        "doc15, the poem: the hard sign dropped from «къ» in line 1",
        "doc15/data/key_negri_tan.txt",
        "вчера къ моей постели\nЯвилась",
        "вчера к моей постели\nЯвилась",
        "no pair or control of document 15 reads beyond the 13th letter of a line",
    ),
    # the pages
    (
        "doc449 page: a figure of the table of the two counts changed",
        "doc449/README.md",
        "| 24 right | 38 right |",
        "| 25 right | 38 right |",
    ),
    (
        "front page: one letter of the address changed",
        "README.md",
        "> Якоб Рихтер, Холфорд-сквер",
        "> Якоб Рихтер, Холфорт-сквер",
    ),
    (
        "doc449 page: one pair in the block of all 40 changed",
        "doc449/README.md",
        "2.4 9.4 16.1 20.2",
        "2.4 9.4 16.1 20.3",
    ),
    (
        "doc449 page: the letter in brackets moved in the table of the name",
        "doc449/README.md",
        "Темны[я] силы",
        "Темн[ы]я силы",
    ),
    (
        "doc449 page: the start line of the best control changed",
        "doc449/README.md",
        "(from line 18)",
        "(from line 19)",
    ),
    (
        "bauman page: the agreement of the poem changed in the table",
        "bauman/README.md",
        "| 516 of 555 (93.0%) |",
        "| 517 of 555 (93.2%) |",
    ),
    ("bauman page: a letter of the square changed", "bauman/README.md", "7   Д  ѣ  л  а  д", "7   Д  а  л  а  д"),
    ("bauman page: a line of the poem changed", "bauman/README.md", "    Блещутъ ихъ очи.", "    Блещетъ ихъ очи."),
    (
        "bauman page: «eleven other places» as «twelve»",
        "bauman/README.md",
        "л in eleven other places",
        "л in twelve other places",
    ),
    ("bauman page: a letter in the table of cells changed", "bauman/README.md", "| 7/3 | л | н |", "| 7/3 | л | и |"),
    ("bauman page: the list of the nine letters changed", "bauman/README.md", "222, 235, 318 and", "222, 235, 313 and"),
    ("bauman page: a slip in «Полтава» misquoted", "bauman/README.md", "19/2 for 13/2", "19/2 for 13/3"),
    ("doc15 page: a letter in the table changed", "doc15/README.md", "| 30 | 4/9 | д |", "| 30 | 4/9 | т |"),
    ("doc15 page: a cell in a note of the table changed", "doc15/README.md", "н at 9/1", "н at 9/2"),
    (
        "doc15 page: the best other text of the search given a score other than its record's",
        "doc15/README.md",
        "the other texts gave 9.",
        "the other texts gave 10.",
    ),
    ("doc15 page: the letters that the pairs give, one changed", "doc15/README.md", "рачъ  иоделло", "рачъ  иодело"),
    (
        "doc15 page: the result of the control changed",
        "doc15/README.md",
        "the pairs give at most 3 of the 18",
        "the pairs give at most 4 of the 18",
    ),
    (
        "doc15 page: the chance of no slip in the name changed",
        "doc15/README.md",
        "the chance is about 0.39",
        "the chance is about 0.40",
    ),
    (
        "bauman page: the agreement in rows 3 to 10 changed",
        "bauman/README.md",
        "where the poem agrees with 64 of",
        "where the poem agrees with 65 of",
    ),
    (
        "doc15 page: the number of trials in the search changed",
        "doc15/README.md",
        "6,806,958 trials",
        "6,806,959 trials",
    ),
    (
        "doc15 page: the chance of no slip with the soft sign changed",
        "doc15/README.md",
        "(about 0.54 if",
        "(about 0.55 if",
    ),
    (
        "bauman page: the disagreements in no. 200 miscounted",
        "bauman/README.md",
        "holds 18 of the 39 disagreements",
        "holds 17 of the 39 disagreements",
    ),
    ("front page: 516 of the 555 as 515", "README.md", "516 of the 555 pairs", "515 of the 555 pairs"),
    ("front page: 16 of the 18 as 17", "README.md", "16 of the 18 letters of that", "17 of the 18 letters of that"),
    (
        "doc449 page: the date of Krupskaya's answer changed",
        "doc449/README.md",
        "Krupskaya answered on 6 June",
        "Krupskaya answered on 7 June",
        QUOTED,
    ),
    (
        "doc449 page: the archival reference changed",
        "doc449/README.md",
        "ед. хр. 769, л. 18 об.",
        "ед. хр. 770, л. 18 об.",
        QUOTED,
    ),
    (
        "bauman page: the month of the journal changed in the sources",
        "bauman/README.md",
        "vol. VI (June 1900), p. 50.",
        "vol. VI (May 1900), p. 50.",
        QUOTED,
    ),
    ("doc15 page: a column of the directory changed", "doc15/README.md", "(cols 833–834)", "(cols 832–834)", QUOTED),
    # the scripts
    (
        "doc449 script: letters counted from 0",
        "doc449/code/decode.py",
        "out.append(lines[a - 1][b - 1])",
        "out.append(lines[a - 1][b % len(lines[a - 1])])",
    ),
    (
        "doc449 script: Lepeshinsky's count the same as the print count",
        "doc449/code/decode.py",
        'if s == "рабочійнародъ" and',
        'if s == "-" and',
    ),
    (
        "doc449 script: ѣ no longer counted as е",
        "doc449/code/decode.py",
        '.replace("ѣ", "е")',
        "",
    ),
    (
        "doc449 script: upper-case letters of the key not lowered",
        "doc449/code/decode.py",
        'return "".join(ch for ch in text.lower() if ch.isalpha())',
        'return "".join(ch for ch in text if ch.isalpha())',
    ),
    ("bauman script: row numbers taken modulo 11", "bauman/code/check.py", "r = (a - 1) % 10", "r = (a - 1) % 11"),
    (
        "bauman script: the twelfth letter used for 11 in place of 12",
        "bauman/code/check.py",
        "c = 11 if (b == 12 and r in twelfth)",
        "c = 11 if (b == 11 and r in twelfth)",
    ),
    ("bauman script: й no longer counted as и", "bauman/code/check.py", '"й": "и", ', ""),
    (
        "bauman script: a hard sign in the reading accepted for any letter",
        "bauman/code/check.py",
        'ok = (x == "ъ") if e == "_"',
        'ok = True if e == "_"',
    ),
    (
        "bauman script: the first group of data/pairs.tsv skipped",
        "bauman/code/check.py",
        'data_lines("pairs.tsv")[1:]',
        'data_lines("pairs.tsv")[2:]',
    ),
    (
        "doc15 script: letters counted from 0",
        "doc15/code/decode.py",
        "return lines[j][b - 1]",
        "return lines[j][b % len(lines[j])]",
    ),
    (
        "doc15 script: hard signs not counted where they should be",
        "doc15/code/decode.py",
        "if not hard_sign:",
        "if hard_sign:",
    ),
    (
        "doc15 script: the control tries only two other start lines",
        "doc15/code/decode.py",
        "start=s, ring=True)[0] for s in range(1, len(lines))}",
        "start=s, ring=True)[0] for s in range(1, 3)}",
    ),
    (
        "doc15 script: only the first ten checks reported",
        "doc15/code/decode.py",
        "    return res\n",
        "    return res[:10]\n",
    ),
]


def run_check(folder):
    """(exit status, names of the parts that failed, whether a part stopped with an error)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, "check.py"],
        cwd=folder,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    parts = [line.split(": ", 1)[1] for line in proc.stdout.splitlines() if line.startswith("FAILED: ")]
    return proc.returncode, parts[0] if parts else "", "Traceback" in proc.stderr


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    wrong = 0
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "repo")
        shutil.copytree(
            ROOT,
            folder,
            ignore=shutil.ignore_patterns(".git", "tests", "__pycache__", ".ruff_cache", ".github", ".venv", "venv"),
        )
        status, _, _ = run_check(folder)
        if status != 0:
            raise SystemExit("mutation_test: the unmodified repository fails its check")
        print("unmodified repository: check.py passes")
        for number, mutant in enumerate(MUTANTS, start=1):
            description, name, old, new = mutant[:4]
            reason = mutant[4] if len(mutant) > 4 else ""
            path = os.path.join(folder, *name.split("/"))
            with open(path, encoding="utf-8", newline="") as handle:
                text = handle.read()
            if "\r\n" in text:  # a copy whose line ends were converted
                old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
            if text.count(old) != 1:
                raise SystemExit(
                    "mutation_test: mutant %d: the text occurs %d times in %s" % (number, text.count(old), name)
                )
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text.replace(old, new))
            status, parts, error = run_check(folder)
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            if status != 0:
                verdict = "detected (%s%s)" % (parts, ", with an error" if error else "")
            else:
                verdict = "NOT DETECTED" + (" (expected: %s)" % reason if reason else "")
            wrong += (status != 0) == bool(reason)
            print("%2d  %s: %s" % (number, description, verdict), flush=True)
    detected = sum(1 for m in MUTANTS if len(m) == 4)
    print(
        "%d of %d mutants detected as expected; %d not detected, as expected"
        % (detected, len(MUTANTS), len(MUTANTS) - detected)
        if not wrong
        else "%d mutants not as expected" % wrong
    )
    return 1 if wrong or not figures_quoted(detected) else 0


def figures_quoted(detected):
    """The figures of this test that README.md and tests/TESTS.md quote are those of the list above."""
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    kinds = {"data": 0, "pages": 0, "scripts": 0}
    for m in MUTANTS:
        kinds["scripts" if m[1].endswith(".py") else "pages" if m[1].endswith(".md") else "data"] += 1
    quoted = sum(1 for m in MUTANTS if len(m) > 4 and m[4] == QUOTED)
    others = len(MUTANTS) - detected
    phrases = [
        ("README.md", "The mutation test makes %d deliberate errors" % len(MUTANTS)),
        ("README.md", "if %d are detected and the other %s are not" % (detected, words[others])),
        ("README.md", "these are %s facts quoted from the sources" % words[quoted]),
        ("tests/TESTS.md", "makes %d deliberate errors there" % len(MUTANTS)),
        (
            "tests/TESTS.md",
            "Of these, %d are in the data, %d on the pages and %d in the scripts."
            % (kinds["data"], kinds["pages"], kinds["scripts"]),
        ),
        ("tests/TESTS.md", "and %s facts quoted from the sources" % words[quoted]),
        ("tests/TESTS.md", "%d of the %d are detected." % (detected, len(MUTANTS))),
        ("tests/TESTS.md", "The %s that are not detected" % words[others]),
    ]
    good = True
    for name, phrase in phrases:
        with open(os.path.join(ROOT, *name.split("/")), encoding="utf-8") as handle:
            if phrase not in " ".join(handle.read().split()):
                print("%s does not say: %s" % (name, phrase))
                good = False
    return good


if __name__ == "__main__":
    sys.exit(main())
