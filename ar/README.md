# Arabic

The Arabic corpus - official translation - is here: 25 masters translated from
the Russian masters in `ru/`, plus the Manifesto in `_manifest/ar-manifest.md`.

Translated from Russian, not from English, and not from the earlier round of
Arabic pages that still sits on the site. Those pages predate the rewriting of
the Russian masters - the Declaration was rebuilt into five parts and eleven
articles - and they are not a reference text.

Arabic is not one of the languages in which the UN Charter and the two Covenants
were concluded. Article 111 of the Charter and Article 53 of the Covenant on
Civil and Political Rights name five, and Arabic is not among them. That is not
a slight on the Arabic text; it is what makes Article 15 of our Declaration
legible to an Arabic lawyer on first reading, because Arabic stands on the same
side of that line as the other translations.

It also creates the one problem this corpus had to solve before anything else.
Articles 14 and 15 rest on a closed pair - the Russian and English texts are
authentic, the rest are official translations - and the Arabic text of the
Charter does not have the first word at all. Where the English original says
`equally authentic`, Article 111 in Arabic says
`وهي لغاته الرسمية على وجه السواء`: it calls the authentic texts *official*.
Taking the formula from there would erase exactly the distinction Article 15
protects. The pair is therefore taken from the Covenants, whose closing articles
do draw it and draw it identically - `تتساوى في الحجية نصوصه` - so authentic is
`متساويان في الحجية` and official translations are `ترجمات رسمية`. As a
consequence `رسمي` is used in this corpus only about translations, never about
the Russian and English texts of the Declaration.

Every terminology decision, with its source, is recorded in
`_СЛОВАРЬ_РЕШЕНИЙ.md` in this directory. The decisions that had no canonical
source and had to be built are collected there separately and marked `[СЛАБОЕ]`:
those are the ones a native reader should look at first. **Section 6А is the
operative list of terms** - it was written after the Declaration was piloted and
independently reviewed, and it overrides the tables above it wherever they
disagree.

Four Arabic-specific points matter more than they look. A people is `الشعب` and
a nation is `الأمة`, kept apart throughout, though the decision file records
honestly that the Arab Charter on Human Rights does not draw that line as
sharply as we need it. Our Charter is `الميثاق` and never `النظام الأساسي`,
which is the compulsory constitutive instrument of a registered association -
exactly what Article 4 of the Declaration denies that we are. A collective will
is `الإرادة المشتركة` and never `الإرادة العامة`, which is Rousseau's general
will and would import an argument the text does not make. And because Arabic has
no letter case, the distinction Russian carries with a capital letter has to be
carried by a name: the Charter is introduced as `ميثاق Earthlings` at first use
in every document, or it reads as the Charter of the United Nations, which is
named three times before it.

Two source findings are recorded so that the next session does not repeat the
search. The saving clause of resolution 2625 says `شعب الاقليم كله` in Arabic -
the whole people of the territory - which matches the Russian master, so the
sentence that follows it needed no rewriting, unlike in German. And ILO
Convention 169 has no authentic Arabic text at all: its Article 44 names only
English and French, and the translation the ILO published survives only in the
web archive. Document `04` calls it what it is - an Arabic translation issued by
the ILO.

Typography is stricter here than elsewhere in the corpus. Tatweel (U+0640) and
Arabic-Indic digits are forbidden outright and machine-checked to zero: where a
proclitic would have to be glued to a Latin name, the phrase is rebuilt with the
name after the noun instead. Vowel marks appear only where they resolve a real
ambiguity. Direction marks are not used at all.

What still needs a native Arabic reader, in order of importance: `الجواز` for
the passport, which in living Arabic completes itself to `جواز السفر`, a travel
document; `الخلية` for a cell, whose other sense is a terrorist cell; and
`التمايز القانوني` for legal distinguishability, which the blind reader of the
pilot did not understand. The legal documents are closed by the accuracy of
citation and are verifiable without a native speaker; intonation is not, so the
voice texts - the Manifesto, 03, 17, 23, 31 - are where a reader should start.

One thing does not translate and is worth naming. The first paragraph of the
Manifesto turns on the Russian word for international reading as *between
peoples*; the Arabic `دولية` reads as between *states*, which is the truth the
Russian word hides, and the irony collapses. The Arabic keeps the argument by
saying outright that this is how the word ought to be read.

The Manifesto PDF is not built for Arabic. That is a question of engine, not of
font: the generator has neither shaping nor a bidirectional algorithm, and the
usual workaround breaks on the Latin text the Manifesto contains. The web page
and the corpus are complete without it.
