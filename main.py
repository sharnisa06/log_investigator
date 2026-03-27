import sys
from agents import run_all_agents
from rca_generator import generate_rca, save_rca

def main():
    print("=" * 60)
    print("   PARALLEL SLM LOG INVESTIGATION TOOL")
    print("   Model: Qwen2.5-1.5B | Search: FAISS")
    print("=" * 60)
    
    
    if len(sys.argv) > 1:
        
        query = " ".join(sys.argv[1:])
    else:
        
        print("\nWhat do you want to investigate?")
        query = input("Query: ").strip()
        if not query:
            query = "Why are block operations failing?"
    
    print(f"\nInvestigating: '{query}'")
    print("-" * 60)
    
    
    findings  = run_all_agents(query)
    rca       = generate_rca(query, findings)
    save_rca(query, findings, rca)
    
    print("\n" + "=" * 60)
    print("FINAL RCA REPORT")
    print("=" * 60)
    print(rca)
    print("\nDone! Report saved to rca_report.txt")

if __name__ == "__main__":
    main()