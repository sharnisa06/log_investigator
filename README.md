🔍 Log Investigation Tool

AI-powered log analysis tool that automatically finds root causes in HDFS log files using a local Small Language Model.


 What it does
- Reads thousands of log lines automatically
- Uses 5 parallel AI agents to analyze different patterns
- Generates a Root Cause Analysis (RCA) report in 2 minutes
- Runs 100% locally — no internet needed



 Tech Stack
- Model: Qwen2.5-1.5B (4-bit quantized, runs locally via Ollama)
- Search: FAISS semantic search
- Embeddings: sentence-transformers
- Backend: Flask (Python)
- Dataset:HDFS logs from Kaggle



##Setup
 1. Install dependencies

pip install sentence-transformers faiss-cpu torch flask request

 2. Install Ollama and download model

 Download Ollama from https://ollama.com/download/windows
ollama pull qwen2.5:1.5b

 3. Build search index
python embedder.py


 4. Run the app

python app.py



## Example Queries

"Why are block operations failing?"
"Which component has the most errors?"
"When did the incident start?"
"Are there any network failures?"




## Project Structure

├── log_parser.py       # parses raw log file
├── embedder.py         # creates FAISS vector index
├── search.py           # semantic search
├── agents.py           # 5 parallel agents
├── rca_generator.py    # generates RCA with Qwen2.5
├── app.py              # Flask web server
└── templates/
    └── index.html      # web UI



## Model Details
 Model : Qwen2.5-1.5B 
 Quantization : 4-bit via Ollama 
 Hardware : CPU only, 8GB RAM 
 Inference : 100% local 


## Dataset
HDFS logs from Kaggle →
https://www.kaggle.com/datasets/ayenuryrr/loghub-hdfs-hadoop-distributed-file-am
