from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class UserRoleHasModulesHasUiPermission(Base):
    __tablename__ = "user_role_has_modules_has_ui_permission"

    __table_args__ = (
        UniqueConstraint(
            "realm_id",
            "application_id",
            "user_role_id",
            "module_id",
            "ui_permission_id",
            name="uq_user_role_has_modules_has_ui_perm",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    realmId = Column("realm_id", Integer, ForeignKey("realms.id"), nullable=False)
    applicationId = Column("application_id", Integer, ForeignKey("applications.id"), nullable=False)
    userRoleId = Column("user_role_id", Integer, ForeignKey("user_roles.id"), nullable=False)
    moduleId = Column("module_id", Integer, ForeignKey("modules.id"), nullable=True)
    uiPermissionId = Column("ui_permission_id", Integer, ForeignKey("ui_permissions.id"), nullable=False)

    realm = relationship("Realm")
    application = relationship("Application")
    user_role = relationship("UserRole")
    module = relationship("Module")
    ui_permission = relationship("UiPermission")
