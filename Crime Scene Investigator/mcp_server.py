"""
Crime Scene Investigator — MCP server
Tools: case management, evidence tagging, timeline extraction, alibi check
Run standalone: python mcp_server.py
"""
import json
import re
import uuid
from pathlib import Path

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

BASE_DIR   = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

server = Server("csi-tools")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="create_case",
            description="Create and persist a new investigation case",
            inputSchema={
                "type": "object",
                "properties": {
                    "title":       {"type": "string"},
                    "brief":       {"type": "string"},
                    "evidence":    {"type": "string"},
                },
                "required": ["title", "brief", "evidence"],
            },
        ),
        types.Tool(
            name="tag_evidence",
            description="Classify evidence items by type: physical, witness, circumstantial, digital",
            inputSchema={
                "type": "object",
                "properties": {"evidence_text": {"type": "string"}},
                "required": ["evidence_text"],
            },
        ),
        types.Tool(
            name="extract_timeline",
            description="Extract chronological events mentioned in a case brief",
            inputSchema={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        ),
        types.Tool(
            name="check_contradictions",
            description="Find logical contradictions between prosecution and defense arguments",
            inputSchema={
                "type": "object",
                "properties": {
                    "prosecution": {"type": "string"},
                    "defense":     {"type": "string"},
                },
                "required": ["prosecution", "defense"],
            },
        ),
        types.Tool(
            name="list_cases",
            description="List all saved investigation cases",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    if name == "create_case":
        case_id = uuid.uuid4().hex[:10]
        data = {
            "case_id":  case_id,
            "title":    arguments["title"],
            "brief":    arguments["brief"],
            "evidence": arguments["evidence"],
        }
        (MEMORY_DIR / f"{case_id}.json").write_text(json.dumps(data, indent=2))
        return [types.TextContent(type="text", text=case_id)]

    elif name == "tag_evidence":
        lines  = [l.strip() for l in arguments["evidence_text"].splitlines() if l.strip()]
        tagged = []
        for item in lines:
            lo = item.lower()
            if any(w in lo for w in ["witness", "saw", "heard", "testified", "said"]):
                tag = "WITNESS"
            elif any(w in lo for w in ["fingerprint", "dna", "blood", "weapon", "tool", "fibre", "hair"]):
                tag = "PHYSICAL"
            elif any(w in lo for w in ["phone", "camera", "cctv", "email", "digital", "log", "record"]):
                tag = "DIGITAL"
            else:
                tag = "CIRCUMSTANTIAL"
            tagged.append(f"[{tag}] {item}")
        return [types.TextContent(type="text", text="\n".join(tagged))]

    elif name == "extract_timeline":
        text   = arguments["text"]
        # simple time-pattern extraction
        times  = re.findall(
            r"(?:at\s+)?(\d{1,2}[:.]\d{2}\s*(?:am|pm)?|\d{1,2}\s*(?:am|pm)|"
            r"(?:morning|afternoon|evening|night|midnight|noon))[^.]*\.",
            text, re.IGNORECASE
        )
        if times:
            result = "Extracted timeline events:\n" + "\n".join(f"- {t.strip()}" for t in times[:10])
        else:
            result = "No explicit timestamps found. Narrative appears non-chronological."
        return [types.TextContent(type="text", text=result)]

    elif name == "check_contradictions":
        p_words = set(arguments["prosecution"].lower().split())
        d_words = set(arguments["defense"].lower().split())
        # look for direct negation pairs
        negations = [
            ("was",    "was not"),
            ("did",    "did not"),
            ("could",  "could not"),
            ("would",  "would not"),
            ("present","absent"),
            ("guilty", "innocent"),
        ]
        found = []
        for pos, neg in negations:
            if pos in p_words and neg.replace(" ","") in " ".join(d_words):
                found.append(f"Contradiction: prosecution asserts '{pos}', defense asserts '{neg}'")
        result = "\n".join(found) if found else "No explicit logical contradictions detected — debate is on interpretation of facts."
        return [types.TextContent(type="text", text=result)]

    elif name == "list_cases":
        cases = []
        for p in sorted(MEMORY_DIR.glob("*.json"), reverse=True)[:15]:
            try:
                d = json.loads(p.read_text())
                cases.append(f"{d['case_id']} — {d['title']}")
            except Exception:
                pass
        result = "\n".join(cases) if cases else "No cases on file."
        return [types.TextContent(type="text", text=result)]

    return [types.TextContent(type="text", text="Unknown tool")]


if __name__ == "__main__":
    import asyncio

    async def main():
        async with stdio_server() as (r, w):
            await server.run(r, w, server.create_initialization_options())

    asyncio.run(main())