import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)

    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)

    applicationId = Column(
        "application_id", Integer, ForeignKey("applications.id"), nullable=False
    )

    moduleName = Column("module_name", String, nullable=False, unique=True)

    active = Column("active", Boolean, nullable=False, default=True)

    realm = relationship("Realm", back_populates="modules")
    application = relationship("Application", back_populates="modules")
