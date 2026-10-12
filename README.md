# An address and two key poems: the Iskra cipher correspondence, 1901–1902

Devin O'Keefe, October 2026. Not peer-reviewed.

*Iskra*, the newspaper that Lenin, Martov and others edited abroad from the end of 1900, was smuggled into
Russia, and its editorial board and its agents there wrote to one another partly in cipher. The usual key was
a poem agreed in advance, in which a pair of numbers picked out a line and a letter. The Soviet edition of the
correspondence (Moscow, 1969–1970) prints the cipher passages as number pairs, with a reading wherever a
decipherment of the time survived or its compilers could supply one. A. V. Sinelnikov's study of the
revolutionaries' ciphers ends with lists of the keys that have been identified and of the letters and keys
that remain unsolved, and each of the three results here begins from an entry in those lists.

## The address in document 449

A letter that Panteleimon Lepeshinsky sent from Pskov in 1902 ends, in the edition, with three lines of number
pairs that have no reading and that Sinelnikov lists as unread. Deciphered with Martov's "Hymn of the Newest
Russian Socialist", the poem in which Lepeshinsky enciphered seven names elsewhere in the letter, they read

> Якоб Рихтер, Холфорд-сквер 30, Пентонвил, Лондон В. С.

Lenin and Krupskaya lived in London under that name and at that address. The pairs follow the hymn as the
journal prints it, while Lepeshinsky's seven names follow a count of his own, and Krupskaya's reply as printed
announces «Наш личный адрес» ("our personal address") without giving it. [doc449](doc449/README.md) suggests
from this that the pairs were enciphered in London for that reply.

## Bauman's key

Nikolai Bauman, the paper's agent in Moscow in 1901, enciphered with a poem arranged in a square of ten lines
by ten letters. Sinelnikov's square has 89 of its cells filled, and the poem had not been identified. It was
printed, sixteen lines signed Л. Медвѣдевъ, in the legal Marxist monthly *Zhizn* for June 1900. The search
used only rows 1 and 2 of the square. Of the 69 filled cells of the other eight rows, 64 hold the poem's
letter, and the poem supplies the other eleven. Read with the poem, 516 of the 555 pairs in this key that can
be compared give the edition's reading (562 are printed), and in three places the pairs as printed do not give
the name that the compilers read. [bauman](bauman/README.md) has the poem and the evidence.

## The key to document 15

A letter of April 1901 to Ivan Babushkin gives in cipher an address in Moscow, which the compilers of the
edition read as «Москва, Бойни, ветеринар[ный] врач ...» without the name; Sinelnikov could not judge the
reading, since the key was unknown. The key proves to be «Fatalità», a poem by Ada Negri, as translated by
V. G. Tan (Vladimir Bogoraz). In a strict search over 54,311 blocks of verse from Russian Wikisource it gives
16 of the 18 letters of that reading that complete pairs fix, and no other text gives more than 9. The pairs
that the search did not use complete «врачъ» and then give «Иоделло», which may be the missing name;
[doc15](doc15/README.md) gives the reading and the search.

## Checking

    python check.py

(Where Python 3 is called `python3`, that name replaces `python` here and below.) The script `check.py` runs
the checks of the three parts, `doc449/code/decode.py`, `bauman/code/check.py` and `doc15/code/decode.py`,
each with `--check`. Each part ends with a line such as `47 of 47 checks passed`, and `check.py` requires the
number of checks that each part is known to run. The check has succeeded if the last line is
`all three parts passed` and the exit status is 0. [runs/check.txt](runs/check.txt) holds the whole of what it
prints, and in a POSIX shell

    python check.py | cmp - runs/check.txt

compares a run with that record byte for byte. (PowerShell re-encodes what passes through a pipe, so the
comparison needs a shell such as bash.)

The scripts recompute, from the key texts and the pairs as transcribed, the counts that the four pages draw
from them, and compare the figures, tables, letters and readings of the pages that
[runs/check.txt](runs/check.txt) names with what they have computed or, for the search over other texts, with
its records in `runs/`. They also run the controls: the pairs read from other lines of each key, the square
begun at other lines of the poem, hard signs not counted. Each part can be checked on its own, as its page
says, and without `--check` each script prints its decipherment; the records of these are in `runs/`.

The scripts use only the standard library and need Python 3.10 or later.

## What has been checked, and what has not

- The pairs were typed from page images of the edition and then compared with those images again, pair by
  pair. Everything rests on the printed edition, and no manuscript has been seen; the limits on each page give
  the archival references of the manuscripts that could settle its questions.
