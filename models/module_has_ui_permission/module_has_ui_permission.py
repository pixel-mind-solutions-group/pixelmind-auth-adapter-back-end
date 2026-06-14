from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class ModuleHasUiPermission(Base):
    __tablename__ = "module_has_ui_permissions"

    __table_args__ = (
        UniqueConstraint(
            "module_id",
            "ui_permission_id",
            name="uq_module_has_ui_permission",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    moduleId = Column("module_id", Integer, ForeignKey("modules.id"), nullable=False)
    uiPermissionId = Column(
        "ui_permission_id", Integer, ForeignKey("ui_permissions.id"), nullable=False
    )

    module = relationship("Module")
    ui_permission = relationship("UiPermission")
