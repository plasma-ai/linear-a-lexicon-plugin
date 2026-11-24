"""The Linear A Lexicon plugin as the two directories will read it.

Each listing string is within its host's limit and said once, the two manifests agree with each other and with the
listing, both point at the one server, and the skill names exactly the tools the server has, read from the contract
copy. No test here reaches the network: `package/check_contract.py` compares that copy with the running server, and
its comparison is tested here on made-up answers. The one file written is the zip, into pytest's tmp_path.
"""
import copy
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path

import pytest

sys.dont_write_bytecode = True  # loading the two scripts below leaves no __pycache__ in package/

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "linear-a-lexicon"
PACKAGE = REPO / "package"
SERVER = "https://mcp.linear-a.ai/mcp"
TOOLS = 18
# The hosts' limits, written here and not read from the file under test.
LIMITS = {"openai.shortDescription": 30, "anthropic.oneLiner": 200, "anthropic.description": 2000,
          "skill.description": 1024, "skill.name": 64, "readme.minWords": 40}
# Backticked words in the skill that are fields of a result and not tools; `get_` is a prefix it names.
FIELDS = {"get_", "proposed_reading", "rivals", "scribe", "standing", "summary", "tier", "tier_meaning", "url"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def script(name: str):
    spec = importlib.util.spec_from_file_location(name, PACKAGE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LISTING = load(PACKAGE / "listing.json")
CONTRACT = load(PACKAGE / "mcp-contract.json")
CLAUDE = load(PLUGIN / ".claude-plugin" / "plugin.json")
OPENAI = load(PLUGIN / "plugin.json")
EXTENSION = OPENAI["extensions"]["com.openai"]
UI = EXTENSION["interface"]
SKILL = (PLUGIN / "skills" / "reading-linear-a" / "SKILL.md").read_text(encoding="utf-8")
README = (PLUGIN / "README.md").read_text(encoding="utf-8")
assert SKILL.startswith("---\n")
FRONT = {key: value.strip() for key, value in
         (line.split(":", 1) for line in SKILL.split("---")[1].strip().splitlines())}


def tool_names() -> list[str]:
    return [tool["name"] for tool in CONTRACT["tools"]]


def test_every_listing_string_is_within_its_hosts_limit():
    assert LISTING["limits"] == LIMITS
    assert len(LISTING["openai"]["shortDescription"]) <= LIMITS["openai.shortDescription"]
    assert len(LISTING["anthropic"]["oneLiner"]) <= LIMITS["anthropic.oneLiner"]
    assert len(LISTING["anthropic"]["description"]) <= LIMITS["anthropic.description"]
    assert len(FRONT["description"]) <= LIMITS["skill.description"]
    assert len(FRONT["name"]) <= LIMITS["skill.name"]
    assert len(f"{CLAUDE['name']}:{FRONT['name']}") <= 64
    assert len(re.sub(r"```.*?```", "", README, flags=re.DOTALL).split()) >= LIMITS["readme.minWords"]
    # OpenAI's final-submission limits
    assert len(LISTING["name"]) <= 30
    assert len(LISTING["publisher"]) <= 80
    assert len(LISTING["openai"]["longDescription"]) <= 4000
    assert len(UI["capabilities"]) <= 20 and all(len(c) <= 120 and "\n" not in c for c in UI["capabilities"])
    assert len(UI["defaultPrompt"]) <= 3 and all(len(p) <= 128 and "@" not in p for p in UI["defaultPrompt"])
    assert len(set(UI["defaultPrompt"])) == len(UI["defaultPrompt"])
    assert len(LISTING["examples"]) == 5
    assert len(LISTING["negative"]) == 3


def test_the_copy_says_proposed_and_never_deciphered_as_fact():
    everything = "\n".join([json.dumps(LISTING), json.dumps(CLAUDE), json.dumps(OPENAI), SKILL, README])
    # the word stands only in the question a user asks
    allowed = r"Is Linear A deciphered|whether Linear A is deciphered"
    rest = re.sub(allowed, "", everything)
    claim = re.search(r"deciph|\bdecod|\bcrack|\bsolv", rest, flags=re.IGNORECASE)
    assert not claim, rest[max(0, claim.start() - 60):claim.end() + 60]
    for text in (LISTING["openai"]["longDescription"], LISTING["anthropic"]["oneLiner"], CLAUDE["description"],
                 README, SKILL):
        assert re.search(r"propos", text, flags=re.IGNORECASE)
    # the copy states the reading and its tiers, and passes no verdict on the field's agreement
    assert not re.search(r"consensus", "\n".join([everything, (PACKAGE / "prompts.json").read_text(encoding="utf-8")]),
                         flags=re.IGNORECASE)


def test_the_two_manifests_say_the_same_things_and_what_the_listing_says():
    for key in ("name", "version", "description", "license", "homepage", "keywords", "author"):
        assert OPENAI[key] == CLAUDE[key], key
    assert CLAUDE["name"] == LISTING["slug"]
    assert re.fullmatch(r"[a-z]+(-[a-z]+)*", CLAUDE["name"])
    assert CLAUDE["displayName"] == UI["displayName"] == LISTING["name"]
    assert CLAUDE["author"]["name"] == UI["developerName"] == LISTING["publisher"]
    assert CLAUDE["privacyPolicyUrl"] == LISTING["privacy"]
    assert UI["shortDescription"] == LISTING["openai"]["shortDescription"]
    assert UI["longDescription"] == LISTING["openai"]["longDescription"]
    assert UI["category"] == LISTING["openai"]["category"]
    assert UI["capabilities"] == LISTING["openai"]["capabilities"]
    assert [UI["websiteURL"], UI["supportURL"], UI["privacyPolicyURL"], UI["termsOfServiceURL"]] == [
        LISTING["website"], LISTING["support"], LISTING["privacy"], LISTING["terms"]]
    assert EXTENSION["publication"]["release_notes"] == LISTING["releaseNotes"]


def test_the_review_cases_are_the_listings_five_and_three_in_full():
    cases = EXTENSION["review"]["test_cases"]
    assert cases["positive"] == [
        {"description": e["checks"], "prompt": e["prompt"], "tools_triggered": e["tool"],
         "expected_behavior": e["expected"]} for e in LISTING["examples"]]
    assert cases["negative"] == [
        {"description": e["reason"], "prompt": e["prompt"], "expected_behavior": e["expected"]}
        for e in LISTING["negative"]]
    # a description says what is checked, in words, and is not the tool's name
    assert not {case["description"] for case in cases["positive"]} & set(tool_names())


def test_both_hosts_are_pointed_at_the_one_server_with_no_sign_in():
    assert LISTING["server"] == SERVER
    assert load(PLUGIN / ".mcp.json")["mcpServers"] == {"linear-a-lexicon": {"type": "http", "url": SERVER}}
    assert load(PLUGIN / "mcp.json")["mcpServers"]["linear-a-lexicon"] == {
        "type": "streamable-http", "url": SERVER, "extensions": {"com.openai": {"auth": {"type": "none"}}}}


def test_the_readme_gives_the_install_commands():
    assert "/plugin marketplace add plasma-ai/kaphtor" in README
    assert f"/plugin install {CLAUDE['name']}@plasma" in README


def test_every_path_a_manifest_names_is_a_file_in_the_plugin_and_nothing_the_chat_apps_refuse_is_there():
    for path in (UI["composerIcon"], UI["logo"], EXTENSION["onboardingSkill"]):
        target = (PLUGIN / path).resolve()
        assert path.startswith("./") and target.is_file() and PLUGIN in target.parents, path
    for name in ("README.md", "LICENSE", ".claude-plugin/plugin.json"):
        assert (PLUGIN / name).is_file(), name
    for name in ("bin", "hooks", "agents"):
        assert not (PLUGIN / name).exists(), name
    assert FRONT["name"] == "reading-linear-a"


def test_the_skill_and_the_listing_name_only_tools_the_server_has():
    have = tool_names()
    assert len(have) == len(set(have)) == TOOLS
    assert set(re.findall(r"`([a-z][a-z0-9_]*)`", SKILL)) - FIELDS == set(have)
    for prompt in load(PACKAGE / "prompts.json")["prompts"]:
        assert set(prompt["tools"]) <= set(have)
    for example in LISTING["examples"]:
        assert example["tool"] in have
    # every tool says whether it reads, reaches outside and destroys, as both directories require
    for tool in CONTRACT["tools"]:
        notes = tool["annotations"]
        assert (notes["readOnlyHint"], notes["destructiveHint"], notes["openWorldHint"]) == (True, False, False)


def test_the_golden_prompts_are_twenty_two_four_of_them_negative():
    prompts = load(PACKAGE / "prompts.json")["prompts"]
    negative = [p for p in prompts if p["kind"] == "negative"]
    assert len(prompts) == 22
    assert len(negative) == 4
    assert all(p["tools"] == [] for p in negative)


def test_the_contract_check_reports_each_kind_of_difference():
    compare = script("check_contract").compare
    assert compare(CONTRACT, copy.deepcopy(CONTRACT)) == []

    live = copy.deepcopy(CONTRACT)
    live["protocolVersion"] = "2099-01-01"
    live["capabilities"] = {"tools": {}, "prompts": {}}
    live["server"]["title"] = "Another"
    live["instructions"] += " More."
    first, second, third = live["tools"][0], live["tools"][1], live["tools"][2]
    live["tools"] = live["tools"][1:] + [copy.deepcopy(second), {"name": "new_tool"}]
    third["description"] += " Changed."
    found = compare(CONTRACT, live)

    assert sum(line.startswith(("protocolVersion:", "capabilities:", "server:")) for line in found) == 3
    assert any('"Another"' in line for line in found)
    assert "instructions differ" in found
    assert f"tool listed twice live: {second['name']}" in found
    assert "new tool: new_tool" in found
    assert f"tool gone: {first['name']}" in found
    assert f"tool changed: {third['name']} (description)" in found
    assert len(found) == 8


def test_the_chatgpt_zip_holds_the_folder_without_any_dot_file_and_is_the_same_each_time(tmp_path):
    pack = script("pack_chatgpt").pack
    one, two = pack(tmp_path / "one"), pack(tmp_path / "two")
    assert one.read_bytes() == two.read_bytes()
    with zipfile.ZipFile(one) as archive:
        listed = archive.namelist()
    assert sorted(listed) == sorted(
        f"linear-a-lexicon/{name}" for name in (
            "LICENSE", "README.md", "plugin.json", "mcp.json", "assets/icon.png", "assets/logo.png",
            "skills/reading-linear-a/SKILL.md"))
    with pytest.raises(ValueError):
        pack(PLUGIN / "assets")
    assert not (PLUGIN / "assets" / "linear-a-lexicon-chatgpt.zip").exists()
