"""
Medical Differential Engine — MCP server
Tools: symptom lookup, ICD coding, drug interaction check, case management
Run standalone: python mcp_server.py
"""
import json
import uuid
from pathlib import Path

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

BASE_DIR   = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

server = Server("mde-tools")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="lookup_red_flags",
            description="Return emergency red flag symptoms for a given chief complaint",
            inputSchema={
                "type": "object",
                "properties": {"chief_complaint": {"type": "string"}},
                "required": ["chief_complaint"],
            },
        ),
        types.Tool(
            name="icd_hint",
            description="Return ICD-10 code hints for a diagnosis name",
            inputSchema={
                "type": "object",
                "properties": {"diagnosis": {"type": "string"}},
                "required": ["diagnosis"],
            },
        ),
        types.Tool(
            name="drug_interaction_check",
            description="Check for clinically significant drug interactions from a medication list",
            inputSchema={
                "type": "object",
                "properties": {"medications": {"type": "string", "description": "Comma-separated list"}},
                "required": ["medications"],
            },
        ),
        types.Tool(
            name="save_case",
            description="Save a differential diagnosis case to persistent memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "case_id": {"type": "string"},
                    "data":    {"type": "string", "description": "JSON string of case data"},
                },
                "required": ["data"],
            },
        ),
        types.Tool(
            name="list_cases",
            description="List all saved differential diagnosis cases",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="load_case",
            description="Load a saved case by ID",
            inputSchema={
                "type": "object",
                "properties": {"case_id": {"type": "string"}},
                "required": ["case_id"],
            },
        ),
    ]


# ── Red flags database (simplified) ──────────────────────────────────────────
RED_FLAG_DB = {
    "chest pain": [
        "Diaphoresis (sweating)", "Radiation to arm/jaw/back", "Associated dyspnoea",
        "Syncope or near-syncope", "Tearing/ripping quality (aortic dissection)",
        "New ST-segment changes", "Haemodynamic instability",
    ],
    "headache": [
        "Thunderclap onset (worst headache of life)", "Fever + neck stiffness (meningism)",
        "Focal neurological deficit", "Papilloedema", "Age >50 new headache",
        "Progressive worsening over weeks", "Associated with vomiting and drowsiness",
    ],
    "abdominal pain": [
        "Peritonism (guarding/rigidity)", "Haemodynamic instability", "Pulsatile abdominal mass",
        "Haematemesis or melaena", "Bilious vomiting", "Absent bowel sounds",
        "Pregnancy with pain (ectopic)", "Immunocompromised patient",
    ],
    "dyspnoea": [
        "SpO2 < 92%", "Respiratory rate > 30", "Accessory muscle use",
        "Cyanosis", "Altered consciousness", "Haemoptysis",
        "Unilateral absent breath sounds (pneumothorax)",
    ],
    "default": [
        "Haemodynamic instability (BP <90, HR >120)", "Altered mental status",
        "Fever >39°C or hypothermia <36°C", "Signs of sepsis",
        "Acute focal neurological deficit",
    ],
}

ICD_HINTS = {
    "acute myocardial infarction": "I21", "angina": "I20", "aortic dissection": "I71",
    "pulmonary embolism": "I26", "pneumothorax": "J93", "pneumonia": "J18",
    "meningitis": "G03", "subarachnoid haemorrhage": "I60", "stroke": "I63",
    "appendicitis": "K37", "pancreatitis": "K85", "ectopic pregnancy": "O00",
    "sepsis": "A41", "diabetic ketoacidosis": "E11.1", "hypertensive emergency": "I10",
    "anaphylaxis": "T78.2", "heart failure": "I50", "atrial fibrillation": "I48",
}


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    if name == "lookup_red_flags":
        cc = arguments.get("chief_complaint", "").lower()
        flags = RED_FLAG_DB.get(cc, RED_FLAG_DB["default"])
        result = {"chief_complaint": cc, "red_flags": flags}
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "icd_hint":
        dx = arguments.get("diagnosis", "").lower()
        code = next((v for k, v in ICD_HINTS.items() if k in dx or dx in k), "Unknown")
        return [types.TextContent(type="text", text=json.dumps({"diagnosis": dx, "icd": code}))]

    elif name == "drug_interaction_check":
        meds = [m.strip().lower() for m in arguments.get("medications", "").split(",")]
        interactions = []
        # Simplified interaction checks
        pairs = [
            ({"warfarin", "aspirin"}, "Warfarin + Aspirin: increased bleeding risk"),
            ({"metformin", "contrast"}, "Metformin + IV contrast: lactic acidosis risk — hold metformin"),
            ({"ssri", "maoi"}, "SSRI + MAOI: serotonin syndrome — DANGEROUS"),
            ({"ace inhibitor", "potassium"}, "ACE inhibitor + K+ supplements: hyperkalaemia risk"),
            ({"digoxin", "amiodarone"}, "Digoxin + Amiodarone: digoxin toxicity risk"),
        ]
        for drug_set, warning in pairs:
            if any(d in " ".join(meds) for d in drug_set):
                if len([d for d in drug_set if any(d in m for m in meds)]) >= 1:
                    interactions.append(warning)
        return [types.TextContent(type="text", text=json.dumps({"interactions": interactions}))]

    elif name == "save_case":
        case_id = arguments.get("case_id") or uuid.uuid4().hex[:10]
        data = json.loads(arguments.get("data", "{}"))
        data["case_id"] = case_id
        (MEMORY_DIR / f"{case_id}.json").write_text(json.dumps(data, indent=2))
        return [types.TextContent(type="text", text=json.dumps({"saved": case_id}))]

    elif name == "list_cases":
        cases = []
        for p in sorted(MEMORY_DIR.glob("*.json"), reverse=True)[:20]:
            try:
                d = json.loads(p.read_text())
                cases.append({
                    "case_id": d.get("case_id", p.stem),
                    "chief_complaint": d.get("chief_complaint", ""),
                    "patient_age": d.get("patient_age", ""),
                    "disposition": d.get("disposition", ""),
                })
            except Exception:
                pass
        return [types.TextContent(type="text", text=json.dumps({"cases": cases}))]

    elif name == "load_case":
        path = MEMORY_DIR / f"{arguments['case_id']}.json"
        if path.exists():
            return [types.TextContent(type="text", text=path.read_text())]
        return [types.TextContent(type="text", text=json.dumps({"error": "Not found"}))]

    return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


# ── sync wrappers ──────────────────────────────────────────────────────────────
# Used by graph.py to call MCP tools synchronously

import asyncio

def _run(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())