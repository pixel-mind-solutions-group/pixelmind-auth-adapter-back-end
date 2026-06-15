from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "realm_id",
            "application_id",
            "user_role_id",
            name="uq_user_profile_composite",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    userId = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)
    applicationId = Column("application_id", Integer, ForeignKey("applications.id"), nullable=False)
    userRoleId = Column("user_role_id", Integer, ForeignKey("user_roles.id"), nullable=False)

    user = relationship("User")
    realm = relationship("Realm")
    application = relationship("Application")
    user_role = relationship("UserRole")
