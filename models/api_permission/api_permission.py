from sqlalchemy import Column, Integer, String, Boolean, DateTime
from core.database import Base


class ApiPermission(Base):
    __tablename__ = "api_permissions"

    id = Column(Integer, primary_key=True, index=True)

    apiPermissionName = Column(
        "api_permission_name", String, nullable=False, unique=True
    )

    description = Column("description", String)

    active = Column("active", Boolean, nullable=False, default=True)

    createdBy = Column("created_by", String, nullable=False)
    createdAt = Column("created_at", DateTime, nullable=False)
    updatedBy = Column("updated_by", String)
    updatedAt = Column("updated_at", DateTime)
