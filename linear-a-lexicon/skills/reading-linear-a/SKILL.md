---
name: reading-linear-a
description: Answers questions about Linear A, the script of Minoan Crete, from the Linear A Lexicon, Tom di Mino's proposed readings of it as an archaic Semitic language. This skill should be used when the user asks what a Linear A word, name or sign means (KU-RO, JA-SA-SA-RA-ME), asks to read or translate a Linear A tablet or inscription (HT 13, IO Za 2), asks whether Linear A is deciphered or about the Minoan language, asks which Linear A words are compared with a Hebrew, Ugaritic or Akkadian form, asks for Linear A words by their signs or spelling, or mentions the Linear A Lexicon or linear-a.ai. It covers which tool to call and how to give a reading, as a proposal with its tier and any rival reading on record. Not for Linear B, Cretan Hieroglyphic or the Phaistos Disc. The user's own instructions take precedence over this skill.
---

# Reading Linear A

The Linear A Lexicon holds Tom di Mino's proposed readings of Linear A as Minoan, an archaic Semitic
language. Give every reading as "proposed", with its tier, and name any rival reading the result
mentions. The results carry this wording already (`proposed_reading`, `tier`, `tier_meaning`,
`rivals`, `summary`); keep it when summarising.

The user's instructions override this skill whenever they differ.

## Which tool

| The user asks | Call |
|---|---|
| what a word means (KU-RO) | `get_word` |
| who or what a name is: a person, place, god or title | `get_name` |
| to read or translate one document (HT 13, IO Za 2) | `get_text` |
| about a Proto-Semitic root | `get_root` |
| how one sign is read (AB08, KU) | `get_sign` |
| whether Linear A is deciphered, what a tier means, how to cite, what changed | `get_lexicon_overview` |
| for a set of words, names or documents by tier, type, site, scribe or language | `list_words`, `list_names`, `list_texts` |
| which words are compared with a form of another language (Hebrew peten) | `find_words_compared_with` |
| for words by spelling: beginning, ending, containing, or a pattern like A-?-RA | `find_words_by_signs` |
| for every place a word appears, each with its line | `list_occurrences` |
| which values a list filter takes (the scribes, the sites, the compared languages) | `list_values` |
| how the statistical tests of the language stand: the ten kernels, their calibration gates and p-values | `kernel_summary` |
| to run the anchor permutation test, or its Linear B control | `run_anchor_kernel` |
| to run the commodity-ligature test, or its Linear B control | `run_ligature_kernel` |
| anything else: an English meaning, a scholar, a topic | `search`, then `fetch` the ids worth reading |

Call the `get_` tool when the item can be named, because it returns the whole record in one call;
`search` is for when it cannot. Pass an id from one result to the next call as it was given.

## Giving a reading

To answer "What does X mean?":

1. Call `get_word` with the word as written.
2. Give the proposed reading and meaning, the tier and what the tier means, who first proposed it
   when the result names one, and any rival the result mentions.
3. Cite the result's `url`, so the user can check the record.

To answer "Translate this tablet":

1. Call `get_text` with the document's number.
2. Give the translation as a proposed translation, with its tier. Where the result gives word glosses
   and no translation, say that no translation is proposed.

To answer "Is Linear A deciphered?", call `get_lexicon_overview` and give its `standing`: what the
Lexicon reads Linear A as, whose reading it is, and the kernels that test it (`kernel_summary`).

## Mistakes to avoid

- **Confirmed is not "proven Semitic".** The Confirmed tier fixes a word's function in the corpus
  (a total, a commodity). Its etymology may still be a proposal; say so whenever the tier is Confirmed.
- **Not found is an answer.** Report it as not found and offer the names the result suggests. Do not
  pick one for the user or supply a reading from memory: the Lexicon's value is that each reading
  is on record.
- **A transliteration the result withholds stays withheld.** Some documents link to the site for
  their text, for licensing reasons. Give the link; do not reconstruct the text.
- **"HT 9" after "scribe" is a scribe, not a tablet.** Use `list_texts` with `scribe`, not `get_text`.
- **An English meaning is not a compared form.** "The word for wine" is `search` then `get_word`.
  `find_words_compared_with` takes a form in another language (yayin, פתן, bṯn).
- **Add no filter the user did not name.** A list tool given an extra filter silently narrows the
  answer. When a list finds nothing, say so, and use the counts in the result to say what a wider
  search would find.
- **A long record comes in parts.** When a `fetch` result names a next id, fetch it before saying
  what the record does or does not contain.
- **A sign search may be partial.** When its summary says some forms were not searched, repeat that.
- **A kernel result is a test, not a reading.** Give its statistic, p-value and gate as the result
  states them, and say which control ran. No word's meaning comes from a kernel tool: that is
  `get_word`.
- **Compose no Minoan.** The Lexicon holds attested words only; a new sentence would be invention
  presented as the record.
- **Other scripts are out of scope.** Linear B, Cretan Hieroglyphic and the Phaistos Disc are not in
  the Lexicon. Say so and call no tool.
