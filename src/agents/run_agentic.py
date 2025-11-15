"""Simple runner simulating orchestrator planning and tool usage."""
from tools.registry import run_tool
from agents.loader import bootstrap

def simulate():
    state = bootstrap()
    plan_resp = run_tool("plan_tasks", {"objective": "Demo objective"})
    retrieval_resp = run_tool("md_lookup", {"query": "demo", "kb_path": "kb", "max_sections": 3})
    verify_resp = run_tool("cross_check", {"evidence": retrieval_resp.get("data", [])})
    return {
        "plan": plan_resp,
        "retrieval": retrieval_resp,
        "verification": verify_resp,
        "bootstrap": state,
    }

if __name__ == "__main__":
    output = simulate()
    print(output)
