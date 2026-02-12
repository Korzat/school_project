from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_model import Base



class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True)
    university_name = Column(String)
    description = Column(String)

    professions = relationship("Profession", secondary="professions_universities", back_populates="universities")

