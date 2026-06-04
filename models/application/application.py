from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    applicationName = Column("application_name", String, nullable=False)

    active = Column("active", Boolean, nullable=False)

    uuid = Column("uuid", String, nullable=False, unique=True)
