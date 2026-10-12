"""Cut the collection of verse texts for corpus_control.py from a Russian Wikisource dump.

Reads the dump of the pages and articles (ruwikisource-YYYYMMDD-pages-articles.xml.bz2, from
https://dumps.wikimedia.org/ruwikisource/) as a stream, keeps the pages of the main namespace and of the
namespace «Страница» (0 and 104), and writes every block of verse found in them as one JSON record per
line: {"t": title, "ns": namespace, "k": kind of block, "lines": [the lines]}.  A block is the text of a
<poem> tag, the text between {{poem-on}} and {{poem-off}}, or the longest parameter of a {{poemx}},
{{poem}} or {{стих}} template.  Templates, links, tags, notes and stress marks are removed from it, and
only lines with a word of two Cyrillic letters or more are kept; a block of fewer than three such lines
is dropped.

runs/README.md identifies the dump and the collection behind runs/corpus_control.txt.

usage: python code/make_corpus.py <dump.xml.bz2> <corpus.jsonl>
"""

import bz2
import html
import json
import re
import sys

POEM_TAG = re.compile(r"<poem[^>]*>(.*?)</poem>", re.S | re.I)
POEM_ON_OFF = re.compile(r"\{\{\s*poem-on[^}]*\}\}(.*?)\{\{\s*poem-off[^}]*\}\}", re.S | re.I)
POEM_TEMPLATE = re.compile(r"\{\{\s*(poemx1?|poem-?x?|стих|poem)\s*\|", re.I)
NOTE = re.compile(r"<ref[^>/]*>.*?</ref>|<ref[^>]*/>", re.S | re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
TAG = re.compile(r"<[^>]+>")
LINK = re.compile(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]")
INNER_TEMPLATE = re.compile(r"\{\{([^{}]*)\}\}")
DROPPED_TEMPLATES = (
    "ref", "примечание", "sidenote", "heading", "заголовок", "cite", "comment", "комментарий", "right",
    "center", "pagenum", "page", "страница",
)  # fmt: skip
STRESS = re.compile("[̀-ͯ]")
WORD = re.compile(r"[а-яА-ЯёѣѢіІ]{2,}")


def template(m):
    """An inner template is replaced by its last parameter, or by nothing."""
    parts = m.group(1).split("|")
    name = parts[0].strip().lower()
    if len(parts) == 1 or any(name.startswith(d) for d in DROPPED_TEMPLATES):
        return ""
    last = parts[-1]
    if "=" in last and len(last.split("=")[0]) < 15:
        last = last.split("=", 1)[1]
    return last


def clean(text):
    text = COMMENT.sub("", text)
    text = NOTE.sub("", text)
    for _ in range(6):
        new = INNER_TEMPLATE.sub(template, text)
        if new == text:
            break
        text = new
    text = LINK.sub(r"\1", text)
    text = TAG.sub("", text)
    text = text.replace("'''", "").replace("''", "")
    return STRESS.sub("", text)


def template_bodies(text):
    """The body of each {{poemx|...}}-like template: the parameter with the most line breaks."""
    out = []
    for m in POEM_TEMPLATE.finditer(text):
        depth, j, last, square, parts = 2, m.end(), m.end(), 0, []
        while j < len(text) and depth > 0:
            two = text[j : j + 2]
            if two == "{{":
                depth += 2
                j += 2
                continue
            if two == "}}":
                depth -= 2
                if depth == 0:
                    parts.append(text[last:j])
                j += 2
                continue
            if two == "[[":
                square += 1
                j += 2
                continue
            if two == "]]":
                square = max(0, square - 1)
                j += 2
                continue
            if text[j] == "|" and depth == 2 and square == 0:
                parts.append(text[last:j])
                last = j + 1
            j += 1
        if parts:
            body = max(parts, key=lambda p: p.count("\n"))
            if body.count("\n") >= 3:
                out.append(body)
    return out


def blocks(text):
    low = text.lower()
    found = []
    if "<poem" in low:
        found += [("poem", b) for b in POEM_TAG.findall(text)]
    if "poem-on" in low:
        found += [("onoff", b) for b in POEM_ON_OFF.findall(text)]
    if "{{poem" in low or "{{стих" in low:
        found += [("poemx", b) for b in template_bodies(text)]
    return found


def pages(path):
    """(title, namespace, wikitext) for every page of the dump."""
    title = ns = None
    buf, in_text = [], False
    with bz2.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            if in_text:
                k = line.find("</text>")
                if k >= 0:
                    buf.append(line[:k])
                    in_text = False
                    yield title, ns, "".join(buf)
                else:
                    buf.append(line)
                continue
            if "<title>" in line:
                m = re.search(r"<title>(.*?)</title>", line)
                title = html.unescape(m.group(1)) if m else None
            elif "<ns>" in line:
                m = re.search(r"<ns>(\d+)</ns>", line)
                ns = int(m.group(1)) if m else None
            elif "<text" in line:
                i = line.find(">", line.find("<text"))
                if line[i - 1] == "/":
                    continue
                rest = line[i + 1 :]
                k = rest.find("</text>")
                if k >= 0:
                    yield title, ns, rest[:k]
                else:
                    buf, in_text = [rest], True


def main(dump, out_path):
    n_pages = n_blocks = 0
    with open(out_path, "w", encoding="utf-8", newline="\n") as out:
        for title, ns, raw in pages(dump):
            n_pages += 1
            if ns not in (0, 104):
                continue
            text = html.unescape(raw)
            for kind, body in blocks(text):
                lines = [x.strip() for x in clean(body).split("\n")]
                lines = [x for x in lines if WORD.search(x)]
                if len(lines) < 3:
                    continue
                record = {"t": title, "ns": ns, "k": kind, "lines": lines}
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                n_blocks += 1
    print("pages: %d; blocks of verse written: %d" % (n_pages, n_blocks))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python code/make_corpus.py <dump.xml.bz2> <corpus.jsonl>")
    sys.stdout.reconfigure(newline="\n")  # LF line ends on every system, as in runs/make_corpus.txt
    main(sys.argv[1], sys.argv[2])
