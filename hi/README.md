# Hindi

The Hindi corpus - official translation - is here: 25 masters translated from
the Russian masters in `ru/`, plus the Address in `_manifest/hi-manifest.md`.

Translated from Russian, not from English, and not from the earlier round of
Hindi pages that still sits on the site. Those pages predate the rewriting of
the Russian masters, and they are not a reference text - a census of all 23 of
them found the terminology had collapsed inside the translation itself: the
Declaration and the Address were rendered by one and the same word, the
Treasury and the Fund by another single word, the cells were named twice on the
same page, and belonging and membership were used interchangeably.

Hindi is the ninth and last language of the corpus, and it is the only one with
no source language at all. The other eight are protected by the fact that a
term is taken from an act. There is no official Hindi text of the UN Charter,
of either Covenant, of resolutions 1514, 1541 or 2625, of ILO Convention 169,
or of the Vienna Convention. The one instrument that exists in Hindi is the
Universal Declaration, and it says of itself, on its own first page, that the
official texts are the five UN languages and that what follows is a translation
approved by the Government of India.

That is not a gap to be papered over. It changes what the legal documents in
this directory are: they are not *verifiable* against a source, they are
*reasoned*. Every decision, with whatever source it has, is recorded in
`_СЛОВАРЬ_РЕШЕНИЙ.md` in this directory. The decisions built without a source
are collected separately and marked `[СЛАБОЕ]` - seventeen of them, against one
in Spanish. **Those are what a native reader should look at first.**

What replaced the missing acts is three supports, and only two of them held.
The Hindi edition of the Constitution of India, published under Article 394A,
carries the backbone: fundamental rights, citizenship, freedom of association,
constituent power. The Hindi editions of the central laws carry contract,
juristic person, obligation, registry. The third support - the CSTT
terminology glossaries - could not be reached at all; everything that should
have rested on it rests on the IT Act 2000 and the DPDP Act 2023 instead, or is
marked `[СЛАБОЕ]`.

The method for a language in exactly this position is not something this
session invented. Article 13 of the Declaration prescribes it: where official
texts of the named acts exist, take the term from them; where they do not, take
the term used in the official translation of the Covenant on Civil and
Political Rights; and where that does not exist either, take **a term conveying
the stated meaning, with an explanation at first use**. Hindi runs the whole
ladder to its last rung, which is why `जन` carries an English gloss at first
use in every document.

Four decisions matter more than the rest.

**A people is `जन`, and people are `लोग`.** The obvious reading points the other
way: the preamble of the Constitution says `हम, भारत के लोग`, and Article 51(c)
uses `लोगों` for *organised peoples* in international dealings. But the corpus
speaks of both things constantly, often in adjacent sentences - "we, **people**
of different countries ... constitute ourselves a **people**" - and one word for
both would have lost both. What settles it is countability: the corpus stands on
"one of the peoples", "are a people", "on the scale of a people", and a census of
the old pages found `एक जन` twelve times and `एक लोग` not once. English carries
this distinction with an article; Hindi carries it with two different words,
which is sturdier. `जनता` is locked out on two grounds - the Constitution uses it
only in `साधारण जनता`, the general public, and it is the word in the names of
Indian political parties, which collides with the corpus's own lock against
reading the people as a party. `राष्ट्र` is locked out because it is the nation,
and it never names India as a polity.

**Authentic is `प्राधिकृत` and official is `आधिकारिक`.** The first is the
Constitution's own word - Article 348(1)(b), Article 394A(3), where a
translation published under authority `प्राधिकृत पाठ समझा जाएगा`, is deemed the
authentic text for all purposes. The second was originally taken from the
Constitution too, as `शासकीय`, until a blind reading pointed out what a source
cannot: `शासकीय` means *governmental*, and this is a corpus that denies its own
statehood on every page. Article 15 of the Declaration rests on the two words
being different, and here Hindi keeps them apart twice over - by the adjectives
and by the nouns, `पाठ` against `अनुवाद`. `सरकारी` is forbidden outright for the
status of a text, because the Hindi Universal Declaration uses exactly that word
for the five **authentic** languages - the same trap Arabic had to avoid.

**The passport is `पासपोर्ट`, and `यात्रा-दस्तावेज` is a hard lock.** The
Passports Act 1967 defines the two as separate categories in adjacent clauses,
which means Indian law already has a precise word for a travel document and it
is not ours. No other language in the corpus closed that danger this cleanly.

**The Treasury is `कोष` and the Fund is `निधि`.** The place was free: `राजकोष`
and `कोषागार` do not occur in the Constitution at all - the state treasury there
is `संचित निधि` - so unlike French, where the word was occupied and the sentence
told a French reader the people had a French treasury, nothing had to be worked
around. It also repaired the worst collision in the old translation, where one
word served both concepts 109 times.

Typography needed less than expected and one thing more. The danda `।` and the
double danda `॥` are absent from the corpus-wide forbidden dictionary and pass
without any entry; a census of the old pages found 2615 dandas and not one
forbidden character. Quotation marks are guillemets, as in Arabic and Georgian,
because Hindi has none of its own and the curly ones are the mark of a foreign
keyboard. ZWNJ is not used at all. Nuktas are written decomposed, and the
precomposed codepoints U+0958-U+095F are machine-checked to zero, because
Unicode excludes them from composition and two spellings in one corpus would
make search and string comparison lie silently.

The thing that needed adding is specific to this language and was found the hard
way, in this session's own files: **a Cyrillic letter inside a Devanagari word.**
It is invisible - `रि` and `ри` are indistinguishable at body size - and it fails
completely and without a sound, because the word cannot then be found by search,
by replace, or by the audit itself, so a lock written with that typo reports
clean forever. It happens because the session writes Russian and Devanagari in
the same sitting and the keyboard layout switches mid-word. It is now checked
per document and across the corpus.

The Address PDF is not built for Hindi. That is a question of engine, not of
font: Devanagari needs conjunct ligatures and vowel reordering - the short *i*
is written after its consonant and drawn before it - and the generator has no
shaping at all, so the output would not be ugly but *wrong*, with words spelled
in the wrong letters and the wrong order, plausibly enough not to notice. No
font in the repository covers the script either. The web pages and the corpus
are complete without it; Arabic stands in the same position for the same reason.

What still needs a native Hindi reader, in order of importance: `जन` itself,
because standalone it is not attested in the operative text of the Constitution
and because colloquially it counts people one by one; `विधिक व्यक्तित्व` and
`अधिकार-क्षमता`, which are built rather than quoted and which no Indian statute
supplies; `कार्यभार` for a commission, where the agency term of the Contract Act
had to be rejected because it defines the agent through representation, and
Article 11 of the Declaration denies exactly that; and `कोशिका` for a cell,
which may read too biologically in an organisational text. The legal documents
here are closed by consistency, not by citation; the voice texts - the Address,
`02`, `03`, `23`, `31` - are closed by nothing at all, and that is where a
reader should start.
