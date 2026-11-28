# Submitting to the directories

The steps of each directory's submission, and the answers that are written nowhere else. Every listing string
(name, publisher, addresses, descriptions, test cases) is in `package/listing.json` and the manifests
([copy.md](copy.md)); this page repeats none of them.

The server is public and asks for no sign-in, so neither review needs a test account.

## Claude

Portal: `claude.ai/directory/manage`, on a paid Claude plan. Two submissions.

### The MCP connector

Submit new, MCP connector, and paste the `server` address from `listing.json`. The tools sync from the server.

- Authentication: not required.
- Slug: `slug` in `listing.json`. It is permanent once published.
- One-liner, description and categories: under `anthropic` in `listing.json`. The use cases the form asks for
  are the five `examples`.
- Documentation, support and privacy addresses: `documentation`, `support`, `privacy`.
- Reads or writes: reads only.
- Data handling: the server is the publisher's own, handles no health data, and shows no sponsored content.
- Test and launch: confirm that every tool was run, in MCP Inspector or as a custom connector in Claude.
- The form also asks for a company name, a primary contact and its compliance acknowledgements.

### The plugin

1. Connect a GitHub account to claude.ai in the organization that submits. The account needs push access to the
   repository. The Claude GitHub App is needed only if the portal says it cannot reach the repository.
2. Submit new, plugin bundle. Repository: `plasma-ai/linear-a-plugin`. Plugin path: `linear-a-lexicon`.
3. The listing is read from `.claude-plugin/plugin.json` and the plugin's README, not typed.
4. The form asks the data-handling questions, a contact email and its acknowledgements.

`claude plugin validate linear-a-lexicon` passes locally; the portal's own Validate checks more.

## ChatGPT

The submitter is an owner of the OpenAI organization, or has Apps Management Write. The project's data residency
is global, not EU.

1. **Verify identity.** Individual verification in the organization settings. The directory shows that
   identity's name whatever the manifest says, and the public pages must name the same publisher.
2. **Upload the zip.** This creates the draft. The zip is the file attached to the latest GitHub release, or
   `python3 package/pack_chatgpt.py OUT_DIR` with OUT_DIR outside `linear-a-lexicon/`. The descriptions, the
   starter prompts (`defaultPrompt`), the test cases and the release notes are imported from the zip's
   `plugin.json`; the imported test cases cannot be edited in the dashboard.
3. **Connect the server.** Under MCPs, connect the server and complete the domain challenge the portal shows:
   an exact token, served as plain text to a GET at `/.well-known/openai-apps-challenge` on the server's host
   or an allowed parent host. The server answers no such path yet; the route is added in the site repository
   (`plasma-internal/linear-a`, `apps/mcp`) once the portal gives the token. Then run the tool scan.
4. **Justify the tool hints.** The form asks for a reason for each hint on each tool: see below.
5. **Review details.** Country availability, and a demo recording that shows the test cases across the
   supported platforms, at an address a reviewer can open.
6. **Submit** with the policy attestations, then publish once approved.

## Tool hint justifications

Every tool carries the same hints: read-only, not destructive, not open-world.

For the lookup tools (every tool but the three kernel tools):

- **Read-only.** The tool looks up records of one published edition of the Lexicon, packed into the server when
  it is deployed. It creates, changes and deletes nothing, on the server or elsewhere.
- **Not destructive.** Nothing is written, so nothing can be lost.
- **Not open-world.** The tool reads the Lexicon's own records and calls no other system: no web search, no
  third-party API, no account of the user's.

For `kernel_summary`, `run_anchor_kernel` and `run_ligature_kernel`:

- **Read-only.** The tool computes on fixed data held in the server's code and returns the result. It stores
  nothing.
- **Not destructive.** Nothing is written, so nothing can be lost.
- **Not open-world.** The computation runs inside the server and calls no other system.

What each tool returns, where a form asks tool by tool. When the server's tools change, change this table too.

| Tool | What it returns |
|---|---|
| `search` | Lexicon records and wiki pages that match a query: their ids, titles and addresses. |
| `fetch` | One Lexicon record or page, by the id a search gave. |
| `get_lexicon_overview` | What the Lexicon is, its tiers, its counts, how to cite it and its latest release. |
| `get_word` | One word's proposed reading, tier, first proposer, evidence and rival readings. |
| `get_name` | One name: whether a person, place, god or title, with its proposed reading and tier. |
| `get_text` | The document or documents a number names, with the proposed translation and the page's address. |
| `get_root` | One Proto-Semitic root, its meaning, and the Linear A readings built on it. |
| `get_sign` | One sign, how it is read, and the Lexicon words written with it. |
| `list_words` | The Lexicon's words that fit the filters given (tier, word type, language family, site and others). |
| `list_texts` | The documents that fit the filters given (site, object, scribe, whether a translation is proposed). |
| `list_names` | The names that fit the filters given (type, language, site). |
| `find_words_compared_with` | The words the Lexicon compares with a given form of another language. |
| `find_words_by_signs` | The word forms that hold given signs at a given place; it says which forms it did not search. |
| `list_occurrences` | The documents in which one word stands. |
| `list_values` | The values in use for a filter of the list tools, with counts. |
| `kernel_summary` | The scoreboard of the language-identification kernels, as held in the server's code. |
| `run_anchor_kernel` | Kernel D's permutation test; the same arguments, seed included, give the same result. |
| `run_ligature_kernel` | Kernel F's permutation test; the same arguments, seed included, give the same result. |

## What the server receives

A tool call carries the arguments the model sends (a word, a document number, a query, signs, filters). The
server asks for no sign-in, sets no cookie, returns no data about the user and writes nothing to any store. It
logs only its own faults, to the hosting platform's log; the platform keeps its usual request logs.
