from flask import Flask, render_template, request, jsonify
from agents import run_all_agents, index, documents, model
from rca_generator import generate_rca, save_rca

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/investigate", methods=["POST"])
def investigate():
    data = request.get_json()
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Please enter a query"}), 400
    
    try:
    
        findings = run_all_agents(query)
        
    
        rca = generate_rca(query, findings)
        
        
        save_rca(query, findings, rca)
        
        return jsonify({
            "success": True,
            "query": query,
            "findings": findings,
            "rca": rca
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Log Investigation Tool...")
    print("Open browser at: http://localhost:5000")
    app.run(debug=False, port=5000)