import re
import json


LOG_FILE = r"C:\Users\cyril\Downloads\archive (8)\HDFS_2k\HDFS_2k.log"


LOG_PATTERN = re.compile(
    r'(\d{6})\s+(\d{6})\s+(\d+)\s+(INFO|WARN|ERROR|FATAL|DEBUG)\s+(\S+):\s+(.*)'
)

def parse_log_line(line):
    
    line = line.strip()
    if not line:
        return None
    
    match = LOG_PATTERN.match(line)
    if match:
        date, time, thread_id, severity, component, message = match.groups()
        return {
            "timestamp": f"{date} {time}",
            "date": date,
            "time": time,
            "thread_id": thread_id,
            "severity": severity,
            "component": component,
            "message": message,
            "raw": line
        }
    else:
        
        return {
            "timestamp": "unknown",
            "date": "unknown",
            "time": "unknown", 
            "thread_id": "unknown",
            "severity": "UNKNOWN",
            "component": "unknown",
            "message": line,
            "raw": line
        }

def load_logs(filepath):
    
    documents = []
    failed = 0
    
    print(f"Reading log file: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    print(f"Total lines found: {len(lines)}")
    
    for i, line in enumerate(lines):
        doc = parse_log_line(line)
        if doc:
            doc["line_number"] = i + 1  # track original line number
            documents.append(doc)
        else:
            failed += 1
    
    print(f"Successfully parsed: {len(documents)} lines")
    print(f"Failed to parse:     {failed} lines")
    return documents

def show_summary(documents):
    """Print a quick summary of what we found"""
    print("\n--- LOG SUMMARY ---")
    
    
    severity_counts = {}
    component_counts = {}
    
    for doc in documents:
        sev = doc["severity"]
        comp = doc["component"]
        
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        component_counts[comp] = component_counts.get(comp, 0) + 1
    
    print("\nSeverity breakdown:")
    for sev, count in sorted(severity_counts.items()):
        print(f"  {sev:10} : {count} lines")
    
    print("\nTop 5 components:")
    top_components = sorted(component_counts.items(), 
                           key=lambda x: x[1], reverse=True)[:5]
    for comp, count in top_components:
        print(f"  {count:5} : {comp}")
    
    print("\nFirst 3 parsed documents:")
    for doc in documents[:3]:
        print(json.dumps(doc, indent=2))


if __name__ == "__main__":
    documents = load_logs(LOG_FILE)
    show_summary(documents)
    print("\nDay 1 Complete! Log parser is working.")