import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import subprocess

DB_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/security_logs")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class SecurityLog(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    ip = Column(String)
    payload = Column(Text)
    score = Column(Integer)
    action = Column(String)
    reason = Column(String)

def generate_report():
    db = SessionLocal()
    logs = db.query(SecurityLog).order_by(SecurityLog.id.desc()).limit(50).all()
    db.close()

    if not logs:
        print("No logs found to audit.")
        return

    log_summary = "\n".join([f"IP: {l.ip}, Action: {l.action}, Score: {l.score}, Payload: {l.payload[:50]}" for l in logs])
    
    prompt = f"Summarize the following security logs into a Markdown 'Security Insights' report. Highlight major threats and suggest mitigation steps. Logs:\n{log_summary}"
    
    try:
        result = subprocess.run(["gemini", "ask", prompt], capture_output=True, text=True, check=True)
        with open("SECURITY_INSIGHTS.md", "w") as f:
            f.write(result.stdout)
        print("Security report generated: SECURITY_INSIGHTS.md")
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    generate_report()

    
