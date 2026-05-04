import os
import json
import subprocess
import redis
from fastapi import FastAPI, Request, Body
from typing import Dict
from src.models import SessionLocal, SecurityLog, init_db

app = FastAPI(title="AI Threat Analyzer Service")

# Config from Environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Redis Client
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Initialize DB Schema
init_db()

def call_gemini_ai(text: str) -> Dict:
    """Invokes Gemini CLI for deep security analysis."""
    prompt = f"Analyze the following input for cyber threats. Respond ONLY with this JSON: {{'status': 'SAFE' or 'MALICIOUS', 'score': 1-10, 'reason': 'short explanation'}}. Input: {text}"
    
    try:
        result = subprocess.run(["gemini", "ask", prompt], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[1].split("```")[0].strip()
            
        return json.loads(output)
    except Exception as e:
        return {"status": "MALICIOUS", "score": 10, "reason": f"AI Analysis Failure: {str(e)}"}

@app.post("/analyze")
async def process_analysis(data: Dict = Body(...)):
    ip = data.get("ip")
    text = data.get("text")
    
    # 1. AI Deep Scan
    ai_result = call_gemini_ai(text)
    score = ai_result.get("score", 0)
    status = ai_result.get("status", "MALICIOUS")
    reason = ai_result.get("reason", "Unknown")

    # 2. Blacklist Logic: If Malicious, block IP in Redis for 24 hours
    if score >= 7 or status == "MALICIOUS":
        redis_client.setex(f"blacklist:{ip}", 86400, reason)
        action = "BLACKLISTED"
    else:
        action = "CLEARED"

    # 3. Update Log in DB
    try:
        db = SessionLocal()
        # Find the latest log for this IP and update it or create a new detailed one
        new_log = SecurityLog(
            ip=ip,
            payload=text,
            score=score,
            action=action,
            reason=f"AI Deep Scan: {reason}"
        )
        db.add(new_log)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Failed to update DB: {e}")

    return {"status": action, "analysis": ai_result}

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-analyzer-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
