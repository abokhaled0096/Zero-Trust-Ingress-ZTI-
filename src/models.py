import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Config from Environment
DB_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/security_logs")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SecurityLog(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip = Column(String, index=True)
    payload = Column(Text)
    score = Column(Integer)
    action = Column(String)
    reason = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
