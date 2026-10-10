from sqlalchemy import create_engine, Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class IdempotencyKey(Base):
    __tablename__ = 'idempotency_keys'

    id = Column(String, primary_key=True)
    operation = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)

def register_key(operation, lease_duration=timedelta(hours=1)):
    session = Session()
    key = IdempotencyKey(id=operation, operation=operation, expires_at=datetime.utcnow() + lease_duration)
    session.add(key)
    session.commit()
    session.close()

def is_key_registered(operation):
    session = Session()
    key = session.query(IdempotencyKey).filter_by(id=operation).first()
    session.close()
    return key is not None and not key.is_expired()