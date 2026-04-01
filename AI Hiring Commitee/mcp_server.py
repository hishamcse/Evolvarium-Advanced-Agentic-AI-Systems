"""
AI Hiring Committee — MCP server
Tools: CV parsing, job spec extraction, session storage, listing
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

server = Server("hiring-committee-tools")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="parse_cv",
            description="Extract candidate name, skills, experience level from CV text",
            inputSchema={
                "type": "object",
                "properties": {"cv_text": {"type": "string"}},
                "required": ["cv_text"],
            },
        ),
        types.Tool(
            name="extract_requirements",
            description="Extract key requirements from a job description",
            inputSchema={
                "type": "object",
                "properties": {"job_spec": {"type": "string"}},
                "required": ["job_spec"],
            },
        ),
        types.Tool(
            name="save_session",
            description="Persist a completed committee session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "data":       {"type": "object"},
                },
                "required": ["session_id", "data"],
            },
        ),
        types.Tool(
            name="list_sessions",
            description="List recent committee sessions",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    if name == "parse_cv":
        result = _parse_cv(arguments["cv_text"])
        return [types.TextContent(type="text", text=json.dumps(result))]

    elif name == "extract_requirements":
        result = _extract_requirements(arguments["job_spec"])
        return [types.TextContent(type="text", text=json.dumps(result))]

    elif name == "save_session":
        path = MEMORY_DIR / f"{arguments['session_id']}.json"
        path.write_text(json.dumps(arguments["data"], indent=2))
        return [types.TextContent(type="text", text="saved")]

    elif name == "list_sessions":
        sessions = _list_sessions()
        return [types.TextContent(type="text", text=json.dumps(sessions))]

    return [types.TextContent(type="text", text="unknown tool")]


# ── sync helpers ───────────────────────────────────────────────────────────────

def _parse_cv(text: str) -> dict:
    """Heuristic CV parser — extracts name, skills, experience."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Candidate name: usually first non-empty line or after "Name:"
    name = ""
    for line in lines[:5]:
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line):
            name = line
            break
        if line.lower().startswith("name:"):
            name = line.split(":", 1)[1].strip()
            break

    # Experience: look for year patterns
    year_patterns = re.findall(r'(\d+)\+?\s*years?', text, re.IGNORECASE)
    exp_years = max((int(y) for y in year_patterns), default=0)
    if exp_years >= 10:
        seniority = "Senior / Principal"
    elif exp_years >= 5:
        seniority = "Mid-level"
    elif exp_years >= 2:
        seniority = "Junior / Mid"
    else:
        seniority = "Entry level"

    # Skills: common tech keywords
    skill_keywords = [
        "python","javascript","typescript","java","go","rust","c++","react","node",
        "django","fastapi","sql","postgresql","mysql","mongodb","redis","docker",
        "kubernetes","aws","gcp","azure","terraform","ci/cd","machine learning",
        "deep learning","nlp","data science","product management","agile","scrum",
        "leadership","communication","figma","ux","design","analytics","spark",
        "kafka","microservices","api","rest","graphql",
    ]
    found = [s for s in skill_keywords if s in text.lower()]

    return {
        "candidate_name": name or "Candidate",
        "experience":     f"{exp_years}+ years — {seniority}" if exp_years else seniority,
        "skills":         found[:15],
    }


def _extract_requirements(job_spec: str) -> dict:
    """Extract key requirements from job description."""
    lines = [l.strip() for l in job_spec.splitlines() if l.strip()]
    reqs = []

    in_req_section = False
    for line in lines:
        lo = line.lower()
        if any(kw in lo for kw in ["requirement", "qualification", "must have", "you will need", "we expect"]):
            in_req_section = True
            continue
        if in_req_section:
            if line.startswith(("-", "•", "*", "·")) or (len(line) > 10 and not line.endswith(":")):
                reqs.append(line.lstrip("-•*· "))
            if len(reqs) >= 8:
                break

    # Fallback: grab bullet points anywhere
    if not reqs:
        for line in lines:
            if line.startswith(("-", "•", "*", "·")) and len(line) > 15:
                reqs.append(line.lstrip("-•*· "))
            if len(reqs) >= 8:
                break

    return {"requirements": reqs[:8] or ["See job description"]}


def _list_sessions() -> list[dict]:
    sessions = []
    for p in sorted(MEMORY_DIR.glob("*.json"), reverse=True)[:20]:
        try:
            d = json.loads(p.read_text())
            sessions.append({
                "session_id":     d.get("session_id"),
                "candidate_name": d.get("candidate_name", "Unknown"),
                "role_title":     d.get("role_title", "Unknown role"),
                "decision":       d.get("decision", ""),
                "overall_score":  d.get("overall_score", 0),
            })
        except Exception:
            pass
    return sessions


# Public sync wrappers for graph nodes
def parse_cv_sync(cv_text: str) -> dict:
    return _parse_cv(cv_text)

def extract_requirements_sync(job_spec: str) -> dict:
    return _extract_requirements(job_spec)

def save_session_sync(session_id: str, data: dict) -> None:
    path = MEMORY_DIR / f"{session_id}.json"
    path.write_text(json.dumps(data, indent=2))

def list_sessions_sync() -> list[dict]:
    return _list_sessions()

def load_session_sync(session_id: str) -> dict | None:
    path = MEMORY_DIR / f"{session_id}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None


if __name__ == "__main__":
    import asyncio
    async def main():
        async with stdio_server() as (r, w):
            await server.run(r, w, server.create_initialization_options())
    asyncio.run(main())