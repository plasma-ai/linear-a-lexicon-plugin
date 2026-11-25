# Linear A Lexicon

Look up Tom di Mino's proposed readings of Linear A, the script of Minoan Crete, from a conversation.
The plugin pairs the Linear A Lexicon's public MCP server with a skill that tells the model how to
give a reading: as a proposal, with its confidence tier, and beside any rival reading on record.

The Lexicon reads Linear A as Minoan, an archaic Semitic language. Twelve signed probabilistic kernels
test that reading. Of the eleven that rank languages, ten rank Semitic first; the twelfth is a stress test of
the others.

## Use it

Ask what a Linear A word means, who a name refers to, how a tablet reads, which words are compared
with a Hebrew or Ugaritic form, or which words are spelt with given signs. Each answer links to the
page on [linear-a.ai](https://linear-a.ai) that shows the same record.

In Claude Code:

```
/plugin marketplace add plasma-ai/kaphtor
/plugin install linear-a-lexicon@plasma
```

The server is at `https://mcp.linear-a.ai/mcp`. It needs no account and no sign-in, and every tool
reads only.

## Data

The plugin sends the words, names, document numbers and search text of your question to
mcp.linear-a.ai, which answers from the published Lexicon. It needs no account and stores nothing
about you. See the [privacy page](https://linear-a.ai/privacy).

## Licence

The plugin's files (the manifests and the skill) are under the Apache License 2.0. The Lexicon's
readings and the corpus keep their own terms, which each result and the [terms page](https://linear-a.ai/terms)
state.
