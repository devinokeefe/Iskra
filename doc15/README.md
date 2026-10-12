# Document 15: the key poem

On 5 April 1901 Inna Leman, then secretary to *Iskra*'s editorial board, wrote to Ivan Babushkin in Pokrov
and gave him in cipher the address at which to find «заграничный человек», the man from abroad. The Soviet
edition of the correspondence ([Sources](../README.md#sources)) prints a reading of the address, «Москва,
Бойни, ветеринар[ный] врач ...», with dots for a name, and its footnote says that the address was deciphered
by the compilers of the edition. A. V. Sinelnikov puts the decipherment in the 1960s and gives it, with a
"presumably", to V. N. Stepanov, who led the compilers. Sinelnikov lists the letter among the cryptograms
whose key is unknown and adds that the reading cannot be judged until the key is found.

The key is Ada Negri's «Fatalità» in the Russian translation of V. G. Tan, the pen-name of the ethnographer
and poet Vladimir Bogoraz (1865–1936). The poem begins «Полночною порой вчера къ моей постели», and with it
the 34 printed pairs give, letter by letter,

    моссв.  ыойни  ветерина  .лй.  рачъ  иоделло

where a point stands for a pair printed without its second number. That is the address

    Мос[к]в[а], [Б]ойни, ветерина[рный в]рачъ Иоделло

or "Moscow, the slaughterhouses, veterinary surgeon Iodello". Of the eighteen letters of the compilers'
reading that complete pairs fix, sixteen agree with the key, and where the compilers print dots the key gives
seven letters. The key was found by searching for that agreement, but in some 6.8 million trials, many of them
repeats, no other text gave more than nine of the eighteen (see [How it was found](#how-it-was-found)). The
size of the search does not account for the sixteen, which support the key and the compilers' reading
together. A second test lies in the pairs that the search did not use. The four after the bracketed stretch
give «рачъ», the end of «врачъ», three of its letters from cells that no earlier pair uses. The seven after
them give a word that may be a name, which nothing confirms: no one of that name has been found in the parts
of the Moscow directory that were searched.

## The document

The letter is no. 15 in vol. 1 of the edition, p. 50. The autograph is in the former Central Party Archive
(ЦПА ИМЛ, now РГАСПИ), ф. 2, оп. 1, ед. хр. 434, л. 16. The sentence runs: «Адрес заграничного человека:
Москва, Бойни, ветеринар[ный] врач ... а у него спросить Николая Петровича Орлова, — это и будет
заграничный человек.» The footnote prints the pairs and ends «Часть шифра густо зачеркнута» ("part of the
cipher is heavily deleted").

The file `data/pairs.tsv` holds the pairs as printed. Beside pairs 1 to 20 it gives the letter that the
compilers' reading requires. Eighteen of those twenty pairs are printed in full and can be tested.

The reading of 1969 could have been made from the context, without the key. Three of the cells that it fixes
occur again later in the passage. Pair 22 repeats 10/2, the й of «Бойни», and pair 24 repeats 4/3, which is р
where «врачъ» would have it if the word begins at pair 23. Pair 28, the first of the name, repeats 4/1, and no
other pair of the name uses a cell that occurs earlier in the passage, so a reading made without the key could
have gone no further than the compilers' dots.

## The key

The file `data/key_negri_tan.txt` has the poem in the old spelling, from Russian Wikisource, which gives its
first publication as *Nachalo*, a legal Marxist monthly of St Petersburg, 1899, no. 5, p. 165, and names no
source for its text. Tan's verse was in use in this correspondence in another way. Sinelnikov (part 3, ch. 4)
tells of a letter from Lenin in cipher, written between the lines of a volume of Tan's poems, that was found
on S. V. Andropov when he was arrested at Kazan on 26 August 1901.

The first line of the poem is line 1, and a pair a/b is letter b of line a. Letters are counted without
spaces or punctuation and in the old spelling, so a hard sign (ъ) at the end of a word takes a place.

## The reading

| n | pair | letter | compilers | |
|---|------|--------|-----------|---|
| 1 | 3/5 | м | м | |
| 2 | 4/6 | о | о | |
| 3 | 5/2 | с | с | |
| 4 | 5/8 | с | к | к stands at 5/9 and 5/3 |
| 5 | 3/1 | в | в | |
| 6 | 2/... | | а | second number not printed; а stands at 2/5 |
| 7 | 13/2 | ы | б | б stands at 13/3 |
| 8 | 12/1 | о | о | |
| 9 | 10/2 | й | й | |
| 10 | 9/1 | н | н | |
| 11 | 4/1 | и | и | |
| 12 | 2/2 | в | в | |
| 13 | 9/2 | е | е | |
| 14 | 3/3 | т | т | |
| 15 | 11/4 | е | е | |
| 16 | 4/3 | р | р | |
| 17 | 2/3 | и | и | |
| 18 | 1/7 | н | н | |
| 19 | 2/5 | а | а | |
| 20 | 9/... | | р | second number not printed; р stands at 9/3, н at 9/1 and 9/6 |
| 21 | 6/10 | л | | |
| 22 | 10/2 | й | | |
| 23 | 2/... | | | second number not printed; в stands at 2/2 |
| 24 | 4/3 | р | | |
| 25 | 7/5 | а | | |
| 26 | 1/6 | ч | | |
| 27 | 3/2 | ъ | | |
| 28 | 4/1 | и | | |
| 29 | 1/2 | о | | |
| 30 | 4/9 | д | | |
| 31 | 6/4 | е | | |
| 32 | 2/4 | л | | |
| 33 | 7/2 | л | | |
| 34 | 8/3 | о | | |

Three of the 34 pairs are printed without a second number, and three more give a letter that the address
cannot have. Pair 4 gives с for the к of «Москва», and pair 7 gives ы for the б of «Бойни». In both the letter
wanted is the next one in the line, and for pair 4 it also stands at 5/3, so a 3 misread as 8 would explain it
as well. Or the writer may not have counted the soft sign: line 5 begins «Я скорбь!», and without its ь, 5/8
is к. Leaving the soft sign out of the count changes no other pair of the 34, so pair 4 is the only test of
it, and the agreement would be 17 of 18. The third of the three is pair 21, which gives л.

Pairs 20 to 23 stand where the compilers print «р[ный] в», and two of them are printed incomplete, perhaps
where the footnote says the cipher is deleted. The й of pair 22 fits the ending of «ветеринарный». Pair 20 can
be р or н, since line 9 has both, and pair 23 can be в, but four pairs cannot hold the five letters «рный в».
If pair 21 was 6/16, which is ы, the four pairs read н ы й в, and the writer omitted the р of «ветеринарный»;
without the soft sign in the count, that ы would be 6/15. The printed pairs do not decide this, and the
stretch is bracketed above for that reason.

Pairs 24 to 34 played no part in finding the key. They give «рачъ», which completes «врачъ» with its hard
sign, and then «иоделло». Pair 24 is 4/3, the cell of pair 16, which the search had already fixed as р, but
the other three letters of «рачъ» come from cells that no earlier pair uses (7/5, 1/6 and 3/2). This is the
second test, and a small one: three new cells, one of them a hard sign, at a place that the compilers' reading
fixes only to within a pair, since the stretch before it may or may not end with the в of «врачъ».

## The name

«Иоделло» is what the last seven pairs give; in the spelling of the time it would be Іоделло. *Vsya Moskva*
(«Вся Москва»), the city directory, has no Іоделло for 1901 in its list of veterinarians (cols 833–834), among
the staff of the city slaughterhouses (col. 533), or in the alphabetical list of residents (pp. 180–181). In
case the first letters are initials, the same list has no Оделло (p. 318) and no Делло (p. 127). The list of
residents for 1902 has no Іоделло either (p. 180). The veterinarians named at the slaughterhouses in 1901 are
Сальяръ, Вихерскій, Зеленинъ, Кочуровъ, Невтеревъ, Шукевичъ and Половинкинъ, with a doctor Чернышевъ.

The index of the edition names six veterinarians who worked in Moscow among the party's contacts.
P. N. Andreyev, a veterinarian of the city slaughterhouses, is in a letter of March 1903 (vol. 3, no. 1120).
L. L. Nikiforov and A. A. Petrov were arrested in September 1901 (vol. 1, pp. 280 and 286), and
V. S. Bobrovsky in February 1902. The addresses of S. N. Pavlushkov and A. I. Popov served as meeting places
from September 1902 (vol. 2, p. 280). None of the six is the name that the seven pairs give, and Andreyev is
not among the slaughterhouse staff listed for 1901.

The man Babushkin was to ask for, Nikolai Petrovich Orlov, is Nikolai Bauman: the index of the edition gives
Orlov among his aliases, and notes that he qualified at the Kazan Veterinary Institute in 1895. Document 14,
written to Bauman on the same day, gives him Babushkin's address in Pokrov, so each was being told where to
find the other. The cipher of document 14 is in Bauman's own key; see
[the page on that key](../bauman/README.md).

## Limits

- The pairs use only the first ten letters of the first thirteen lines of the poem, so an error in Tan's
  text elsewhere could not change the reading.
- Three of the 24 complete pairs before the name give a letter that the address cannot have (pairs 4, 7 and
  21). At that rate the chance is about 0.39 that the seven pairs of the name hold no slip (about 0.54 if the
  soft sign explains pair 4), and it is probably lower, since the key was chosen to fit 18 of those 24 pairs.
- The directories were searched only for Іоделло, Оделло and Делло, and the volume for 1902 only in its list
  of residents.
- The text of Tan's translation is that of the Russian Wikisource page in the old spelling (revision
  5004993, 26 August 2023) and has not been compared with a printing. The page that gives the poem in
  modern spelling, without hard signs, gives 14 of the 18.
- The looser search that first found the key ran on an earlier collection of verse, which is not in the
  repository, so its 17 of 18 cannot be repeated from these files.
- The autograph, ЦПА ИМЛ (now РГАСПИ), ф. 2, оп. 1, ед. хр. 434, л. 16, is the only source that might show
  whether pairs 4, 7 and 21 are slips of the writer or misprints, and what the three incomplete pairs and the
  heavily deleted part of the cipher were.

## How it was found

The compilers' reading served as a crib, a guess at the plain text against which keys can be tried. The
key was first found by a looser search, over a collection of verse cut earlier from Wikisource, in which
the line of a text that a line number of the cipher stands for could drift by one from one line number
to the next, and by two at most in all; with that freedom Tan's translation gave 17 of the 18.

The figures given here are those of the strict search, which `code/corpus_control.py` makes over 91,128 blocks
of verse from the Russian Wikisource dump of 1 October 2026, which holds the whole site in one file. They are
the texts that the site marks as verse in its main namespace and in «Страница», as `code/make_corpus.py` takes
them. Each of the 54,311 blocks of thirteen lines or more was tried with each of its lines as line 1, as far
as the pairs stayed inside the block. That gives 1,565,962 start lines with the pair read line/letter, and
more with the pair read letter/line, which reaches only eight lines down. Every start was tried with the hard
signs at the ends of words counted and not counted, 6,806,958 trials in all, many of them repeats, since a
block with no hard sign at the end of a word gives the same trial both ways. Each trial was scored by how many
of the eighteen testable pairs gave the compilers' letter. Tan's translation gave 16 of 18, and the best of
the other texts gave 9.

## Checking

From this folder:

    python code/decode.py --check

The script reads the poem and the pairs from `data/`. It tests the figures of the search over other texts
against the records of that search in `runs/`, and the reading, the table and the other figures of this page
that [runs/check.txt](../runs/check.txt) names against what it has computed. It also tries every other line of
the poem as line 1, and the pair read letter/line from every line, going on from the first line where the
count runs past the last. Taken from any of the other 25 lines, the pairs give at most 3 of the 18 letters
(from lines 16 and 20), and read letter/line at most 2. Without hard signs in the count, 14 agree and the last
eleven pairs give «рачтиоублло». Without `--check` the script prints the table.

The command `python code/make_corpus.py <dump> <corpus.jsonl>` cuts the collection from the dump, and
`python code/corpus_control.py <corpus.jsonl>` runs the search over it. [runs/README.md](../runs/README.md)
identifies the dump and the collection, which are not in the repository.

## Files

- `data/key_negri_tan.txt`: the poem.
- `data/pairs.tsv`: the pairs as printed, with the compilers' letters.
- `code/decode.py`: the table, the reading and the checks.
- `code/make_corpus.py`: cuts the collection of verse from the Wikisource dump.
- `code/corpus_control.py`: the same test over the collection.

## Sources

- The edition, vol. 1, no. 15, p. 50, and the index of names in vol. 3.
- Sinelnikov, appendix 4, no. 2: «Письмо было в 1960-х годах расшифровано (предположительно) В. Н. Степановым.
  Но ключ пока не определен, а значит говорить о правильности его варианта текста преждевременно. 34
  шифрдроби». The poem is not among the identified keys in appendix 2. On Stepanov and the edition, part 3,
  ch. 1.
- Ada Negri, «Fatalità», translated by В. Г. Танъ: the Russian Wikisource page «Полночною порой вчера к моей
  постели (Негри; Богораз)/ДО».
- *Вся Москва* for 1901 and 1902, in the electronic library of the State Public Historical Library of
  Russia: <http://elib.shpl.ru/ru/nodes/27432-na-1901-god-30-y-god-izdaniya-1901> and
  <http://elib.shpl.ru/ru/nodes/17512-na-1902-god-31-y-god-izdaniya-1902>.
