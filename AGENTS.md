# linear-a-plugin: agent guide

The plugin that connects Claude and ChatGPT to the Linear A Lexicon's public MCP server
(`https://mcp.linear-a.ai/mcp`), with one skill, `reading-linear-a`. The server, the data and the research record
are in [kaphtor](https://github.com/plasma-ai/kaphtor); this repository holds only what a host installs and the
files that check it. Python 3.12, standard library only; pytest is the one dependency.

## Structure

- `linear-a-lexicon/`: the plugin as a host installs it. `.claude-plugin/plugin.json` and `.mcp.json` are Claude's;
  `plugin.json` and `mcp.json` are the portable pair ChatGPT reads; `skills/reading-linear-a/SKILL.md` is the skill.
- `package/`: the listing strings (`listing.json`), a copy of the server's contract (`mcp-contract.json`), the
  golden prompts, the trigger queries, and two scripts.
- `tests/test_plugin.py`: checks that the manifests, the listing, the skill and the contract copy agree. No network.
- `docs/`: the guides listed below.

## Commands

Run from the repository root.

- Tests: `uv run --with pytest pytest tests`
- Contract copy against the running server (reads only): `python3 package/check_contract.py`
- Validate the plugin for Claude: `claude plugin validate linear-a-lexicon`
- Build the ChatGPT zip: `python3 package/pack_chatgpt.py OUT_DIR` (OUT_DIR outside `linear-a-lexicon/`)

## Conventions

- Each listing string is written once, in `package/listing.json`. The two manifests repeat the strings they carry,
  and a test fails when a copy differs: change `listing.json` first, then both manifests.
- The copy says "proposed". It never states that Linear A is deciphered, decoded, cracked or solved, and never uses
  the word "consensus"; a test searches every string for these.
- The server's tools are stated in four places: the count `TOOLS` in the test, one row per tool in the skill's
  table, and two listing strings that spell the count out ("all eighteen", "eighteen read-only tools"). Change all
  four together.
- The version is in both manifests and must be equal.
- A script's user agent names the project and nothing else: no address, no contact detail.

## Boundaries

- The repository is `linear-a-plugin`; the plugin is `linear-a-lexicon` (its folder, slug, install command and zip
  name). kaphtor's marketplace installs it from this repository at the path `linear-a-lexicon`, so renaming the
  folder breaks that install: change both repositories together, or neither.
- `linear-a-lexicon/` holds no `bin`, `hooks` or `agents` folder, because the chat apps refuse a plugin that has
  one. Put scripts in `package/` instead.
- Tests never reach the network. Compare with the running server through `package/check_contract.py` instead.

## Guides

- [docs/copy.md](docs/copy.md): where each listing string lives, each host's limit, and the wording rules. Read
  before changing any description, example or the skill's frontmatter.
- [docs/maintaining.md](docs/maintaining.md): what to do when the server's tools change, how a release is made,
  and what the golden prompts and trigger queries are for. Read before a version bump or a contract update.
- [docs/submitting.md](docs/submitting.md): the steps of each directory's submission, the justification of the
  tool hints, and what the server receives. Read before submitting or answering a reviewer.
