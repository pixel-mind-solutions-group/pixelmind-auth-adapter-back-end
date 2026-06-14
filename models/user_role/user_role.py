from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    __table_args__ = (
        UniqueConstraint(
            "realm_id",
            "application_id",
            "role_name",
            name="uq_user_roles",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)
    applicationId = Column("application_id", Integer, ForeignKey("applications.id"), nullable=False)

    roleName = Column("role_name", String, nullable=False)
    description = Column("description", String, nullable=True)
    active = Column("active", Boolean, nullable=False, default=True)

    createdBy = Column("created_by", String, nullable=False)
    createdAt = Column("created_at", DateTime, nullable=False)
    updatedBy = Column("updated_by", String)
    updatedAt = Column("updated_at", DateTime)

    realm = relationship("Realm")
    application = relationship("Application")
