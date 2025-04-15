from sqlalchemy import Column, String, TIMESTAMP, text, UUID, Integer
from db.engine import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    tokens = Column(Integer, nullable=False, server_default=text('2'))
    created_at = Column(TIMESTAMP(timezone=True),  server_default=text('now()'))