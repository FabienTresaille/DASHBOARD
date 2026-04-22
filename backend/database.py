from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bpia_user:bpia_password@localhost:5432/bpia_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class KnowledgeBase(Base):
    """
    Table pour stocker les 10 ans de data, SOP, frameworks d'offres, et transcripts.
    C'est le 'Moat' (fossé concurrentiel) de l'agence.
    """
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True) # Ex: SOP, framework_offre, transcript_vente
    title = Column(String)
    content = Column(Text)
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Lead(Base):
    """
    Table pour stocker les prospects analysés par l'agent de qualification.
    """
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact_info = Column(String)
    source = Column(String)
    raw_data = Column(Text)
    ai_score = Column(Float, nullable=True)
    ai_justification = Column(Text, nullable=True)
    ai_next_action = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
