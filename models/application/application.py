import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    clientId = Column("client_id", String, nullable=False)

    active = Column("active", Boolean, nullable=False)

    realms = relationship("RealmsHasApplications", back_populates="application")
