"""Tool registry with structured output stubs.
All tools return dicts: {"tool": name, "ok": bool, "data": any, "meta": {...}}
"""
from typing import Any, Dict, Callable, List, Tuple
import os
import time

ToolFn = Callable[[Dict[str, Any]], Dict[str, Any]]

# ---- Tool Implementations (Stubs) ----

def md_lookup(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Scan markdown files in KB_PATH for query terms; return matched sections.
    Heuristic: lines starting with '#' treated as headers; sections captured until next header.
    """
    query = (payload.get("query") or "").lower().strip()
    kb_path = payload.get("kb_path") or os.environ.get("KB_PATH", "kb")
    max_sections = int(payload.get("max_sections", 5))
    results: List[Dict[str, Any]] = []
    if not query:
        return {"tool": "md_lookup", "ok": False, "data": [], "meta": {"t": time.time(), "error": "empty query"}}
    if not os.path.isdir(kb_path):
        return {"tool": "md_lookup", "ok": False, "data": [], "meta": {"t": time.time(), "error": f"kb_path not found: {kb_path}"}}
    for fname in os.listdir(kb_path):
        if not fname.endswith(".md"):
            continue
        full = os.path.join(kb_path, fname)
        try:
            text = open(full, "r", encoding="utf-8").read()
        except Exception:
            continue
        sections = _split_markdown_sections(text)
        scored: List[Tuple[float, Dict[str, Any]]] = []
        for sec in sections:
            content_lower = sec["content"].lower()
            score = sum(content_lower.count(tok) for tok in query.split())
            if score > 0:
                scored.append((score, {"file": fname, "header": sec["header"], "content": sec["content"], "score": score}))
        for score, item in sorted(scored, key=lambda x: x[0], reverse=True)[:max_sections]:
            results.append(item)
    return {"tool": "md_lookup", "ok": True, "data": results, "meta": {"t": time.time(), "count": len(results)}}

def web_search(payload: Dict[str, Any]) -> Dict[str, Any]:
    term = payload.get("query", "")
    return {"tool": "web_search", "ok": True, "data": [{"title": term, "url": "https://example.com?q=" + term}], "meta": {"t": time.time()}}

def schema_validate(payload: Dict[str, Any]) -> Dict[str, Any]:
    from jsonschema import validate, ValidationError
    instance = payload.get("instance")
    schema = payload.get("schema")
    try:
        validate(instance, schema)
        return {"tool": "schema_validate", "ok": True, "data": {"valid": True}, "meta": {"t": time.time()}}
    except ValidationError as e:
        return {"tool": "schema_validate", "ok": False, "data": {"error": e.message}, "meta": {"t": time.time()}}

def cross_check(payload: Dict[str, Any]) -> Dict[str, Any]:
    evidence = payload.get("evidence", [])
    # naive consistency check
    consistent = all("chunk" in e or "text" in e for e in evidence)
    return {"tool": "cross_check", "ok": consistent, "data": {"consistent": consistent}, "meta": {"t": time.time()}}

def fact_consistency(payload: Dict[str, Any]) -> Dict[str, Any]:
    facts = payload.get("facts", [])
    # dummy: mark all consistent
    return {"tool": "fact_consistency", "ok": True, "data": {"facts_checked": len(facts)}, "meta": {"t": time.time()}}

def aggregate_results(payload: Dict[str, Any]) -> Dict[str, Any]:
    parts = payload.get("parts", [])
    summary = " | ".join(str(p) for p in parts)
    return {"tool": "aggregate_results", "ok": True, "data": {"summary": summary}, "meta": {"t": time.time(), "count": len(parts)}}

def dispatch_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
    agent = payload.get("agent")
    task = payload.get("task")
    return {"tool": "dispatch_agent", "ok": True, "data": {"agent": agent, "task": task}, "meta": {"t": time.time()}}

def plan_tasks(payload: Dict[str, Any]) -> Dict[str, Any]:
    objective = payload.get("objective", "")
    steps = [f"Analyze: {objective}", "Retrieve context", "Generate draft", "Verify", "Finalize"]
    return {"tool": "plan_tasks", "ok": True, "data": {"steps": steps}, "meta": {"t": time.time()}}

TOOLS: Dict[str, ToolFn] = {
    "md_lookup": md_lookup,
    "web_search": web_search,
    "schema_validate": schema_validate,
    "cross_check": cross_check,
    "fact_consistency": fact_consistency,
    "aggregate_results": aggregate_results,
    "dispatch_agent": dispatch_agent,
    "plan_tasks": plan_tasks,
}

def run_tool(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    fn = TOOLS.get(name)
    if not fn:
        return {"tool": name, "ok": False, "data": {"error": "unknown tool"}, "meta": {"t": time.time()}}
    return fn(payload)


def _split_markdown_sections(text: str) -> List[Dict[str, str]]:
    sections: List[Dict[str, str]] = []
    current_header = "(root)"
    current_lines: List[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            # flush previous
            if current_lines:
                sections.append({"header": current_header, "content": "\n".join(current_lines).strip()})
            current_header = line.lstrip('#').strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append({"header": current_header, "content": "\n".join(current_lines).strip()})
    return sections
