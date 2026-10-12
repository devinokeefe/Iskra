"""Document 15: how well does any other text fit the compilers' eighteen letters?

Every text of a line-broken corpus is tried as the key at every start line, with hard signs counted or not and
with the pair read line/letter or letter/line.  The corpus is a JSON-lines file with fields "t" (title) and
"lines" (list of verse lines).  The one used for the figures in the README was cut from the Russian Wikisource
dump by make_corpus.py and is not in the repository.  The check compares the figures of the README with the
record of this script, runs/corpus_control.txt, without repeating the run.

usage: python code/corpus_control.py <corpus.jsonl>
"""

import json
import os
import re
import sys

import decode as D

WORD = re.compile(r"[а-яёѣіѳѵ]+")
FLOOR = 8  # agreements below this are not kept


def norm(line, hard_sign):
    words = WORD.findall(line.lower())
    if not hard_sign:
        words = [w[:-1] if len(w) > 1 and w.endswith("ъ") else w for w in words]
    return "".join(words).translate(D.FOLD)


def main(path):
    rows = [(a, b, ed) for _, a, b, ed in D.pairs() if ed and b is not None]
    amax = max(a for a, _, _ in rows)
    best = {}
    ntext = nstart = 0
    with open(path, encoding="utf-8-sig") as f:
        for number, ln in enumerate(f, 1):
            if not ln.strip():
                continue
            try:
                rec = json.loads(ln)
            except ValueError:
                sys.exit("%s, line %d: not a JSON record" % (path, number))
            lines = rec.get("lines") or []
            if len(lines) < amax:
                continue
            ntext += 1
            for hs in (True, False):
                L = [norm(x, hs) for x in lines]
                for swap in (False, True):
                    cells = [(b, a, ed) for a, b, ed in rows] if swap else rows
                    top = max(a for a, _, _ in cells)
                    for s in range(len(L) - top + 1):
                        if hs and not swap:
                            nstart += 1
                        k = 0
                        for a, b, ed in cells:
                            x = L[s + a - 1]
                            if b <= len(x) and x[b - 1] == ed:
                                k += 1
                        if k >= FLOOR:
                            key = (rec.get("t", "?"), hs, swap)
                            if k > best.get(key, (0, 0))[0]:
                                best[key] = (k, s + 1)
    print("texts tried: %d; start lines tried in the reading's own convention: %d" % (ntext, nstart))
    ranked = sorted(best.items(), key=lambda kv: -kv[1][0])
    for (title, hs, swap), (k, s) in ranked[:12]:
        order = "letter/line" if swap else "line/letter"
        print("  %2d of 18  start line %-4d hard signs %-5s %s  %s" % (k, s, hs, order, title))
    poem = "Полночною порой вчера"
    others = [k for (title, hs, swap), (k, s) in ranked if not title.startswith(poem)]
    if others:
        print("best text other than the pages of this poem: %d of 18" % max(others))
    else:
        print("best text other than the pages of this poem: under %d of 18" % FLOOR)


if __name__ == "__main__":
    D.utf8_stdout()
    if len(sys.argv) != 2:
        sys.exit("usage: python code/corpus_control.py <corpus.jsonl>")
    if not os.path.isfile(sys.argv[1]):
        sys.exit("no such file: %s" % sys.argv[1])
    main(sys.argv[1])
