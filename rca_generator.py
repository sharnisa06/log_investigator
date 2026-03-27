import json
import requests
from agents import run_all_agents

def generate_rca(user_query, findings):
    """Send agent findings to Qwen via Ollama and get RCA report"""
    
    
    findings_text = ""
    for f in findings:
        findings_text += f"\n[{f['agent']}]\n"
        findings_text += json.dumps(f, indent=2)
        findings_text += "\n"
    

    prompt = f"""You are an expert system reliability engineer analyzing HDFS distributed system logs.

A user asked: "{user_query}"

Multiple analysis agents investigated the logs and found the following:

{findings_text}

Based on these findings, generate a clear Root Cause Analysis (RCA) report with these sections:

1. INCIDENT SUMMARY
2. TIMELINE
3. AFFECTED COMPONENTS  
4. ROOT CAUSE
5. SUPPORTING EVIDENCE
6. RECOMMENDED ACTIONS

Be specific, concise, and technical."""

    print("Sending findings to Qwen2.5 for RCA generation...")
    print("(This may take 30-60 seconds on CPU)\n")
    
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    
    if response.status_code == 200:
        rca = response.json()["response"]
        return rca
    else:
        return f"Error calling Ollama: {response.status_code}"

def save_rca(query, findings, rca_text):
    """Save the full report to a file"""
    report = {
        "query": query,
        "agent_findings": findings,
        "rca_report": rca_text
    }
    
    with open("rca_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    with open("rca_report.txt", "w") as f:
        f.write(f"QUERY: {query}\n")
        f.write("=" * 60 + "\n\n")
        f.write(rca_text)
    
    print("\nReport saved to rca_report.txt and rca_report.json")

if __name__ == "__main__":
    user_query = "Why are block operations failing in HDFS?"
    
    
    print("STEP 1: Running parallel agents...")
    findings = run_all_agents(user_query)
    
    
    print("\nSTEP 2: Generating RCA with Qwen2.5...")
    rca = generate_rca(user_query, findings)
    
    
    print("\n" + "=" * 60)
    print("FINAL RCA REPORT")
    print("=" * 60)
    print(rca)
    
    save_rca(user_query, findings, rca)