import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class RealmsHasApplications(Base):
    __tablename__ = "realms_has_applications"

    id = Column(Integer, primary_key=True, index=True)

    uuid = Column(
        "application_uuid",
        String,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )

    internal_application_uuid = Column(
        "internal_application_uuid",
        String,
        nullable=False,
        unique=True,
    )

    application_id = Column(
        "application_id", Integer, ForeignKey("applications.id"), nullable=False
    )
    realm_id = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)

    application = relationship("Application", back_populates="realms")
    realm = relationship("Realm", back_populates="applications")
