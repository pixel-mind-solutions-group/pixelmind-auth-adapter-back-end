from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    clientId = Column("client_id", String, nullable=False, unique=True)

    uuid = Column("uuid", String, nullable=False, unique=True)

    active = Column("active", Boolean, nullable=False)

    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)

    realm = relationship("Realm", back_populates="applications")
