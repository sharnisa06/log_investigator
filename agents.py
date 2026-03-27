import concurrent.futures
import json
from sentence_transformers import SentenceTransformer
from search import load_index, search


print("Loading model and index...")
index, documents = load_index()
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Ready!\n")



def agent_error_detection(query):
    
    results = search("error exception failed", index, documents, model, top_k=10)
    errors = [r for r in results if r["severity"] in ["WARN", "ERROR"]]
    
    return {
        "agent": "Error Detection",
        "finding": f"Found {len(errors)} error/warning lines",
        "top_errors": [r["message"][:80] for r in errors[:3]],
        "severity_found": list(set(r["severity"] for r in errors))
    }

def agent_time_detection(query):
    
    results = search(query, index, documents, model, top_k=10)
    
    timestamps = [r["timestamp"] for r in results]
    first_time = min(timestamps) if timestamps else "unknown"
    last_time  = max(timestamps) if timestamps else "unknown"
    
    return {
        "agent": "Time Detection",
        "finding": f"Incident window detected",
        "first_seen": first_time,
        "last_seen": last_time,
        "sample_times": timestamps[:3]
    }

def agent_component_detection(query):
    
    results = search(query, index, documents, model, top_k=10)
    
    component_counts = {}
    for r in results:
        comp = r["component"]
        component_counts[comp] = component_counts.get(comp, 0) + 1
    
    top_component = max(component_counts, key=component_counts.get) \
                    if component_counts else "unknown"
    
    return {
        "agent": "Component Detection",
        "finding": f"Most affected component identified",
        "top_component": top_component,
        "all_components": component_counts
    }

def agent_severity_analysis(query):
    
    results = search(query, index, documents, model, top_k=20)
    
    severity_counts = {}
    for r in results:
        sev = r["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    return {
        "agent": "Severity Analysis",
        "finding": "Severity distribution in relevant logs",
        "breakdown": severity_counts,
        "critical_count": severity_counts.get("ERROR", 0) + 
                         severity_counts.get("FATAL", 0)
    }

def agent_block_analysis(query):
    """HDFS specific - find block operation failures"""
    results = search("block exception serve failed", 
                    index, documents, model, top_k=10)
    
    block_ids = []
    for r in results:
        if "blk_" in r["message"]:
            
            parts = r["message"].split()
            for part in parts:
                if part.startswith("blk_"):
                    block_ids.append(part)
    
    return {
        "agent": "Block Analysis",
        "finding": f"Found {len(block_ids)} problematic block operations",
        "affected_blocks": list(set(block_ids))[:5],
        "sample_message": results[0]["message"][:100] if results else "none"
    }

def run_all_agents(user_query):
    
    
    print(f"Running 5 agents in parallel for: '{user_query}'")
    print("=" * 60)
    
    
    agents = [
        agent_error_detection,
        agent_time_detection,
        agent_component_detection,
        agent_severity_analysis,
        agent_block_analysis
    ]
    
    results = []
    
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        futures = {
            executor.submit(agent, user_query): agent.__name__
            for agent in agents
        }
        
    
        for future in concurrent.futures.as_completed(futures):
            agent_name = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"✅ {result['agent']} finished")
            except Exception as e:
                print(f"❌ {agent_name} failed: {e}")
    
    return results

if __name__ == "__main__":
    user_query = "Why are block operations failing?"
    
    findings = run_all_agents(user_query)
    
    print("\n--- ALL AGENT FINDINGS ---")
    for finding in findings:
        print(f"\n[{finding['agent']}]")
        print(json.dumps(finding, indent=2))