- The hymn and the poem from *Zhizn* were compared with images of the printed pages. Tan's translation is
  taken from Russian Wikisource, and the limits of [doc15](doc15/README.md#limits) say which text.
- A pass of `python check.py` shows that the keys, the pairs, the readings and the figures that the check
  names agree with one another. It cannot show that a pair was copied correctly from the edition, how the
  edition sets a pair (with a space or a query, for instance), or that a date, a page, a quotation or an
  archival reference is right; those were compared with the sources by hand.
- The check does not rerun the search over other texts on the page for document 15, because neither the
  Wikisource dump nor the collection of verse cut from it is in the repository.
  [runs/README.md](runs/README.md) identifies both, and the two scripts that made the search are in
  `doc15/code/`.
- Page numbers of Sinelnikov's study are those of the PDF named under Sources; other copies of the text are
  paginated differently or not at all.
- The searches for earlier readings were last made on 12 October 2026. They covered
  the web, GitHub and Zenodo, for the first line of the poem from *Zhizn*, the name «Иоделло», the address in
  document 449 and the three keys, in Russian and in English, and found no earlier reading. Yu. S. Uralsky's
  *Пароль: «От Петрова»* (Moscow, 1988), in which according to Sinelnikov the *Iskra* keys known to its author
  were first made public, has not been seen, and printed work that is not open on the web would not have been
  found.

The questions that each result leaves open are listed on its page.

## Contents

| Folder or file | Contents |
|---|---|
| [doc449/](doc449/README.md) | the address in document 449: the page, the hymn, the pairs, the script |
| [bauman/](bauman/README.md) | Bauman's key: the page, the poem, the pairs from nine letters, Sinelnikov's square, the script, three page images of the journal |
| [doc15/](doc15/README.md) | the key to document 15: the page, the poem, the pairs, the script, and the scripts of the search over other texts |
| `check.py` | runs the checks of the three parts |
| [runs/](runs/README.md) | what the scripts printed; [runs/README.md](runs/README.md) says which record belongs to which claim |
| [tests/](tests/TESTS.md) | the mutation test and its description |
| `tools/make_sums.sh` | writes `SHA256SUMS.txt` |

The file `SHA256SUMS.txt` lists the SHA-256 of every other file (`sha256sum -c SHA256SUMS.txt`, or
`shasum -a 256 -c SHA256SUMS.txt` where there is no `sha256sum`). The workflow in `.github/` checks that list
and the style of the scripts, runs `python check.py`, the three scripts and the mutation test under Linux and
under Windows, and compares what they print with the records in `runs/`. The settings of the linter that it
runs are in `ruff.toml`.

## Tests

    python tests/mutation_test.py

The mutation test makes 56 deliberate errors in the data, the pages and the scripts, one at a time, and
reports which of them `python check.py` detects. It ends with status 0 if 51 are detected and the other five
are not, as expected: these are four facts quoted from the sources and a letter of Tan's translation that no
check reads. [tests/TESTS.md](tests/TESTS.md) describes the errors and says what the tests do not reach.

## Sources

- *Переписка В. И. Ленина и редакции газеты «Искра» с социал-демократическими организациями в России.
  1900–1903 гг.*, 3 vols (Moscow: Мысль, 1969–1970), prepared by К. Г. Ляшенко, В. Н. Степанов and
  З. Н. Тихонова. The pages call it "the edition", cite it by volume, document number and page, and call those
  who prepared it "the compilers". Scans of the three volumes are at
  <https://leninism.su/images/PDF/perepiska11.pdf>, <https://leninism.su/images/PDF/perepiska2.pdf> and
  <https://leninism.su/images/PDF/perepiska3.pdf>. The edition dates each letter in the New Style and then in
  the Old Style in brackets (vol. 1, p. 23); letters are dated here in the New Style, and other dates as the
  sources give them.
- А. В. Синельников, *Шифры и революционеры России*, dated Novosibirsk, 1980–2000, with revisions of 2009.
  Pages are cited from the PDF at <https://leninism.su/images/PDF/sinelnikov.pdf>; the text is also at
  <http://hrono.ru/libris/lib_s/shifr00.html>. Appendix 2 lists the identified keys and appendix 4 the
  letters still unread and the keys still unknown.
- The key texts are «Гимнъ новѣйшаго русскаго соціалиста», *Заря* 1 (Stuttgart, April 1901), pp. 152–153; the
  poem signed Л. Медвѣдевъ, *Жизнь*, vol. VI (June 1900), p. 50; and Ada Negri's «Fatalità», translated by
  В. Г. Танъ, in the text of Russian Wikisource.

## Licence and citation

The scripts (every `.py` and `.sh` file), the workflow and the configuration files (`ruff.toml`,
`.gitattributes`, `.gitignore`) are released under the MIT licence ([LICENSE](LICENSE)). The pages, the
records in `runs/` and the files in the `data/` folders are released under the Creative Commons Attribution
4.0 licence ([LICENSE-CC-BY-4.0](LICENSE-CC-BY-4.0)). [CITATION.cff](CITATION.cff) says how to cite the
repository.

The files in `data/` transcribe the letters and the three key poems, texts of 1899 to 1902 in which no rights
are claimed, and quote the readings that the edition prints; the licence covers what has been added to them.
The exception is `bauman/data/sinelnikov_square.txt`, which reproduces the square printed in Sinelnikov's
study and is covered by neither licence. The three images in `bauman/images/` are pages of *Жизнь*, vol. VI
(1900), from the scan of the volume at Google Books (id sYgAAAAAYAAJ), and are covered by neither licence.

Reports of errors are welcome, as an [issue](https://github.com/devinokeefe/Iskra/issues).
