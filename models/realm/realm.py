from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base


class Realm(Base):
    __tablename__ = "realms"

    id = Column(Integer, primary_key=True, index=True)

    realm = Column("realm", String, nullable=False)

    internal_uuid = Column("internal_uuid", String, nullable=False, unique=True)

    uuid = Column("uuid", String, nullable=False, unique=True)

    active = Column("active", Boolean, nullable=False, default=True)

    applications = relationship("Application", back_populates="realm")
