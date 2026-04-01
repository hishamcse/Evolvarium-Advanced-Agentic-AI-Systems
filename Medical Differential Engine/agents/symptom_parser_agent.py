"""
Symptom Parser Agent — Layer 0 of the Bayesian cascade.
Converts raw clinical text into structured, machine-readable features.
Does NOT generate diagnoses — purely structural extraction.
"""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a clinical informaticist specialising in symptom feature extraction.
Your ONLY job is to parse unstructured clinical text into a clean, structured JSON object.
You do NOT diagnose. You do NOT suggest treatments.

Extract and return ONLY valid JSON:
{
  "onset": "<acute/subacute/chronic — duration if stated>",
  "location": ["<anatomical locations mentioned>"],
  "character": ["<quality descriptors: sharp, dull, burning, throbbing, etc.>"],
  "severity": "<1-10 scale if stated, else mild/moderate/severe>",
  "timing": "<constant/intermittent/positional/exertional>",
  "modifying_factors": {
    "better": ["<what relieves it>"],
    "worse": ["<what aggravates it>"]
  },
  "associated_symptoms": ["<every additional symptom mentioned>"],
  "red_flag_features": ["<any EMERGENCY warning signs: chest pain, syncope, focal neuro, haemoptysis, etc.>"],
  "vital_abnormalities": ["<any abnormal vital signs with values>"],
  "risk_factors": ["<relevant history, meds, social factors that modify risk>"],
  "excluded_features": ["<things explicitly absent that are clinically important>"],
  "system_review": {
    "cardiovascular": "<pos/neg/unknown>",
    "respiratory": "<pos/neg/unknown>",
    "gastrointestinal": "<pos/neg/unknown>",
    "neurological": "<pos/neg/unknown>",
    "musculoskeletal": "<pos/neg/unknown>",
    "genitourinary": "<pos/neg/unknown>",
    "dermatological": "<pos/neg/unknown>",
    "constitutional": "<pos/neg/unknown>"
  }
}"""


def run_symptom_parser(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=0.1,
    )

    prompt = f"""Patient: {state.get('patient_age', 'Unknown age')}, {state.get('patient_sex', 'Unknown sex')}
Chief complaint: {state.get('chief_complaint', 'Not provided')}

SYMPTOMS:
{state.get('symptoms', 'None documented')}

VITALS:
{state.get('vitals', 'Not provided')}

HISTORY:
{state.get('history', 'None documented')}

EXAMINATION:
{state.get('exam_findings', 'None documented')}

Extract structured clinical features. Return JSON only."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    features = _parse(resp.content)
    return {"parsed_features": features}


def _parse(text: str) -> dict:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        return json.loads(clean)
    except Exception:
        return {
            "onset": "unknown", "location": [], "character": [],
            "severity": "unknown", "timing": "unknown",
            "modifying_factors": {"better": [], "worse": []},
            "associated_symptoms": [], "red_flag_features": [],
            "vital_abnormalities": [], "risk_factors": [],
            "excluded_features": [], "system_review": {},
        }