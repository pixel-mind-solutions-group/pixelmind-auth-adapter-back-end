from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class ApplicationHasUiPermission(Base):
    __tablename__ = "application_has_ui_permissions"

    __table_args__ = (
        UniqueConstraint(
            "realm_id",
            "application_id",
            "ui_permission_id",
            name="uq_app_has_ui_permission",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)
    applicationId = Column(
        "application_id", Integer, ForeignKey("applications.id"), nullable=False
    )
    uiPermissionId = Column(
        "ui_permission_id", Integer, ForeignKey("ui_permissions.id"), nullable=False
    )

    realm = relationship("Realm")
    application = relationship("Application")
    ui_permission = relationship("UiPermission")
