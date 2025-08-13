from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(50), nullable=False)
    requirements = Column(Text, nullable=False)
    complexity = Column(String(20), nullable=False)  # 'basic', 'medium', 'complex'
    status = Column(String(20), default='pending')
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    delivery_path = Column(String(255))

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    payment_method = Column(String(50))
    encrypted_data = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    allocation_ai = Column(Float)
    allocation_reserve = Column(Float)
    allocation_owner = Column(Float)

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(String(50), primary_key=True)  # UUID
    encrypted_contact = Column(Text, nullable=False)
    encrypted_payment_methods = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    last_active = Column(DateTime)
