from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_model import Base



class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True)
    profession_name = Column(String)

    universities = relationship("University", secondary="professions_universities", back_populates="professions")

