# The listing copy

Every string a plugin directory shows is written once, in `package/listing.json`. The manifests repeat the strings
their host reads. `tests/test_plugin.py` fails when a copy differs or a string is over its limit.

## Where each string lives

| String | In `listing.json` | Repeated in |
|---|---|---|
| Display name | `name` | both manifests (`displayName`) |
| Slug | `slug` | both manifests (`name`) |
| Publisher | `publisher` | both manifests (`author.name`, `developerName`) |
| ChatGPT short description | `openai.shortDescription` | `plugin.json` |
| ChatGPT long description | `openai.longDescription` | `plugin.json` |
| ChatGPT category and capabilities | `openai.category`, `openai.capabilities` | `plugin.json` |
| Claude one-liner and description | `anthropic.oneLiner`, `anthropic.description` | nowhere: neither manifest carries them |
| Five examples and three negative cases | `examples`, `negative` | `plugin.json`, as the review test cases |
| Release notes | `releaseNotes` | `plugin.json` |
| Website, support, privacy and terms addresses | `website`, `support`, `privacy`, `terms` | `plugin.json`; the privacy address also in Claude's manifest |

The manifests' own `description` is not in `listing.json`. It must be the same in both manifests.

The skill's `name` and `description` are in the frontmatter of `linear-a-lexicon/skills/reading-linear-a/SKILL.md`.

## Limits

| String | Limit |
|---|---|
| ChatGPT short description | 30 characters |
| ChatGPT long description | 4,000 characters |
| Display name | 30 characters |
| Publisher | 80 characters |
| Each capability | 120 characters, one line, at most 20 of them |
| Each default prompt | 128 characters, no `@`, at most 3, no two the same |
| Claude one-liner | 200 characters |
| Claude description | 2,000 characters |
| Skill description | 1,024 characters |
| Skill name | 64 characters; `linear-a-lexicon:` plus the name also within 64 |
| Plugin README | at least 40 words outside code blocks |

The limits are written in `listing.json` under `limits` and again in the test, which does not read them from the
file it checks.

## Wording rules

- Every description, the plugin's README and the skill say "proposed": the readings are Tom di Mino's proposals.
- No string says Linear A is deciphered, decoded, cracked or solved. The word "deciphered" may stand only in the
  question a user asks ("Is Linear A deciphered?", "whether Linear A is deciphered").
- No string uses the word "consensus". The copy states the reading and its tiers and gives no verdict on what the
  field agrees.
- The plugin's README keeps both install commands: `/plugin marketplace add plasma-ai/kaphtor` and
  `/plugin install linear-a-lexicon@plasma`.
- An example's `checks` says in words what is checked. It is not the tool's name.
- In the skill, a backticked lower-case word is read as a tool name and must be a tool the server has. The fields
  of a result that the skill may name are listed in the test (`FIELDS`); add a new one there.

## Changing a string

1. Change it in `package/listing.json`.
2. Change each copy named in the table above.
3. Run `uv run --with pytest pytest tests`.
