"""Compare mcp-contract.json with the running server's own answers. Reads only.

    python3 package/check_contract.py [URL]            # exit 0 they match, 1 they differ, 2 the server did not answer
    python3 package/check_contract.py --print [URL]    # the server's answers as JSON, in the copy's shape

Asks the server (default: the address in listing.json) for `initialize` and every page of `tools/list`, and reports
what differs from the copy: the protocol version, the capabilities, the server's name and version, its instructions,
tools added, gone or listed twice, and for a changed tool the keys that changed. The tests read the copy and never the
network, so this is how drift between the two is found. To take the server's new answers, redirect `--print` into
mcp-contract.json.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent
PROTOCOL = "2025-06-18"
AGENT = "linear-a-lexicon-contract-check"  # names the project and nothing else
HEADS = ("protocolVersion", "capabilities", "server")


def ask(url: str, method: str, params: dict[str, Any]) -> dict[str, Any]:
    """One JSON-RPC call. A server may answer in JSON or as an event stream; an error answer raises."""
    request = urllib.request.Request(
        url, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
        headers={"content-type": "application/json", "accept": "application/json, text/event-stream",
                 "mcp-protocol-version": PROTOCOL, "user-agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")
        if response.headers.get_content_type() == "text/event-stream":
            data = [line[5:].strip() for line in text.splitlines() if line.startswith("data:")]
            if not data:
                raise RuntimeError(f"{method}: an event stream with no data")
            text = data[-1]
    body = json.loads(text)
    if "result" not in body:
        raise RuntimeError(f"{method}: {body.get('error', body)}")
    return body["result"]


def live_contract(url: str) -> dict[str, Any]:
    """The server's answers in the shape of mcp-contract.json."""
    started = ask(url, "initialize", {"protocolVersion": PROTOCOL, "capabilities": {},
                                      "clientInfo": {"name": AGENT, "version": "1"}})
    tools: list[dict[str, Any]] = []
    cursor = None
    while True:
        page = ask(url, "tools/list", {"cursor": cursor} if cursor else {})
        tools += page["tools"]
        cursor = page.get("nextCursor")
        if not cursor:
            break
    return {"protocolVersion": started.get("protocolVersion"), "capabilities": started.get("capabilities", {}),
            "server": started["serverInfo"], "instructions": started.get("instructions"), "tools": tools}


def compare(copy: dict[str, Any], live: dict[str, Any]) -> list[str]:
    """What differs between the copy and the server's answers, one line each. No network."""
    found = [f"{key}: {json.dumps(copy.get(key), ensure_ascii=False)} in the copy, "
             f"{json.dumps(live.get(key), ensure_ascii=False)} live"
             for key in HEADS if copy.get(key) != live.get(key)]
    if copy.get("instructions") != live.get("instructions"):
        found.append("instructions differ")
    names = [tool["name"] for tool in live["tools"]]
    found += [f"tool listed twice live: {name}" for name in sorted({n for n in names if names.count(n) > 1})]
    have = {tool["name"]: tool for tool in copy["tools"]}
    now = {tool["name"]: tool for tool in live["tools"]}
    found += [f"new tool: {name}" for name in sorted(set(now) - set(have))]
    found += [f"tool gone: {name}" for name in sorted(set(have) - set(now))]
    for name in sorted(set(have) & set(now)):
        keys = sorted(key for key in have[name].keys() | now[name].keys() if have[name].get(key) != now[name].get(key))
        if keys:
            found.append(f"tool changed: {name} ({', '.join(keys)})")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", nargs="?", help="the server's address (default: the one in listing.json)")
    parser.add_argument("--print", action="store_true", dest="show",
                        help="print the server's answers and compare nothing")
    args = parser.parse_args()
    url = args.url or json.loads((PACKAGE / "listing.json").read_text("utf-8"))["server"]
    try:
        live = live_contract(url)
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"{url} did not answer: {error}", file=sys.stderr)
        return 2
    if args.show:
        print(json.dumps(live, indent=2, ensure_ascii=False))
        return 0
    drift = compare(json.loads((PACKAGE / "mcp-contract.json").read_text("utf-8")), live)
    print("\n".join(drift) if drift else f"mcp-contract.json matches {url}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
