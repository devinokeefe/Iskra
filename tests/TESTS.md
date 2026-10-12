# Tests

    python tests/mutation_test.py

The command can be run from any folder. It copies the repository to a temporary folder and makes 56 deliberate
errors there, one at a time, running `python check.py` after each and putting the file back before the next.
What it printed is in `runs/mutation_test.txt`.

Of these, 15 are in the data, 28 on the pages and 13 in the scripts. In the data a pair is copied wrongly, a
clear token is dropped, a letter of a reading is changed, a reading is put under the wrong person or the wrong
document, a letter or a word of one of the three key poems is changed, a refrain of the hymn is typed with its
last two lines as one, or a cell of Sinelnikov's square is copied wrongly. On the pages the changes touch a
figure, a letter of a reading, a row of a table, a line of the square or of the poem, the result of a control,
a figure of the search over other texts, and four facts quoted from the sources: a date, an archival
reference, the month of the journal and a column of the Moscow directory. In the scripts a letter is counted
from the wrong place, row numbers are taken modulo 11, the twelfth letter goes to the wrong pair, the refrain
is counted the same way under both counts, the letters of a key keep their capitals, a spelling is no longer
folded, a hard sign is accepted for any letter, a line of the data is skipped, hard signs are not counted, a
control tries only two other start lines, and one part reports only its first ten checks.

In all, 51 of the 56 are detected. Some of them stop a script with an error before its checks are complete,
and `check.py` then reports that part as failed. The part that reports only ten checks still ends with status
0, and is caught by the count of checks that `check.py` expects of each part. The five that are not detected
are marked in the list in `mutation_test.py` with the reason, and the script ends with status 0 only if
exactly these five pass unnoticed.

- The checks do not test the four facts quoted from the sources, since they test only the figures, the tables,
  the letters and the readings ([what has been checked](../README.md#what-has-been-checked-and-what-has-not)).
- The hard sign of «къ» in line 1 of Tan's translation lies beyond every letter that the pairs use ([limits of
  document 15](../doc15/README.md#limits)), that the controls try or that another check reads, so dropping it
  changes nothing that is checked.

## What the tests do not reach

- Errors of copying from the edition are beyond the tests, since the pages of the edition are not in the
  repository ([what has been checked](../README.md#what-has-been-checked-and-what-has-not)).
- A change that only weakens a check, such as a comparison that always succeeds, does not show while the data
  and the pages are right. The controls of documents 449 and 15, for example, give the same maxima if a count
  that runs past the last line of the key is dropped instead of going on from the first, so that change would
  pass unnoticed.
- The errors above show that the checks they touch are made; the test does not try an error against every
  check.
