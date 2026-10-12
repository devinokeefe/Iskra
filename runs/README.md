# Records of the runs

This folder holds what the scripts printed. The table says which record belongs to which claim.

| Claim, and where it is made | Record |
|---|---|
| The figures, tables and readings of the four pages and of this one that the check compares with the data or with the records of the search below, and the controls (`python check.py`) | `check.txt` |
| The page on document 449: the run of pairs at the end and the seven footnoted names, deciphered under both counts | `doc449.txt` |
| The page on Bauman's key: every group with the poem's reading beside the printed one, the totals, the cells and the controls | `bauman.txt` |
| The page on document 15: the key lines, the table and the letters that the pairs give | `doc15.txt` |
| The page on document 15: the collection of verse cut from the Wikisource dump (91,128 blocks) | `make_corpus.txt` |
| The page on document 15: the search over other texts (54,311 blocks of thirteen lines or more, 1,565,962 start lines in the reading's own convention, 9 of 18 at best for any other text) | `corpus_control.txt` |
| `tests/TESTS.md`, the mutation test | `mutation_test.txt` |

Each record holds what the script printed on standard output, with LF line ends. The workflow in `.github/`
runs every script except the two of the search over other texts, and compares what they print with these
records.

The search needs two files that are not in the repository. The first is the Russian Wikisource dump
`ruwikisource-20261001-pages-articles.xml.bz2` (SHA-1 `cfb9d1bd902026a339f719b79e6c3b84f2a8cdb4`, as
Wikimedia lists it), from <https://dumps.wikimedia.org/ruwikisource/>, which keeps each dump for a limited
time. The second is the collection of verse that

    python doc15/code/make_corpus.py ruwikisource-20261001-pages-articles.xml.bz2 ws_poems.jsonl

cuts from it: 91,128 blocks of verse, one to a line, in a file of 166,149,032 bytes with the SHA-256
`c92003581279c68d2043fa395d5ab2d68673b7983f14a8502ab44eaccce7f835`. Then

    python doc15/code/corpus_control.py ws_poems.jsonl

prints `corpus_control.txt`. The pages of Tan's translation are among the blocks, and the record lists them
at the top.

The looser search that first found the key has no record here; the
limits of [the page for document 15](../doc15/README.md#limits) give the reason.
