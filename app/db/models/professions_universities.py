from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_model import Base



class ProfessionsUniversities(Base):
    __tablename__ = "professions_universities"
    profession_id = Column(Integer, ForeignKey("professions.id"), primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"), primary_key=True)

