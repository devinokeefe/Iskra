# The poem behind Bauman's cipher key

Nikolai Bauman, known in the party as Grach ("Rook"), settled in Moscow at the start of 1901 as an agent of
*Iskra* and corresponded with its editorial board until his arrest in the province of Voronezh in
February 1902. Nine letters from that correspondence have passages in his cipher, which the Soviet edition
of the correspondence ([Sources](../README.md#sources)) prints with their decipherment. The key was a poem
written into a square, ten lines by ten letters, a form that A. V. Sinelnikov calls unique in *Iskra*'s
practice. Sinelnikov writes that the compilers of the edition already knew the key and that the deciphered
letters are enough to restore it. The square printed in the study has 89 of its hundred cells filled, and
the other letters, it says, could not be established. The poem is listed there as "author unknown,
«Звезды усып...»". V. N. Stepanov, Yu. S. Uralsky and Sinelnikov had each tried for years to find the
author, and the study leaves the puzzle to its readers.

The poem was printed in *Zhizn* («Жизнь»), a St Petersburg monthly of the legal Marxists, vol. VI (June
1900), p. 50. It has sixteen lines and is signed Л. Медвѣдевъ, and the table of contents lists it as
«Стихотвореніе Л. Медвѣдева».

## The poem

    Звѣзды усыпали неба порфиру
        Въ сумракѣ ночи,
    Какъ безмятежно усталому міру
        Блещутъ ихъ очи.
    Тучки плывутъ средь эфирнаго моря
        Флотомъ воздушнымъ,
    Дѣла до счастья людского иль горя
        Нѣтъ равнодушнымъ.
    Богъ даровалъ для вселенной лампаду
        Въ мѣсяцѣ гордомъ...
    Ночь проливаетъ печаль и отраду
        Тихимъ аккордомъ.
    Музыку сна, какъ святыню, пріемлютъ
        Воды и суши...
    Только людскія сердца не задремлютъ,
        Бодрствуютъ души...
                                  Л. Медвѣдевъ.

The page is `images/zhizn1900_p50.png`, from the Google Books scan of the volume (id sYgAAAAAYAAJ). The page
carries no number; the contents give 50 and the page before it is 49. The title page and the contents are in
`images/zhizn1900_title.png` and `images/zhizn1900_contents.png`.

## The key

The first ten lines are the rows of the square, in the old spelling and with the final ъ counted. A pair a/b
means row a, letter b, and either number may be raised by a multiple of ten (11 = 1, 23 = 3, 35 = 5). The
square has no ж and no ш, so 3/12 and 8/12 stand for the real twelfth letters of lines 3 and 8, as Sinelnikov
describes. Six of the printed pairs use a twelfth letter. Two more pairs have 12 as their second number, 4/12
in no. 73 and 2/12 in no. 200, and are read by the rule of tens as 4/2 and 2/2.

Sinelnikov allows only the second and third tens in place of the first. Numbers above thirty occur seven
times in the letters, six in the thirties and one in the fifties, and four of them give the printed letter
when read in the same way (33/9, 5/35 and 38/11 in no. 14, 33/2 in no. 24). The script reads every number
modulo ten.

            1  2  3  4  5  6  7  8  9  10      12
        1   З  в  ѣ  з  д  ы  у  с  ы  п
        2   В  ъ  с  у  м  р  а  к  ѣ  н
        3   К  а  к  ъ  б  е  з  м  я  т       ж
        4   Б  л  е  щ  у  т  ъ  и  х  ъ
        5   Т  у  ч  к  и  п  л  ы  в  у
        6   Ф  л  о  т  о  м  ъ  в  о  з
        7   Д  ѣ  л  а  д  о  с  ч  а  с
        8   Н  ѣ  т  ъ  р  а  в  н  о  д       ш
        9   Б  о  г  ъ  д  а  р  о  в  а
       10   В  ъ  м  ѣ  с  я  ц  ѣ  г  о

## Evidence

The poem agrees with 84 of the 89 cells of Sinelnikov's square, and with four of the six letters in its
columns 11 and 12, е ж in row 3 and у ш in row 8. The other two, е ж in row 2, are discussed below. Rows 1 and
2 of the square were used to find the poem, so the test lies in rows 3 to 10, where the poem agrees with 64 of
the 69 filled cells.

Volume 1 of the edition prints pairs in this key in nine letters: nos 14, 24, 73, 80, 200, 222, 235, 318 and
336. The file `data/pairs.tsv` holds all 33 groups, 562 pairs, copied from the printed pages, each with the
reading the edition prints for it. The edition prints a pair as 3/5 in some of the letters and as 3.5 in
others, and four pairs with a space alone, three in no. 200 (p. 243) and one in no. 222 (p. 269); the slash is
used here for all of them. The script `code/check.py` deciphers the pairs with the poem. Letters are compared
in modern spelling (ѣ as е, і and й as и).

| | pairs giving the printed letter |
|---|---|
| the poem | 516 of 555 (93.0%) |
| Sinelnikov's square | 514 of 555 |
| the square begun at each other line of the poem in turn | at most 41 of 555 |
| the poem without hard signs | 346 of 555 |
| the poem without the twelfth letters | 510 of 555 |

Seven of the 562 pairs are not counted: three are printed without their second number (such as «6/...»), and
four have no letter in the printed word (three in no. 80, one in «Разоренова» in no. 14). Sinelnikov's square
is read with all its twelfth letters, including the ж at 2/12. For the third row of the table the sixteen
lines are taken as a ring, so that a square begun at line 12 goes on from line 16 to line 1. Sinelnikov's
square scores almost as well as the poem, as it must, since it was made from these letters. The poem is
identified by its agreement with the square cell by cell, and by the real words it has where the square has
gaps.

The script lists the 39 pairs that do not give the printed letter, and they are of five kinds.

- seven in a row near the start of the first copy of the address in no. 200 (pairs 3 to 9). The address is
  written twice there, the second time under the heading «Bis»; the two copies are out of step at this
  point, and the edition prints a query after the seventh of these pairs;
- twenty single pairs, several of them one figure away from the pair wanted: 19/2 for 13/2 in «Полтава»,
  8/4 for 8/1 in «магазин», and for the м of «Марковичу», which is 10/3, the first copy in no. 200 has 10/9
  and the second 16/3. In no. 80 the second number is one too high four times (6/6, 8/6 and 8/7 twice, where
  6/5, 8/5 and 8/6 give the letters wanted);
- two of spelling: the cipher has «Лепешинскаго» and «получении» where the edition prints «Лепешинского» and
  «получению», and the square has no ю;
- three of the five in «Марье» in no. 14 (7/2, 9/4, 5/7);
- seven in four readings made by the compilers, in nos 14, 24 and 73. Three of these readings are discussed
  [below](#readings-that-the-printed-pairs-do-not-give). In the fourth, «Устинью», the one pair that
  disagrees is cell 10/9 (see Limits).

Two of the twenty single pairs are also in readings made by the compilers, 2/8 in «Покров» (no. 14) and 8/4 in
«магазин» (no. 73), so nine of the 39 fall in such readings.

## What the poem adds to the square

The printed pairs use 81 cells of the square. Ten of Sinelnikov's 89 are used by no pair (3/4, 3/10, 4/4,
4/5, 4/7, 4/10, 8/10, 10/4, 10/7 and 10/8), so those were presumably filled by completing the words. Nine of
the ten are right, and the tenth is 4/5, where Sinelnikov has «блещетъ» for the poem's «блещутъ».

The poem fills the eleven cells left empty in Sinelnikov's square and differs from it in five. Six of these
sixteen cells are used in the letters, and the table gives their uses.

| cell | poem | Sinelnikov | uses in the letters |
|---|---|---|---|
| 7/2 | ѣ | а | е or ѣ three times, the last letter of «на сѣверѣ» (no. 80) and of «отдѣленіе» in both copies (no. 200); а once, in «Марье» (no. 14) |
| 7/3 | л | н | л in «листок» (no. 24); н only in the compilers' «Доноди» (no. 73) |
| 5/7 | л | и | once, in «Марье», where the clear word has ь |
| 10/9 | г | и | three times, and г fits none of them (see Limits) |
| 6/7 | ъ | empty | the hard sign of «Меерсонъ» in both copies (no. 200) |
| 5/10 | у | empty | once, in no. 200, where к is wanted |

Sinelnikov's square also has е and ж in columns 11 and 12 of row 2, where the poem has о and ч («ночи»). The
only support for them is one 2/12 in the first copy of no. 200, where the second copy has 3/12.

## Readings that the printed pairs do not give

Some readings in the edition were made by its compilers, without a decipherment of the time to follow. In
three of them the pairs as printed say something else, leaving aside cell 10/9. The first two need nothing
from the poem, because the cells concerned are the same in Sinelnikov's square.

- No. 14, Babushkin's address in Pokrov, is printed «дом Чапышниной». The pairs 5/3 13/2 4/2 1/6 8/12 3/21
  5/5 18/1 8/2 15/5 give ч а л ы ш к и н ѣ и, with и for й, which the square does not have. That is
  «Чалышкиной» if 8/2 is a slip for 8/9, which is о. Cell 4/2 is л in eleven other places and 3/1 is к in
  eighteen. The index of the edition has «Чапышнина — домовладелица в Покрове» with this page as its only
  reference.
- No. 24, the address for callers in Pskov, is printed «Завеличье, дом Ветровой». The pairs 5/16 14/3 6/4 8/5
  7/6 11/2 6/3 give п е т р о в о, and the й that follows is in clear, so the name as printed in cipher is
  «Петровой». Cell 5/6 is п in seventeen other places. A 5/19 in the manuscript would give в, from one of
  the cells that only the poem supplies. The index again has «Ветрова — домовладелица в Пскове» from this
  page alone.
- No. 73, Bauman's address for callers in Moscow, is printed «спросить Устинью Яковлевну Топову, а у нее
  спросить Доноди». The last word is 7/1 6/3 7/3 6/5 7/1 10/9, which with the poem is д о л о д г, the г
  from cell 10/9. Sinelnikov has н at 7/3 and и at 10/9, which are the letters «Доноди» needs, so those two
  cells of the square probably come from this reading.

Twice the edition brackets letters that the pairs supply. No. 222 is printed «З[и]наида Павло[в]на», and both
bracketed letters are in the pairs. In no. 235 the name is printed «Ляп[унова]», as if the decipherment,
which the footnote gives to Krupskaya, had stopped at «Ляп»; the seven pairs printed with it give ляпунов.

No. 14 was written on the same day as no. 15, whose key is a different poem; see
[the page on document 15](../doc15/README.md).

## Limits

- Cell 10/9, г in the poem, fits none of its three uses: once in no. 200, where the м of «Марковичу» is
  wanted, and twice in no. 73, as the last of the six pairs that the compilers read «Устинью» and as the
  last pair of «Доноди». The manuscript of no. 73 is ЦПА ИМЛ, ф. 24, оп. 8у, ед. хр. 28167.
- «Марье» in no. 14, where the cipher is written above the clear word in an autograph: 7/2, 9/4 and 5/7
  stand over а, р and ь, and the poem gives ѣ, ъ and л.
- Whether the readings of nos 14 and 24 above are slips in the cipher that the compilers corrected without a
  note, as the rules of the edition allow (vol. 1, p. 23), faults in their readings or misprints in the pairs
  can be settled only from the manuscripts, autographs in the former Central Party Archive, ф. 2, оп. 1,
  ед. хр. 434: no. 14 at л. 21–21 об., no. 24 at л. 25, 26 and 26 об.
- In no. 80 the second number of four pairs is one too high. Its manuscript, ЦПА ИМЛ, ф. 24, оп. 8у,
  ед. хр. 28168, would show whether the cipher or the print is at fault.
- Four of the nine letters are printed from copies, so their pairs passed through a copyist's hands before the
  printer's. Nos 318 and 336 are police copies of intercepted letters (ЦГАОР, now ГАРФ, ф. ДП, ОО, 1901 г.,
  д. 825, ч. 3, л. 150–150 об., and ч. 4, л. 72–72 об.). Nos 200 and 235 are copies in the former Central
  Party Archive (ф. 24, оп. 8у, ед. хр. 28177 and 28181), the first in the hand of I. S. Blumenfeld. No. 200
  holds 18 of the 39 disagreements.
- Where the cipher skips letters of a printed reading, `data/pairs.tsv` omits them too (its header
  lists them), and the count of 516 rests on that alignment.
- The poet is known here only by the signature. Лев Михайлович Медведев (1865–1904), a poet, children's
  writer and translator whose books are listed on Russian Wikisource, is a possible match, and nothing seen
  so far ties him to *Zhizn*. Bauman's wife, К. П. Медведева in the index of the edition, had the same
  surname, which is a common one; no connection with the poem is known.

## How it was found

A search of the full text of Google Books for the openings of rows 1 and 2 of Sinelnikov's square,
completed to «Звѣзды усыпали» and «Въ сумракѣ» in the old spelling, returned the June 1900 volume of
*Zhizn*. Russian Wikisource, searched first, does not have the poem.

## Checking

From this folder:

    python code/check.py --check

The script reads the poem and the pairs from `data/`, deciphers every group, and tests against what it has
computed the figures, the square, the poem and the tables of this page that
[runs/check.txt](../runs/check.txt) names. Without `--check` it prints each
group of pairs with the key's reading beside the printed one, then the totals, the cells and the controls.

## Files

- `data/poem.txt`: the poem as printed.
- `data/sinelnikov_square.txt`: Sinelnikov's square, cell for cell.
- `data/pairs.tsv`: document, page, whose reading it is, the printed reading, the pairs, and the reading
  aligned to the pairs. Letters that the writer left in clear inside a group (й, ь) are not in the file,
  nor are the three queries that the edition prints among the pairs of no. 200.
- `code/check.py`: the decipherment and the checks.
- `images/`: the page with the poem, the title page and the contents of the journal.

## Sources

- «Жизнь. Литературный, научный и политическій журналъ», vol. VI (June 1900), p. 50.
- The edition, vol. 1, at the nine numbers given above, and the index of names in vol. 3.
- Sinelnikov, part 3, ch. 3, for Bauman's key, with the square on p. 134. The poem is no. 6 in appendix 2,
  and the nine letters are those listed there.
- Лев Михайлович Медведев on Russian Wikisource:
  <https://ru.wikisource.org/wiki/Автор:Лев_Михайлович_Медведев>.
