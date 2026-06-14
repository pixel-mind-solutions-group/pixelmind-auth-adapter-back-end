from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class ModuleHasApiPermission(Base):
    __tablename__ = "module_has_api_permissions"

    __table_args__ = (
        UniqueConstraint(
            "module_id",
            "api_permission_id",
            name="uq_module_has_api_permission",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    moduleId = Column("module_id", Integer, ForeignKey("modules.id"), nullable=False)
    apiPermissionId = Column(
        "api_permission_id", Integer, ForeignKey("api_permissions.id"), nullable=False
    )

    module = relationship("Module")
    api_permission = relationship("ApiPermission")
