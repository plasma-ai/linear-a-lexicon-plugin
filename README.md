# Linear A Lexicon plugin

The plugin that connects Claude and ChatGPT to the [Linear A Lexicon](https://linear-a.ai)'s public MCP server. It
pairs the server with one skill, `reading-linear-a`, which tells the model how to give a reading: as a proposal, with
its confidence tier, beside any rival reading on record.

The Lexicon's data, tools and research record are in [kaphtor](https://github.com/plasma-ai/kaphtor). This repository
holds the plugin alone, so that the two plugin directories can read it from a small repository.

## Install

In Claude Code, through kaphtor's marketplace:

```
/plugin marketplace add plasma-ai/kaphtor
/plugin install linear-a-lexicon@plasma
```

Any client that speaks Streamable HTTP MCP needs only the server's address, with no key and no sign-in:

```json
{
  "mcpServers": {
    "linear-a-lexicon": {
      "type": "http",
      "url": "https://mcp.linear-a.ai/mcp"
    }
  }
}
```

For ChatGPT, each release carries `linear-a-lexicon-chatgpt.zip`.

## Layout

| Path | What it is |
|---|---|
| `linear-a-lexicon/` | The plugin as a host installs it: Claude's manifest and `.mcp.json`, the portable `plugin.json` and `mcp.json` ChatGPT reads, the skill, two icons, a README and a licence |
| `package/listing.json` | Every listing string, once, with its host's limit; the manifests repeat the ones they carry |
| `package/mcp-contract.json` | A copy of the server's answers to `initialize` and `tools/list` (server 1.2.0, 18 tools) |
| `package/prompts.json` | The golden prompts and the bar they are held to |
| `package/trigger-queries.json` | Twenty questions, ten that should load the skill and ten that should not |
| `package/check_contract.py` | Compares the contract copy with the running server; reads only |
| `package/pack_chatgpt.py` | Writes the zip ChatGPT takes: the plugin folder without its dot files |
| `tests/` | Holds the manifests, the listing, the skill and the contract copy to each other; no network |

## Check it

```
uv run --with pytest pytest tests
python3 package/check_contract.py          # the copy against the running server
claude plugin validate linear-a-lexicon
python3 package/pack_chatgpt.py OUT_DIR
```

When `check_contract.py` reports a difference, take the server's new answers with
`python3 package/check_contract.py --print > package/mcp-contract.json`, add any new tool to the skill and correct the
count in the test and in the listing strings.

## Release

The plugin's version is in both manifests, and a test holds them equal. Raise it when the plugin folder changes in a
way a user would see, and publish a GitHub release: the release workflow attaches the ChatGPT zip. Claude's directory
follows `main` with the plugin path `linear-a-lexicon`.

## Licence

The files here are under the Apache License 2.0. `package/mcp-contract.json` copies the server's own tool
descriptions. The Lexicon's readings and the corpus keep their own terms, which each result states.
