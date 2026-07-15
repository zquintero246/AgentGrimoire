"""Validation and integration tests for the whole spellbook.

Three layers: every manifest is well-formed; the entire tree loads
through sanctum-engine's ``Tome.load_from_directory``; and every spell
executes against sample inputs (plus one ReAct end-to-end with a scripted
oracle). Run with: pip install -r requirements-dev.txt && pytest
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
MANIFESTS = sorted(ROOT.glob("*/*/spell.json"))

EXPECTED_SPELLS = {
    "calculate",
    "current_datetime",
    "http_fetch",
    "list_directory",
    "read_text",
    "regex_extract",
    "word_count",
}


def spell_id(manifest_path: Path) -> str:
    return f"{manifest_path.parent.parent.name}/{manifest_path.parent.name}"


def load_tome():
    from sanctum import Tome

    return Tome.load_from_directory(ROOT)


# --- manifests ---------------------------------------------------------------


def test_grimoire_is_not_empty() -> None:
    assert len(MANIFESTS) >= len(EXPECTED_SPELLS)


@pytest.mark.parametrize("manifest_path", MANIFESTS, ids=spell_id)
def test_manifest_is_well_formed(manifest_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest.get("name"), "manifest requires a non-empty 'name'"
    assert manifest["name"] == manifest_path.parent.name, (
        "the spell folder must be named after the spell"
    )
    assert manifest.get("description"), "manifest requires a 'description'"

    file_name, separator, attribute = manifest.get("entrypoint", "").partition(":")
    assert separator and attribute, "entrypoint must be '<file>.py:<function>'"
    assert (manifest_path.parent / file_name).is_file(), "entrypoint file missing"

    parameters = manifest.get("parameters")
    assert parameters is not None, "manifests here declare parameters explicitly"
    assert parameters.get("type") == "object"
    assert isinstance(parameters.get("properties", {}), dict)
    assert isinstance(parameters.get("required", []), list)


# --- loading through sanctum-engine ------------------------------------------


def test_tome_loads_the_whole_grimoire() -> None:
    tome = load_tome()
    names = {entry.name for entry in tome}
    assert EXPECTED_SPELLS <= names


# --- execution ----------------------------------------------------------------

EXECUTION_SAMPLES = [
    ("word_count", {"text": "lux aeterna"}, lambda r: r["words"] == 2),
    (
        "regex_extract",
        {"pattern": r"\d+", "text": "born 1877, died 1907"},
        lambda r: r == ["1877", "1907"],
    ),
    ("calculate", {"expression": "(2 + 3) * sqrt(16)"}, lambda r: r == 20.0),
    (
        "read_text",
        {"path": str(ROOT / "README.md"), "max_bytes": 4096},
        lambda r: "AgentGrimoire" in r["text"],
    ),
    (
        "list_directory",
        {"path": str(ROOT)},
        lambda r: any(entry["name"] == "README.md" for entry in r),
    ),
    ("current_datetime", {"timezone": "utc"}, lambda r: "T" in r and "+00:00" in r),
]


@pytest.mark.parametrize(
    ("name", "arguments", "check"),
    EXECUTION_SAMPLES,
    ids=[sample[0] for sample in EXECUTION_SAMPLES],
)
async def test_spell_executes(name, arguments, check) -> None:
    tome = load_tome()
    result = await tome.get(name).execute(arguments)
    assert check(result), f"{name} returned {result!r}"


async def test_http_fetch_rejects_private_hosts_offline() -> None:
    from sanctum.grimoire import SpellExecutionError

    tome = load_tome()
    with pytest.raises(SpellExecutionError, match="private"):
        await tome.get("http_fetch").execute({"url": "http://127.0.0.1/anything"})


async def test_errors_are_agent_readable() -> None:
    """Failures must carry messages a model can act on (self-correction)."""
    from sanctum.grimoire import SpellExecutionError

    tome = load_tome()
    with pytest.raises(SpellExecutionError, match="Invalid regular expression"):
        await tome.get("regex_extract").execute({"pattern": "(", "text": "x"})
    with pytest.raises(SpellExecutionError, match="allowed functions"):
        await tome.get("calculate").execute({"expression": "__import__('os')"})
    with pytest.raises(SpellExecutionError, match="No file at"):
        await tome.get("read_text").execute({"path": str(ROOT / "missing.txt")})


# --- end-to-end with a summoned entity ----------------------------------------


async def test_summoned_entity_casts_from_the_grimoire() -> None:
    from sanctum import summon
    from sanctum.oracle import OracleResponse, ScriptedOracle, SpellCall

    oracle = ScriptedOracle(
        [
            OracleResponse(
                text="",
                spell_calls=[
                    SpellCall(
                        spell="calculate",
                        arguments={"expression": "6 * 7"},
                        call_id="c1",
                    )
                ],
            ),
            OracleResponse(text="The answer is 42."),
        ]
    )
    entity = summon(oracle, load_tome())

    result = await entity.ainvoke(
        {"messages": [{"role": "user", "content": "What is 6 times 7?"}]}
    )
    messages = result["messages"]
    assert messages[2]["content"] == "42"
    assert messages[-1]["content"] == "The answer is 42."
