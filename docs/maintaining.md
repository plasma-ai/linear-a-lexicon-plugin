# Maintaining the plugin

## When the server changes

`package/mcp-contract.json` is a copy of the server's answers to `initialize` and `tools/list`. The tests read the
copy and never the network, so a change on the server shows only when the copy is compared with it:

```
python3 package/check_contract.py
```

It exits 0 when they match, 1 when they differ and 2 when the server did not answer. The `check` workflow runs it
every Monday and on request.

When it reports a difference:

1. Copy the server's new answers: `python3 package/check_contract.py --print > package/mcp-contract.json`.
2. For a new tool, add a row to the table in the skill. For a removed tool, delete its row.
3. If the number of tools changed, correct it in the three places that state it: `TOOLS` in
   `tests/test_plugin.py`, and the two listing strings that spell the number out (the weather case's reason and
   the release notes), each of which is repeated in `plugin.json`.
4. Correct the server version in the README's layout table.
5. Run the tests.

Every tool must be marked read-only, not destructive and not open-world; both directories require it and a test
checks it.

## Releasing

1. Raise `version` in both manifests when the plugin folder changes in a way a user would see. A test checks that
   the two are equal.
2. Update `releaseNotes` in `package/listing.json` and its copy in `plugin.json`.
3. Publish a GitHub release. The `release` workflow builds `linear-a-lexicon-chatgpt.zip` and attaches it.

## What each host reads

| Host | Reads |
|---|---|
| Claude Code, through kaphtor's marketplace | this repository's `main`, at the path `linear-a-lexicon` |
| Claude's plugin directory | `main`, at the path `linear-a-lexicon` |
| ChatGPT | the zip attached to a release: the plugin folder without any file or folder whose name begins with a dot |

The zip leaves out Claude's manifest folder and `.mcp.json`. The same files always give the same bytes.

## The prompt files

- `package/prompts.json`: 22 golden prompts (8 direct, 10 indirect, 4 negative), each with the tools it should call
  and what the answer should contain. `bar` gives the pass rate required of each kind (0.9 direct, 0.9 indirect,
  1.0 negative), and `configurations` names the three set-ups they are run under. A negative prompt calls no tool.
- `package/trigger-queries.json`: 20 questions, 10 that should load the skill and 10 that should not.

No script in this repository runs either file; the tests check only their counts and that every tool they name
exists.
