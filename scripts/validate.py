#!/usr/bin/env python3
"""Validate the portable parts of the Watasu plugin without external packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "watasu"
SKILL = PLUGIN / "skills" / "watasu" / "SKILL.md"
REFERENCE_DIR = SKILL.parent / "references"


def load_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise AssertionError(f"invalid JSON in {relative_path}: {error}") from error


def validate_manifests() -> None:
    claude_market = load_json(".claude-plugin/marketplace.json")
    codex_market = load_json(".agents/plugins/marketplace.json")
    claude_plugin = load_json("plugins/watasu/.claude-plugin/plugin.json")
    codex_plugin = load_json("plugins/watasu/.codex-plugin/plugin.json")
    mcp = load_json("plugins/watasu/.mcp.json")

    assert claude_market["name"] == "watasu"
    assert len(claude_market["plugins"]) == 1
    assert claude_market["plugins"][0]["source"] == "./plugins/watasu"
    assert len(codex_market["plugins"]) == 1
    assert codex_market["plugins"][0]["source"]["path"] == "./plugins/watasu"
    assert claude_plugin["name"] == codex_plugin["name"] == "watasu"
    assert claude_plugin["version"] == codex_plugin["version"]
    assert claude_market["plugins"][0]["version"] == claude_plugin["version"]
    assert mcp == {
        "mcpServers": {
            "watasu": {
                "type": "http",
                "url": "https://mcp.watasu.io/mcp",
            }
        }
    }


def validate_skill() -> None:
    text = SKILL.read_text()
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    parts = text.split("---\n", 2)
    assert len(parts) == 3, "SKILL.md must close its YAML frontmatter"
    frontmatter = parts[1]
    assert re.search(r"(?m)^name: watasu$", frontmatter)
    assert re.search(r"(?m)^description:(?: .+)?$", frontmatter)

    references = sorted(REFERENCE_DIR.glob("*.md"))
    assert len(references) >= 30, "the handbook needs focused, swallowable chapters"

    reachable = {SKILL.resolve()}
    pending = [SKILL.resolve()]
    while pending:
        path = pending.pop()
        contents = path.read_text()
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", contents):
            if target.startswith(("https://", "http://", "#")):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if resolved.suffix == ".md" and resolved not in reachable:
                reachable.add(resolved)
                pending.append(resolved)

    for reference in references:
        assert reference.resolve() in reachable, (
            f"handbook does not route to {reference.relative_to(SKILL.parent)}"
        )

    for path in [SKILL, *references, ROOT / "README.md"]:
        contents = path.read_text()
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", contents):
            if target.startswith(("https://", "http://", "#")):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            assert resolved.exists(), f"broken link in {path.relative_to(ROOT)}: {target}"
        assert "\t" not in contents, f"tab found in {path.relative_to(ROOT)}"
        assert not any(line.endswith(" ") for line in contents.splitlines()), (
            f"trailing whitespace found in {path.relative_to(ROOT)}"
        )

    source_map = (REFERENCE_DIR / "source-map.md").read_text()
    public_doc_urls = set(
        re.findall(r"https://docs\.watasu\.io(?:/[^)\s]*)?", source_map)
    )
    assert len(public_doc_urls) >= 45, "source map must retain full public-doc coverage"

    combined = "\n".join(path.read_text() for path in [SKILL, *references])
    for required in [
        "METRICS_PORT",
        "apply_diff",
        "applyDiff",
        "numeric non-root",
        "TURN_SHARED_SECRET",
        "box.watasu.io",
        "Idempotency-Key",
        "watasu --version",
        "sandbox_quota_exceeded",
        "pg backups download",
        "Retry-After",
    ]:
        assert required in combined, f"handbook is missing required contract: {required}"

    coverage = (REFERENCE_DIR / "coverage.md").read_text()
    covered_urls = set(re.findall(r"https://docs\.watasu\.io(?:/[^)\s]*)?", coverage))
    assert public_doc_urls <= covered_urls, "coverage map must route every source-map documentation URL"

    mcp_resources = set((REFERENCE_DIR / "mcp.md").read_text().splitlines())
    for uri in [
        "watasu://overview", "watasu://whoami", "watasu://teams",
        "watasu://apps", "watasu://apps/status", "watasu://apps/{name}",
        "watasu://teams/{team}/apps", "watasu://addons/{name}",
        "watasu://apps/{app}/addons", "watasu://apps/{app}/process-types",
        "watasu://apps/{app}/releases/latest", "watasu://apps/{app}/builds",
        "watasu://apps/{app}/builds?limit={limit}",
        "watasu://apps/{app}/builds/latest", "watasu://apps/{app}/builds/{number}",
        "watasu://apps/{app}/builds/{number}/logs",
        "watasu://apps/{app}/builds/{number}/logs?limit={limit}",
        "watasu://apps/{app}/builds/{number}/raw-output",
        "watasu://apps/{app}/builds/{number}/raw-output?lines={lines}",
    ]:
        assert uri in mcp_resources, f"MCP reference missing resource: {uri}"


def main() -> int:
    try:
        validate_manifests()
        validate_skill()
    except (AssertionError, OSError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print("Watasu plugin validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
