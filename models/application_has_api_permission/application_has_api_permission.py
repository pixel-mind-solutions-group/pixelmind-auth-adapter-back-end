from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class ApplicationHasApiPermission(Base):
    __tablename__ = "application_has_api_permissions"

    __table_args__ = (
        UniqueConstraint(
            "realm_id",
            "application_id",
            "api_permission_id",
            name="uq_app_has_api_permission",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)
    applicationId = Column(
        "application_id", Integer, ForeignKey("applications.id"), nullable=False
    )
    apiPermissionId = Column(
        "api_permission_id", Integer, ForeignKey("api_permissions.id"), nullable=False
    )

    realm = relationship("Realm")
    application = relationship("Application")
    api_permission = relationship("ApiPermission")
